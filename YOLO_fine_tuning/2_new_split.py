import cv2
import os
import json
from glob import glob
import threading
from tqdm import tqdm

root = "C:/Users/sunxo/Study/BIS/data"
video_path_list = glob(f"{root}/movie/**/*.mp4", recursive=True)
os.makedirs(f"{root}/split_image", exist_ok=True)

def worker(video_path_list, tid):
    with tqdm(total=len(video_path_list), ncols=80, position=tid) as pbar:
        for video_path in video_path_list:
            label_path = os.path.join(
                root,
                "JSON",
                os.path.basename(os.path.dirname(video_path)),
                f"{os.path.basename(video_path.replace('.mp4', ''))}.json",
            )
            with open(label_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            frame_list = [int(i["frame"]) for i in data]
            video = cv2.VideoCapture(video_path)
            while video.isOpened():
                ret, image = video.read()
                if not ret:
                    break
                current_frame = int(video.get(1))
                if current_frame in frame_list:
                    file_name = os.path.join(
                        root,
                        "split_image",
                        os.path.basename(os.path.dirname(video_path)),
                        f"{os.path.basename(video_path.replace('.mp4', ''))}_{current_frame}.jpg",
                    )
                    file_name = file_name.replace("\\", "/")
                    os.makedirs(os.path.dirname(file_name),exist_ok=True)
                    cv2.imwrite(file_name, image)
            #video.release()
            pbar.update(1)

num_threads = 1
threads = []
for tid in range(num_threads):
    start_index = tid * len(video_path_list) // num_threads
    end_index = (tid + 1) * len(video_path_list) // num_threads
    thread = threading.Thread(
        target=worker,
        args=(
            video_path_list[start_index:end_index],
            tid,
        ),
    )
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()