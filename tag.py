from imageai.Detection import ObjectDetection
import os
import collections

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
detector.loadModel()

def generate_tags(image_path):
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(execution_path, image_path),
        # output_image_path=os.path.join(execution_path, "imagenew.jpg"),
        minimum_percentage_probability=98,
    )
    return list({d['name'] for d in detections})
    # return collections.Counter([d["name"] for d in detections])


if __name__ == "__main__":
    detections = detector.detectObjectsFromImage(
        input_image=os.path.join(execution_path, "data/20231218_201842.jpg"),
        # output_image_path=os.path.join(execution_path, "imagenew.jpg"),
        minimum_percentage_probability=30,
    )

    print(detections)

    for eachObject in detections:
        print(
            eachObject["name"],
            " : ",
            eachObject["percentage_probability"],
            # " : ",
            # eachObject["box_points"],
        )
        print("--------------------------------")
