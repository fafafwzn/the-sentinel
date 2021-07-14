import tensorflow as tf
import tensorflowjs as tfjs
import numpy as np
import base64
import io
import scipy
import json
import cv2
from keras.preprocessing import image
from google.colab import files
import boto3

uploaded = files.upload()

def write_to_file(save_path, data):
  with open(save_path, "wb") as f:
    f.write(base64.b64decode(data))

def get_model():
    bucket = boto3.resource('s3').Bucket('the-sentinel-bucket')
    bucket.download_file('tfjs_model/model.json', '/tmp/model.json')
    model = 

def ocr(img):
  ocr_text = pytesseract.image_to_string(img, config = "eng")
  return ocr_text

def lambda_handler(event, context=None):
    
    write_to_file("/tmp/photo.jpg", event["body"])
    im = cv2.imread("/tmp/photo.jpg")
    
    ocr_text = ocr(im)
     
    # Return the result data in json format
    return {
      "statusCode": 200,
      "body": ocr_text
    }

for fn in uploaded.keys():
  path = fn
  img = image.load_img(path, target_size=(256, 256))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)

  uploaded_image = np.vstack([x])
  classification_proba = model.predict(uploaded_image)
  image_class = classification_proba.argmax(axis=-1)

  print(fn)

  if image_class[0]==1:
    print('Focus')
  else:
    print('Not Focus')

  print(classification_proba)