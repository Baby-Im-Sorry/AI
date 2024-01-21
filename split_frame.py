import cv2
import os
import json
import glob

# JSON 파일 불러오기
def load_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            values_list = [list(obj.values()) for obj in data]
            return values_list
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in {file_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# 원하는 프레임 추출
def extract_frames(values_list):
    try:
        frame_list = [int(item[0]) for item in values_list]
        return frame_list
    except ValueError:
        print("Error: Failed to convert frame values to integers.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# 비디오 불러오기
def load_video(file_path):
    try:
        video = cv2.VideoCapture(file_path)
        if not video.isOpened():
            raise Exception("Unable to open the video file.")
        return video
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# 비디오 속성 값 추출
def extract_video_properties(video):
    try:
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video.get(cv2.CAP_PROP_FPS)
        return length, width, height, fps
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
# 이미지 파일 저장소 생성
def create_image_directory(file_path):
    try:
        directory_path = "./data/images/" + file_path[7:-4]
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Directory created successfully. Path: {directory_path}")
        else:
            print("Directory already exists. Path:", directory_path)
    except OSError as e:
        print(f"Error: Creating directory. {str(e)}")

# 프레임 추출 및 이미지 저장
def extract_and_save_frames(video, frame_list, directory_path, file_prefix):
    count = 0

    try:
        while video.isOpened():
            ret, image = video.read()

            if not ret:
                break

            current_frame = int(video.get(1))

            if current_frame in frame_list:
                filename = os.path.join(directory_path, f"{file_prefix}_{frame_list[count]}.jpg")
                cv2.imwrite(filename, image)
                print(f'Saved frame number: {frame_list[count]}, filename: {filename}')
                count += 1

    except Exception as e:
        print(f'An error occurred: {str(e)}')
    finally:
        video.release()

def process_directory(json_directory_path, video_directory_path):
    # JSON 파일 처리
    json_files = glob.glob(os.path.join(json_directory_path, '*.json'))
    for json_file_path in json_files:
        values_list = load_json_file(json_file_path)
        frame_list = extract_frames(values_list)

        # 비디오 파일 처리
        video_base_name = os.path.splitext(os.path.basename(json_file_path))[0]
        video_file_path = os.path.join(video_directory_path, f"{video_base_name}.mp4")
        loaded_video = load_video(video_file_path)
        
        if loaded_video:
            # 비디오 속성 추출
            video_length, _, _, _ = extract_video_properties(loaded_video)

            # 디렉토리 생성
            create_image_directory(video_file_path)

            # 프레임을 이미지로 추출하고 저장
            extract_and_save_frames(loaded_video, frame_list, f"./data/images/{video_base_name}", video_base_name)

# 사용 예시
json_directory_path = './data/JSON/방화'
video_directory_path = 'D:/238-2.실내(편의점, 매장) 사람 이상행동 데이터/01-1.정식개방데이터/Training/01.원천데이터/방화'
process_directory(json_directory_path, video_directory_path)
