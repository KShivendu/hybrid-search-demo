import requests
from PIL import Image
from pathlib import Path
from tqdm import tqdm

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    PayloadSchemaType,
)

from constants import COLLECTION_NAME, DIMS
from embed import generate_embeddings
from location import get_gps_coordinates
from tag import generate_tags

RECREATE_COLLECTION = True
BATCH_SIZE = 10

# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
# image = Image.open(requests.get(url, stream=True).raw)

IMG_DIR = Path("gran-canaria") # Path("data")

image_paths = list(IMG_DIR.glob("*")) # [:25]  # FIXME: Remove [:25]

# Create batches of 10:
embeddings = []
metadata = []

for batch in tqdm(
    [image_paths[i : i + BATCH_SIZE] for i in range(0, len(image_paths), BATCH_SIZE)]
):
    batch_images = [Image.open(str(path)) for path in batch]
    batch_embeddings = generate_embeddings(batch_images)
    embeddings.extend(batch_embeddings)

    batch_locations = [get_gps_coordinates(img_path) for img_path in batch]
    batch_tags = [generate_tags(img_path) for img_path in batch]

    metadata.extend(
        {
            "image_path": str(path),
            "tags": batch_tags[j],
            "location": {
                "lat": batch_locations[j][0],
                "long": batch_locations[j][1],
            }
            if batch_locations[j][0]
            else None,
        }
        for j, path in enumerate(batch)
    )

# import pdb; pdb.set_trace()

client = QdrantClient(prefer_grpc=True)

if RECREATE_COLLECTION:
    client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=DIMS, distance=Distance.COSINE),
    )


client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="location",
    field_schema=PayloadSchemaType.GEO,
)

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="tags",
    field_schema=PayloadSchemaType.KEYWORD,
)

operation_info = client.upsert(
    collection_name=COLLECTION_NAME,
    wait=True,
    points=[
        PointStruct(
            id=i,
            vector=embeddings[i],
            payload={
                # "location": {"lat": 12.971667, "lon": 77.594444},
                **metadata[i],
            },
        )
        for i in range(len(embeddings))
    ],
)
