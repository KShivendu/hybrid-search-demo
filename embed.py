from sentence_transformers import SentenceTransformer, util
from PIL import Image
from pathlib import Path

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

#Encode an image:

# def encode_image(image_path: Path):
#     image = Image.open(image_path)
#     return model.encode(image)



def generate_embeddings(*args, **kwargs):
    # img = Image.open('two_dogs_in_snow.jpg')
    # text = ['Two dogs in the snow', 'A cat on a table', 'A picture of London at night']
    return model.encode(*args, **kwargs)

def generate_label_embeddings():
    pass

# def gen_embeddings():
#     ibed = imgbeddings()
#     embeddings = ibed.to_embeddings([image])

if __name__ == "__main__":
    txt_embeddings = generate_embeddings(['Two dogs in the snow', 'A cat on a table',])
