import os
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import vision
from google.cloud.vision_v1 import types


# initialize firebase admin sdk
def initialize():
    cred = credentials.Certificate(os.environ["FIREBASE_SERVICE_ACCOUNT_KEY_PATH"])
    firebase_admin.initialize_app(cred, {"storageBucket": os.environ["STORAGE_BUCKET"]})


# upload photo to firebase storage
def upload_photo(uid, name, content, content_type):
    bucket = storage.bucket()
    blob = bucket.blob(f"{uid}/{name}")
    blob.upload_from_string(content, content_type=content_type)
    return blob.generate_signed_url(
        version="v4", expiration=datetime.timedelta(days=1), method="GET"
    )


# labels photo via gcp vision api
def detect_labels(content):
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    return [label.description for label in labels]
