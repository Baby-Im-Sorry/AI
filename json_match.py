from glob import glob
import os
import json

path = "C:/Users/sunxo/Study/BIS/data/JSON"

li = glob(path + "/**/*.json", recursive=True)

print(len(li))
print(li[:5])

for i in li:
    i = i.replace("\\", "/")
    with open(i, "r", encoding="utf-8") as f:
        data = json.load(f)
    for j in data:
        newpath = f"C:/Users/sunxo/Study/BIS/data/JSON1/{i.split('/')[-2]}/{os.path.basename(i).replace('.json', '')}"
        os.makedirs(newpath, exist_ok=True)
        with open(
            f"{newpath}/{os.path.basename(i).replace('.json', '')}_{j['frame']}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(j, f, ensure_ascii=False)
        # break
    # break
