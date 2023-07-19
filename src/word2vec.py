import sys
import os
import grpc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../protos")))
import word2vec_pb2_grpc
import word2vec_pb2


# get word2vec embedding from a list of words
def embed_words(words):
    with grpc.insecure_channel(os.environ["WORD2VEC_SERVER_ADDRESS"]) as channel:
        stub = word2vec_pb2_grpc.Word2VecServiceStub(channel)
        response = stub.EmbedWords(word2vec_pb2.EmbedWordsRequest(words=words))
        embeddings = [embedding.embedding for embedding in response.embeddings]
        return embeddings
