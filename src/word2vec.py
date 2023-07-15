from gensim.models import KeyedVectors

print("loading model")
# load model
model_path = "../model/GoogleNews-vectors-negative300.bin.gz"
model = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=None)


# generate word embeddings from a list of words using word2vec embeddings
def embed_words(words):
    return [
        model.get_vector(word).tolist() for word in words 
        if word in model.key_to_index
    ]
