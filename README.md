# 2024 PROMETHEUS AI Hackathon

#### • Skills
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white"> <img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Python&logoColor=white"> 

## 0. 모델 선정 배경
### -1) YOLO
<br/>

>   Vision AI분야의 모델로 YOLOv8을 선택한 이유는 3가지가 있습니다.
>
> 
>>    1. 오픈 소스 모델: YOLOv8은 오픈 라이브러리로, 패키지만 설치한다면 누구나 무료로 사용할 수 있습니다.
>>
>>    2. 모델의 접근성: Fine tuning 과정이 쉽고 간편하여 모델을 본 서비스의 목적대로 튜닝할 수 있습니다.
>>
>>    3. 모델의 다양성: YOLOv8 모델은 Nano부터 Extra Large까지 모델의 속도와 정확성을 trade - off한 여러 모델이 있어, 목적에 맞게 다양한 모델을 선택할 수 있습니다.  
>
> 
>   위 세 가지 이유로 YOLO모델이 '방구석브리핑'프로젝트에 가장 적합하다 판단되어 사용하게 되었습니다.

<br/>

### -2) GPT-4

<br/>

> GPT는 대표적인 LLM 모델입니다.
>> Vision AI로 탐지한 결과를 고객에게 알려주기 위해서 GPT-4를 사용했습니다.

<br/><br/>

## 1. 모델 학습 과정

> YOLO는 pre-trained model로 학습을 시키지 않고도 사용할 수 있는 모델입니다.
>
> 하지만 저희의 목적에 맞게 쓰기 위해서는 fine tuning 과정을 통해 모델의 출력값을 바꾸어줘야합니다.
>> 
