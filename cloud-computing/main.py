# Important packages
import os
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
import numpy as np
from keras_preprocessing import image
import tensorflow as tf
import boto3

app = Flask(__name__)
api = Api(app)

# Access Key
ACCESS_ID = 'AKIATK3OQ7EKGOJX2J6F'
ACCESS_KEY = '8+4f43izL+oTweLowox5wp9Q6ZzcJu1TKg+hEMh6'

# Call the model
model = tf.keras.models.load_model('content/the_sentinel')

# Build the API
## get to upload image
## Model get Arguments
model_get_args = reqparse.RequestParser()
model_get_args.add_argument("s3_uri", type=str, help="s3 URI is required", required=True)

# call Resource Fields
model_get_resource_fields = {
    "s3_uri": fields.String,
    "predict": fields.String
    }

# s3://the-sentinel-bucket/images/fian.png

class Model_get(Resource):
    """
    Build call API to
    1. get the image
    """

    @marshal_with(model_get_resource_fields)
    def get(self):
        args_call = model_get_args.parse_args()
        s3_uri = {"s3_uri":args_call['s3_uri']}
        s3_obj = s3_uri['s3_uri'][25:]
        s3_dir = 'tmp/' + s3_uri['s3_uri'][32:]
        bucket = 'the-sentinel-bucket'
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
        s3.download_file(bucket, s3_obj, s3_dir)
        
        img = image.load_img(s3_dir, target_size=(256, 256))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        uploaded_image = np.vstack([x])

        classification_proba = model.predict(uploaded_image)
        image_class = classification_proba.argmax(axis=-1)

        if image_class[0]==1:
          predict = 'Focus'
        else:
          predict = 'Not Focus'

        result = {
            "s3_uri":s3_uri,
            "predict":predict
        }
        
        return result, 201

class Home(Resource):
    def get(self):
        return "Welcome to The Sentinel Project!", 200

## Routing
api.add_resource(Home, '/')
api.add_resource(Model_get, '/model/get')

# # Test Main
# if __name__ == "__main__":
#     app.run()

# Deploy Main
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))