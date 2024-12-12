import sys, os, time, json
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

weatherCodes = [
    100,
    101,
    102,
    104,
    110,
    112,
    115,
    200,
    201,
    202,
    204,
    210,
    212,
    215,
    300,
    301,
    302,
    303,
    308,
    311,
    313,
    314,
    400,
    411,
    413,
    414,
]

path = os.getcwd()

if not (os.path.isdir(path + "/weatherCodes_Image")):
    print("Create_Directory")
    os.mkdir(path + "/weatherCodes_Image")


print("Start Download")

for id in weatherCodes :
    url = f"https://www.jma.go.jp/bosai/forecast/img/{id}.svg"
    filename_image = os.path.basename(url)
    if not (os.path.exists(path + "/weatherCodes_Image/" + filename_image)):
        print(f"Now_Download_Image: {id}.svg")
        # ダウンロード・保存
        res = requests.get(url)# ダウンロード
        with open(path+ "/weatherCodes_Image/" + filename_image, 'wb') as f:# 保存処理
            f.write(res.content)
        # svgをpngに変換
        #(できないみたいなので、手動でpngに変換してください。svgファイルは消去してかまいません。)
        #drawing = svg2rlg(path + "/weatherCodes_Image/" + filename_image)
        #renderPM.drawToFile(drawing, path + "/weatherCodes_Image/" + str(id) + ".png", fmt="PNG")
        # svgを削除
        #os.remove(path + "/weatherCodes_Image/" + filename_image)
    else:
        print(f"{id}.svg Skip.")
    time.sleep(1)

print("End Download")
