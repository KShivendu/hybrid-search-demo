from lark import Lark, Transformer

from qdrant_client import QdrantClient
from qdrant_client.http import models

from constants import COLLECTION_NAME, LABELS_COLLECTION_NAME, LABELS, DIMS

from embed import generate_embeddings

# Define the grammar for the language
grammar = """
    start: expression
    ?expression: term ("or" term)* -> should
    ?term: factor ("and" factor)* -> must
    ?factor: "not" factor -> must_not
           | TAG
           | "(" expression ")"
    TAG: /\w+/
    %import common.WS
    %ignore WS
"""

# Create the parser with the defined grammar
parser = Lark(grammar, start='start')

client = QdrantClient(":memory:")

client.delete_collection(LABELS_COLLECTION_NAME)
client.create_collection(
    collection_name=LABELS_COLLECTION_NAME,
    vectors_config=models.VectorParams(size=DIMS, distance=models.Distance.COSINE),
)

# Upsert labels:
label_embeddings = generate_embeddings([label for label in LABELS])
operation_info = client.upsert(
    collection_name=LABELS_COLLECTION_NAME,
    wait=True,
    points=[
        models.PointStruct(
            id=k,
            vector=label_embeddings[k],
            payload={"name": label},
        )
        for k, label in enumerate(LABELS)
    ],
)



# Define a transformer to convert the parsed tree into the desired format
class MyTransformer(Transformer):
    def should(self, items):
        # Flatten the list if there's only one item
        if len(items) == 1:
            return items[0]
        return models.Filter(should=items)
        # return {"should": items}

    def must(self, items):
        if len(items) == 1:
            return items[0]

        return models.Filter(must=items)
        # return {"must": items}

    def must_not(self, items):
        # Items list has a single element
        # because of not taking in only 1 value
        return models.Filter(must_not=[items[0]])
        # return {"must_not": item[0]}

    def TAG(self, token):
        token_str = str(token)
        if token_str in LABELS:
            return models.FieldCondition(key="tags", match=models.MatchValue(value=token_str))

        # Find closest matching tags:
        embedding = generate_embeddings(token_str)
        labels = client.search(collection_name=LABELS_COLLECTION_NAME, query_vector=embedding, score_threshold=0.88)

        if labels:
            return models.FieldCondition(key="tags", match=models.MatchAny(any=[l.payload['name'] for l in labels]))
        else:
            return {}
            # return models.Filter(should=models.FieldCondition(key="tags", match=models.MatchAny(any=[])))

        # return models.FieldCondition(key="tags", match=models.MatchValue(value=label.payload['name']))
        # return {"match": labels[0]["name"]}

# Function to parse and transform the expression
def parse_expression(expression):
    if expression == "":
        return {}
    tree = parser.parse(expression)
    transformed_tree = MyTransformer().transform(tree)
    result = transformed_tree.children[0]

    if isinstance(result, models.FieldCondition):
        return models.Filter(must=[result])

    return result


if __name__ == "__main__":
    # Example usage
    expression = "(foo and (not food)) or glass" # (glass doesn't exist)
    result = parse_expression(expression)
    print(result)

