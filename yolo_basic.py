from ultralytics import YOLO
from openai import OpenAI
from dotenv import load_dotenv
import os

Yolo_classes = {
 0: u'person',
 1: u'bicycle',
 2: u'car',
 3: u'motorcycle',
 4: u'airplane',
 5: u'bus',
 6: u'train',
 7: u'truck',
 8: u'boat',
 9: u'traffic light',
 10: u'fire hydrant',
 11: u'stop sign',
 12: u'parking meter',
 13: u'bench',
 14: u'bird',
 15: u'cat',
 16: u'dog',
 17: u'horse',
 18: u'sheep',
 19: u'cow',
 20: u'elephant',
 21: u'bear',
 22: u'zebra',
 23: u'giraffe',
 24: u'backpack',
 25: u'umbrella',
 26: u'handbag',
 27: u'tie',
 28: u'suitcase',
 29: u'frisbee',
 30: u'skis',
 31: u'snowboard',
 32: u'sports ball',
 33: u'kite',
 34: u'baseball bat',
 35: u'baseball glove',
 36: u'skateboard',
 37: u'surfboard',
 38: u'tennis racket',
 39: u'bottle',
 40: u'wine glass',
 41: u'cup',
 42: u'fork',
 43: u'knife',
 44: u'spoon',
 45: u'bowl',
 46: u'banana',
 47: u'apple',
 48: u'sandwich',
 49: u'orange',
 50: u'broccoli',
 51: u'carrot',
 52: u'hot dog',
 53: u'pizza',
 54: u'donut',
 55: u'cake',
 56: u'chair',
 57: u'couch',
 58: u'potted plant',
 59: u'bed',
 60: u'dining table',
 61: u'toilet',
 62: u'tv',
 63: u'laptop',
 64: u'mouse',
 65: u'remote',
 66: u'keyboard',
 67: u'cell phone',
 68: u'microwave',
 69: u'oven',
 70: u'toaster',
 71: u'sink',
 72: u'refrigerator',
 73: u'book',
 74: u'clock',
 75: u'vase',
 76: u'scissors',
 77: u'teddy bear',
 78: u'hair drier',
 79: u'toothbrush'}
Yolo_value = list(Yolo_classes.values())


def load_yolo_model():
    return YOLO('yolov8n.pt')

def perform_object_detection(model, image_url, confidence_threshold=0.25):
    result = model.predict(source=image_url, conf=confidence_threshold, save=False, save_txt=False)
    return result

def count_detected_classes(result):
    result_tensor = result[0].boxes.cls
    result_class = result_tensor.tolist()
    
    for i,j in enumerate(result_class):
        temp = Yolo_classes.__getitem__(j)
        result_class[i] = temp   
        
    result_class
    count_class={}
    
    for i in result_class:
        try: count_class[i] += 1
        except: count_class[i] = 1
    return count_class

def format_class_counts(count_class, class_names):
    formatted_string = ""
    
    for j, k in count_class.items():
        formatted_string += f"{j}는 {str(k)}개 "
    
    return formatted_string

def interact_with_gpt3(formatted_string):
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"현재 매장 내부에 있는 Class들은 {formatted_string}이다. 지금 매장 내부의 상황을 설명해줘.",
            }
        ],
        model="gpt-3.5-turbo",
    )
    
    return chat_completion.choices[0].message.content

def main():
    model = load_yolo_model()
    image_url = 'https://media.roboflow.com/notebooks/examples/dog.jpeg'
    result = perform_object_detection(model, image_url)
    count_class = count_detected_classes(result)
    classes_string = format_class_counts(count_class, Yolo_value)
    gpt3_response = interact_with_gpt3(classes_string)
    
    print(gpt3_response)

if __name__ == "__main__":
    main()
