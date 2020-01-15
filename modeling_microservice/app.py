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
#                                        Modelling Endpoints                                     #
#------------------------------------------------------------------------------------------------#

@app.route("/train_log_reg",methods=["GET"])
def train_log_reg():

    hyperparameters = request.json["hyperparameters"]

    # TODO add function to retrieve from database
    # Get data from SQL DB
    df = 

    # Clean data
    df, balanced = clean_df(df, "URL_Type_obf_Type")

    # Split dataset
    x = df.iloc[:,:-1].values
    y = df.iloc[:, -1].values
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.90, random_state=42)

    # Scale data
    x_train = scale(x_train)

    # Grid Search Logistic Regression
    best_params = log_reg_grid_search(balanced, hyperparameters, x_train, y_train)

    # Train logistic regression model based on grid search best params 
    log_reg = LogisticRegression(**best_params)
    model = log_reg.fit(x_train, y_train)

    # Predict & Evaluate model
    y_pred = model.predict(x_test)
    if balanced==False:
        average="weighted"
    else:
        average="micro"

    # TODO: add function to send saved model to cloud storage
    

    metrics = {
        "accuracy":accuracy_score(y_pred,y_test),
        "recall":recall_score(y_pred,y_test,average=average),
        "precision":precision_score(y_pred,y_test,average=average)
        "f1_score":f1_score(y_pred,y_test,average=average)
    }

    return jsonify metrics
