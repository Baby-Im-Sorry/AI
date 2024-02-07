from ultralytics import YOLO
from multiprocessing import freeze_support
from PIL import Image
import os



if __name__ == '__main__':
    os.environ['KMP_DUPLICATE_LIB_OK']='True'
    
    freeze_support()
    
    model = YOLO("yolov8n.pt")
    model.train(data='./yaml/sun.yaml', epochs=1, workers=8)
    print("모델 학습 완료!")
