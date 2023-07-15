import os
import sys
from concurrent import futures
import grpc
from photo_service import Photo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../proto")))
import photo_pb2_grpc


# start grpc server
def start():
    server = grpc.server(
        futures.ThreadPoolExecutor(), options=[("grpc.max_receive_message_length", -1)]
    )
    photo_pb2_grpc.add_PhotoServiceServicer_to_server(Photo(), server)
    address = f"{os.environ['DOMAIN']}:{os.environ['PORT']}"
    server.add_insecure_port(address)
    print(f"starting photos server on {address}")
    server.start()
    server.wait_for_termination()
