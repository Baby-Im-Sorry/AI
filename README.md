방구석 브리핑_AI
========================

## 모델 선정 배경
### YOLO

Vision AI 모델로 YOLOv8n을 선택한 이유는 3가지가 있습니다.

1. 오픈 소스 모델: YOLOv8은 오픈 라이브러리로, 패키지만 설치한다면 누구나 무료로 사용할 수 있습니다.
2. 모델의 접근성: Fine tuning 과정이 쉽고 간편하여 모델을 본 서비스의 목적대로 튜닝할 수 있습니다.
3. 모델의 다양성: YOLOv8 모델은 Nano부터 Extra Large까지 모델의 속도와 정확성을 trade - off한 여러 모델이 있기에 목적에 맞는 다양한 모델을 선택할 수 있습니다.  

위 세 가지 이유로 YOLO모델이 '방구석브리핑' 프로젝트에 가장 적합하다 판단되어 사용했습니다.

### GPT-4

GPT는 대표적인 LLM 모델입니다. Vision AI로 탐지한 결과를 고객에게 알려주기 위해서 GPT-4를 사용했습니다.

## 모델 학습 과정

YOLO는 pre-trained model로, 학습을 시키지 않고도 사용할 수 있는 모델입니다.
그러나 이번 프로젝트에서는 Fine tuning을 통해 서비스의 목적에 맞게 출력값을 바꿔줘야 합니다.

1. AI-hub에서 학습에 필요한 Mp4, XML형태의 데이터(무인점포 CCTV) 취득
2. 기존의 XML파일을 JSON 형태로 변환
3. mp4파일을 JSON을 참고하여 JPG형태로 변환
4. JSON을 YOLO형식에 맞게 정규화 및 라벨링 후 txt로 변환
5. yaml 파일 작성 및 trn, val, tst split
6. YOLO fine tuning 실시

## 모델 예측 및 자연어 생성

1. Fine tuning된 YOLO 모델은 실시간 영상에서 Object detection후 그 결과값을 GPT-4에게 전달합니다.
2. 그 후 GPT-4가 고객에게 브리핑할 자연어 캡션을 생성합니다.
