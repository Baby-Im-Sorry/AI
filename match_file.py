from glob import glob
import os
import shutil
import threading
from tqdm import tqdm


def copy_files(matching_files, tid):
    with tqdm(total=len(matching_files), ncols=80, position=tid) as pbar:
        for i in matching_files:
            try:
                shutil.copy(
                    f"{vid}/{action_dict[int(i.split('_')[2])]}/{i}.mp4",
                    f"D:/무인점포/Training/원천/{action_dict[int(i.split('_')[2])]}/{i}.mp4",
                )
                shutil.copy(
                    f"{label}/{action_dict[int(i.split('_')[2])]}/{i}.xml",
                    f"D:/무인점포/Training/라벨/{action_dict[int(i.split('_')[2])]}/{i}.xml",
                )
            except Exception as e:
                print(e)
                # break
            pbar.update(1)


# def compare_and_copy_matching_files(folder1, folder2, destination):
#     files_folder1 = set([os.path.basename(file) for file in os.listdir(folder1)])
#     files_folder2 = set([os.path.basename(file) for file in os.listdir(folder2)])

#     matching_files = files_folder1.intersection(files_folder2)

#     # 일치하는 파일을 새로운 폴더에 복사
#     for file in matching_files:
#         source_file_path1 = os.path.join(folder1, file)
#         source_file_path2 = os.path.join(folder2, file)
#         new_folder_path = os.path.join(destination, file)  # 새로운 폴더 경로

#         # 새로운 폴더 생성
#         os.makedirs(destination, exist_ok=True)

#         # 파일 복사
#         if os.path.exists(source_file_path1):
#             shutil.copy2(source_file_path1, new_folder_path)  # 첫 번째 폴더의 파일 복사
#         elif os.path.exists(source_file_path2):
#             shutil.copy2(source_file_path2, new_folder_path)  # 두 번째 폴더의 파일 복사

if __name__ == "__main__":
    vid = "D:/238-2.실내(편의점, 매장) 사람 이상행동 데이터/01-1.정식개방데이터/Training/01.원천데이터"
    label = "D:/238-2.실내(편의점, 매장) 사람 이상행동 데이터/01-1.정식개방데이터/Training/02.라벨링데이터"
    vid_list = glob(f"{vid}/**/*.mp4")
    label_list = glob(f"{label}/**/*.xml")

    files_folder1 = set(
        [os.path.basename(file).replace(".mp4", "") for file in vid_list]
    )
    files_folder2 = set(
        [os.path.basename(file).replace(".xml", "") for file in label_list]
    )
    matching_files = list(files_folder1.intersection(files_folder2))
    print(len(matching_files))
    # print(matching_files[:5])

    action_dict = {7: "전도", 8: "파손", 9: "방화", 10: "흡연", 11: "유기", 12: "절도"}

    for i in action_dict.values():
        os.makedirs(f"D:/무인점포/Training/원천/{i}", exist_ok=True)
        os.makedirs(f"D:/무인점포/Training/라벨/{i}", exist_ok=True)

    num_threads = 4
    threads = []
    for tid in range(num_threads):
        start_index = tid * len(matching_files) // num_threads
        end_index = (tid + 1) * len(matching_files) // num_threads
        thread = threading.Thread(
            target=copy_files,
            args=(
                matching_files[start_index:end_index],
                tid,
            ),
        )
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
