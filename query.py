from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, GeoRadius, GeoPoint, MatchValue
from qdrant_client.http import models
from imgbeddings import imgbeddings

from constants import COLLECTION_NAME, DIMS, AGAETE
from embed import generate_embeddings
from parser2 import parse_expression

client = QdrantClient(prefer_grpc=True)

def run_search(query: str, expression: str, tags: List[str] = None, limit: int = 5):
    # filter = Filter(
    #     must=[
    #         FieldCondition(key="tags", match=MatchValue(value=tag))
    #         for tag in tags
    #     ]
    #         # + [FieldCondition(
    #         #     key="location", geo_radius=GeoRadius(center=AGAETE, radius=1000.0)
    #         # )]
    # )
    filter = parse_expression(expression)

    if query == "":
        return (client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=filter,
            limit=limit
         )[0], filter)

    query_vector = generate_embeddings(query)

    return (client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        # query_filter=Filter(
        #     must=[
        #         FieldCondition(key=f"tags.{tag}", range=models.Range(gte=1))
        #         for tag in tags
        #     ]
        # ),
        query_filter=filter,
        limit=limit,
    ), filter)


if __name__ == "__main__":
    res = run_search("luggage", expression="person or bag")
    print(res)
