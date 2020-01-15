import os
import json
import yaml
import logging
import logging.config
import mysql.connector

from base64 import b64decode
from urllib.parse import urlparse
from mysql.connector import pooling,Error
from flask import Flask,jsonify,request,make_response


logger=logging.getLogger(__name__)

#------------------------------------------------------------------------------------------------#
#                                      Database credentials                                      #
#------------------------------------------------------------------------------------------------#

vcap = json.loads(os.environ.get('VCAP_SERVICES'))

if vcap:
    print('Found VCAP_SERVICES credentials')
    if 'compose-for-mysql' in vcap:
        mysqlCreds=urlparse(vcap['compose-for-mysql'][0]['credentials']['uri'])
        mysqlUser=mysqlCreds.username
        mysqlPassword=mysqlCreds.password
        mysqlUrl=mysqlCreds.hostname
        mysqlPort=mysqlCreds.port
        mysqlDb=mysqlCreds.path[1:]
        mysqlSsl_ca=b64decode(vcap['compose-for-mysql'][0]['credentials']['ca_certificate_base64'])
    if 'cloudantNoSQLDB' in vcap:
        cloudantCreds=vcap['cloudantNoSQLDB'][0]['credentials']
        cloudantUser=cloudantCreds['username']
        cloudantPassword=cloudantCreds['password']
        cloudantUrl=cloudantCreds['url']
else:
    print('VCAP_SERVICES credentials not found')

# Write VCAP CA Cert to temp file for use
with open('./tmpCert.pem', 'wb') as f:
    f.write(mysqlSsl_ca)
    f.close()

#------------------------------------------------------------------------------------------------#
#                                         Setup Logging                                          #
#------------------------------------------------------------------------------------------------#

def setup_logging(default_path='./logging/log_config.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
        Setup logging configuration
    """
    path=default_path
    value=os.getenv(env_key, None)

    if value:
        path=value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config=yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

#------------------------------------------------------------------------------------------------#
#                                       Database methods                                         #
#------------------------------------------------------------------------------------------------#

def read_from_sql(connect,columns,res_columns,datatable):
    """
        Retrieve the mysql datatable to pandas dataframe
        Paras:
            connect     : mysql database connection
            cmd         : sql command
            columns     : the columns in data table
            res_columns : the columns returned
            datatable   : name for the datatable
        return:
            df          : pandas dataframe
    """

    cmd="select * from {}".format(datatable)

    try:
        cur=connect.cursor()
        cur.execute(cmd)
        myresult=cur.fetchall()
        df=pd.DataFrame(myresult,columns=columns)
        cur.close()
    except Exception as e:
        logger.error('{} data error {}'.format(datatable,e))

    return df[res_columns]


def write_to_sql(df,df_name,connection):

    """
        Pushes data to mysql database
        Paras:
            connect     : mysql database connection
            cmd         : sql command
            columns     : the columns in data table
            res_columns : the columns returned
            datatable   : name for the datatable
        return:
            df          : pandas dataframe
    """

    message=""
    status_code=200
    records_step=1000
    print("Pushing to database")

    column_names=df.columns
    
    records = [tuple(row) for _, row in df.iterrows()]

    # get the sql command
    dt_sql="{}({})".format(df_name,','.join(column_names))
    df_sql="Values({}{})".format("%s,"*(len(column_names)-1),"%s")
    sql_command="INSERT into {} {}".format(dt_sql,df_sql)

    # push dataframe to datatable
    
    try:
        cursor=connection.cursor()
        for i in range(0,len(records),records_step):

            if len(records)<records_step:
                temp_records=records[i:i+len(records)]
                
            else:
                temp_records=records[i:i+records_step]
                
            print("{} records push to the database".format(len(temp_records)))

            cursor.executemany(sql_command,temp_records)
            connection.commit()

    except Exception as e:
        status_code=500
        print('Data pushing error {}'.format(e))

    finally: 
        
        if status_code == 200:
            message += "Push to {} success.".format(df_name)
        else:
            message += "Push to {} fail.".format(df_name)

        cursor.close()
        connection.close()

    return message
    

