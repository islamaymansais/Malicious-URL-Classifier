from utils import *

app=Flask(__name__)

#------------------------------------------------------------------------------------------------#
#                                       Error handling and test                                  #
#------------------------------------------------------------------------------------------------#

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Bad request"}),400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}),404)

@app.route("/",methods=["GET"])
def test_app():
    return jsonify({"success": "true"})


#------------------------------------------------------------------------------------------------#
#                                           Main Endoints                                        #
#------------------------------------------------------------------------------------------------#

@app.route("/check_urls",methods=["POST"])
def check_urls():
    urls = request.json["urls"]

    # 1) Check if URLS exist in SQL DB
    # 2) If exists in DB, return classification of each URL to user
    # 3) I doesn't exist in DB:
    #       - send to preprocessing container for processing
    #       - retrieve preprocessed results
    #       - send preprocessed results to modelling container
    #       - retrieve classified results
    #       - push classifiedresults to SQL DB,
    #       - return classification results to user

    return jsonify({"success": "true"})


#------------------------------------------------------------------------------------------------#
#                                               Entry point                                      #
#------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    # setup_logging()
    logging.info('start host')
    # cos = ibm_boto3.resource('s3',
    #                      ibm_api_key_id=COS_API_KEY_ID,
    #                      ibm_service_instance_id=COS_RESOURCE_CRN,
    #                      ibm_auth_endpoint=COS_AUTH_ENDPOINT,
    #                      config=Config(signature_version="oauth"),
    #                      endpoint_url=COS_ENDPOINT)   

    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)