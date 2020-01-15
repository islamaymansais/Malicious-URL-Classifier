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