#! /usr/bin/python3
# Important packages
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from keras_preprocessing import image
import tensorflow as tf
import boto3
import numpy as np

# Not Important packages
# import base64
# import io
# import scipy
# import json
# import cv2
# from keras.preprocessing import image

app = Flask(__name__)
api = Api(app)

# Access Key
ACCESS_ID = 'AKIATK3OQ7EKGOJX2J6F'
ACCESS_KEY = '8+4f43izL+oTweLowox5wp9Q6ZzcJu1TKg+hEMh6'

# Call the model
model = tf.keras.models.load_model('the_sentinel_model')

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

# Test Main
if __name__ == "__main__":
    app.run(debug=True)

# # Deploy Main
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))







# ACCESS_KEY = 'ABC'
# SECRET_KEY = 'XYZ'

# session = Session(aws_access_key_id=ACCESS_KEY,
#               aws_secret_access_key=SECRET_KEY)
# s3 = session.resource('s3')
# your_bucket = s3.Bucket('bucket_name')

# for s3_file in your_bucket.objects.all():
#     print(s3_file.key) # prints the contents of bucket

# s3 = boto3.client ('s3')

# s3.download_file('your_bucket','k.png','/Users/username/Desktop/k.png')



# uploaded = files.upload()

# def write_to_file(save_path, data):
#   with open(save_path, "wb") as f:
#     f.write(data)

# def get_model():
#     bucket = boto3.resource('s3').Bucket('the-sentinel-bucket')
#     bucket.download_file('tfjs_model/saved_model.pb', '/tmp/saved_model.pb')
#     model = tf.load_model()

# def ocr(img):
#   ocr_text = pytesseract.image_to_string(img, config = "eng")
#   return ocr_text

# def lambda_handler(event, context=None):
    
#     write_to_file("/tmp/photo.jpg", event["body"])
#     im = cv2.imread("/tmp/photo.jpg")
    
#     ocr_text = ocr(im)
     
#     # Return the result data in json format
#     return {
#       "statusCode": 200,
#       "body": ocr_text
#     }

# for fn in uploaded.keys():
#   # Dapetin Path
#   path = fn
#   img = image.load_img(path, target_size=(256, 256))
#   imgplot = plt.imshow(img)
#   x = image.img_to_array(img)
#   x = np.expand_dims(x, axis=0)
#   uploaded_image = np.vstack([x])
  
#   # Klasifikasi model
#   classification_proba = model.predict(uploaded_image)
#   image_class = classification_proba.argmax(axis=-1)

#   if image_class[0]==1:
#     print('Focus')
#   else:
#     print('Not Focus')

#   print(classification_proba)