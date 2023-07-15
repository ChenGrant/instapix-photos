import os
import sys
import word2vec
import gcp
import db
from concurrent import futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../proto")))
import photo_pb2
import photo_pb2_grpc


class Photo(photo_pb2_grpc.PhotoServiceServicer):
    def GetPhotos(self, request, context):
        print("GetPhotos request received")
        
        uid = request.uid
        db.initialize()
        photos = db.select_photos(uid=uid)
        db.close()
        for photo in photos:
            response = photo_pb2.GetPhotoResponse(
                photo={
                    "id": photo["id"],
                    "uid": photo["uid"],
                    "name": photo["name"],
                    "content_type": photo["content_type"],
                    "src": photo["src"],
                }
            )
            yield response

    # override photo_pb2_grpc.PhotoServiceServicer UploadPhotos method
    def UploadPhotos(self, requests, context):
        print("UploadPhotos request received")
        
        # unpack files from request
        photos = [
            {
                "uid": request.photo.uid,
                "name": request.photo.name,
                "content": request.photo.content,
                "content_type": request.photo.content_type,
            }
            for request in requests
        ]

        def process_and_store_photo(photo):
            # store photos in firebase storage
            photo["src"] = gcp.upload_photo(**photo)
            # label photos with gcp vision api
            photo["labels"] = gcp.detect_labels(photo["content"])
            # get word2vec vector for photos
            photo["word2vec"] = word2vec.embed_words(photo["labels"])
            del photo["content"]
            # save photo in mysql
            db.add_photo(**photo)

        # use multithreading to concurrently upload photos
        db.initialize()
        with futures.ThreadPoolExecutor() as executor:
            executor.map(process_and_store_photo, photos)
        db.close()

        return photo_pb2.UploadPhotosResponse(uploaded=True)
