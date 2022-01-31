import json
from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

from utils import download_image_data
from redis_driver import get_instance as get_redis_driver_instance, initialize as initialize_redis_driver
from ml_driver import get_instance as get_ml_driver_instance, initialize as initialize_ml_driver

load_dotenv()

app = Flask(__name__)
CORS(app)

initialize_redis_driver()
initialize_ml_driver()

@app.route("/", methods = ["POST"])
@cross_origin()
def get_inference():
    # Download the image data
    image_data = download_image_data(request.get_json()['url'])

    # Preprocess the image
    preprocessed_image = get_ml_driver_instance().process_request_data(image_data)
    
    # Get the scores for all the labels we predict
    scores = get_redis_driver_instance().predict(preprocessed_image)

    # Find the top 3 predictions
    predictions = get_ml_driver_instance().get_predictions(scores)

    # Return this response
    resp = Response(json.dumps(predictions))
    resp.headers['Content-Type'] = 'application/json'
    return resp

app.run(host = '0.0.0.0')