방구석 브리핑_AI
========================

## 모델 선정 배경
### YOLO

The reason for choosing YOLOv8n as the Vision AI model can be summarized into three points.

* **Open-source Model**: YOLOv8n is an open-source library, allowing anyone to use it for free with just the installation of the package.
* **Model Accessibility**: The fine-tuning process is easy and straightforward, enabling tuning of the model according to the specific purposes of the service.
* **Model Diversity**: YOLOv8n offers a variety of models that trade off speed and accuracy, ranging from Nano to Extra Large, providing the flexibility to choose models based on the project's goals.

For these three reasons, YOLO model was deemed most suitable for the 'Home Briefing' project.


### GPT-4

GPT is a prominent LLM model. To communicate the results of Vision AI detection to customers, the **GPT-4-preview model** was employed.



## Model Training Process

YOLO is a pre-trained model that can be used without additional training. However, for this project, fine-tuning is required to customize the output for the service's objectives.

| Step | Description |
|------|-------------|
| 1    | Acquire Mp4 and XML data (from unmanned store CCTV) necessary for training from AI-hub. |
| 2    | Convert existing XML files into JSON format. |
| 3    | Convert Mp4 files into JPG format according to the JSON reference. |
| 4    | Normalize JSON to YOLO format, perform labeling, and convert to txt. |
| 5    | Write a yaml file and split into training, validation, and test sets. |
| 6    | Conduct YOLO fine-tuning. |


## Model Prediction and Natural Language Generation


* The fine-tuned YOLO model performs real-time object detection in video, and the results are then communicated to GPT-4.
* GPT-4 generates natural language captions for briefing customers based on the received results.
