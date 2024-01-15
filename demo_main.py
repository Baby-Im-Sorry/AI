import os
import cv2
import moviepy.video.io.ImageSequenceClip
from google.cloud import vision
import requests
from requests.auth import HTTPBasicAuth
from tqdm import tqdm
from glob import glob
import threading
import time

"""

def split_video(filepath):
    vidcap = cv2.VideoCapture(filepath)
    count = 0
    while vidcap.isOpened():
        _, image = vidcap.read()
        if image is None:
            break
        cv2.imwrite(
            f"./{video_name}/%d.jpg" % count,
            image,
        )
        count += 1
    vidcap.release()
    frames = glob(f"./{video_name}/*.jpg")
    # images = images[:25]
    return frames


def get_speed(image):
    img = cv2.imread(image)
    # google vision api
    crop_img = img[1010:1080, 0:809]
    _, encoded_img = cv2.imencode(".jpg", crop_img)
    content = encoded_img.tobytes()
    im = vision.Image(content=content)
    response = gcp_client.text_detection(image=im)
    texts = response.text_annotations
    speed = texts[0].description.replace("\n", " ").split(" ")[2]
    return speed
"""


def get_bbox(image, endpoint, speed, inferenced_frames):
    # suite model endpoint
    new_image = open(image, "rb").read()
    response = requests.post(
        url=endpoint,
        auth=HTTPBasicAuth("model-service", "qdUwmDqFDr96ICnonQlqN66tib6mfAa05G67F9Gg"),
        headers={"Content-Type": "image/jpeg"},
        data=new_image,
    )
    # img = cv2.imread(image)
    # data = response.json()
    # try:
    #     humans = []
    #     phones = []
    #     for obj in data["objects"]:
    #         if obj["class"] == "human":
    #             human = data["objects"][0]["box"]
    #             humans.append(human)
    #         elif obj["class"] == "phone":
    #             phone = data["objects"][1]["box"]
    #             phones.append(phone)
    #     for i in humans:
    #         img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), (128, 128, 128), 3)

    #     for j in phones:
    #         if float(speed) > 1.5:
    #             img = cv2.rectangle(img, (j[0], j[1]), (j[2], j[3]), (0, 0, 255), 3)
    #         else:
    #             img = cv2.rectangle(img, (j[0], j[1]), (j[2], j[3]), (0, 255, 0), 3)
    # except:
    #     print("no inference", image)
    #     # img = cv2.imread(image)
    # inferenced_frames.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # cv2.imwrite(
    #     f"./{video_name}/result/" + os.path.basename(image),
    #     img,
    # )
    return inferenced_frames


def worker(frames, endpoint, tid):
    with tqdm(total=len(frames), position=tid, ncols=80, desc=f"{tid} tid") as pbar:
        inferenced_frames = []
        for frame in frames:
            # speed = get_speed(frame)
            speed = 15
            inferenced_frames = get_bbox(frame, endpoint, speed, inferenced_frames)
            pbar.update(1)


def get_inference(frames, endpoint, NUM_THREADS):
    start = time.time()
    threads = []
    for tid in range(NUM_THREADS):
        start_index = tid * len(frames) // NUM_THREADS
        end_index = (tid + 1) * len(frames) // NUM_THREADS
        thread = threading.Thread(
            target=worker,
            args=(
                frames[start_index:end_index],
                endpoint,
                tid,
            ),
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    end = time.time()
    total_time = end - start
    return inferenced_frames, total_time


"""
def make_video(inferenced_frames, video_name):
    FPS = 25
    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(
        inferenced_frames, fps=FPS
    )
    clip.write_videofile(f"{video_name}_inside_detect.mp4")
    result = {}
"""


def main(filepath, endpoint, NUM_THREADS):
    video_name = os.path.basename(filepath).replace("_A.mp4", "")
    global inferenced_frames
    inferenced_frames = []

    # split video
    # frames = split_video(filepath)
    frames = glob(f"./{video_name}/*.jpg")[:100]
    # get inference (multi-threading)
    inferenced_frames, total_time = get_inference(frames, endpoint, NUM_THREADS)
    with open("time.txt", "a", encoding="utf-8") as f:
        f.write(f"{NUM_THREADS} : {total_time}\n")
    # make video
    # make_video(inferenced_frames, video_name)


if __name__ == "__main__":
    ####################
    filepath = "D:/다운로드/20231115194152_0060_A.mp4"
    ####################
    endpoint = "https://suite-endpoint-api-apne2.superb-ai.com/endpoints/f67dc481-2b9e-4127-a352-5cea472b0d3e/inference"

    # inferenced_frames = []
    # credential_path = os.path.join("./gcp-key.json")
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path
    # gcp_client = vision.ImageAnnotatorClient()
    video_name = os.path.basename(filepath).replace("_A.mp4", "")
    # for i in [1, 2, 4, 8]:
    #     NUM_THREADS = i
    #     main(filepath, endpoint, NUM_THREADS)
    NUM_THREADS = 2
    main(filepath, endpoint, NUM_THREADS)
    # os.makedirs(f"./{video_name}", exist_ok=True)
    # os.makedirs(f"./{video_name}/result", exist_ok=True)
    # images = glob(f"./{video_name}/*.jpg")
    # images = images[:25]

    # inferenced_frames = glob(f"./{video_name}/result/*.jpg")
    # inferenced_frames = sorted(
    #     inferenced_frames, key=lambda x: int(os.path.basename(x).split(".")[0])
    # )
    # FPS = 25
    # clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(inferenced_frames, fps=FPS)
    # clip.write_videofile(f"{video_name}_inside_detect.mp4")
