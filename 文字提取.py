from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='ch') # need to run only once to download and load model into memory
import os
import csv
#读取每张图片，进行文字识别，并保存到csv文件中
root_path = "C:\\Users\\CUGac\\PycharmProjects\\astar\\.venv\\Scripts\\video_detect\\test"
i = 0
save_path = "C:\\Users\\CUGac\\PycharmProjects\\astar\\.venv\\Scripts\\video_detect\\test.csv"
dic = {}
for i in range(1, 100):
    try:
        pic_path = os.path.join(root_path, "{}.jpg".format(i))
        result = ocr.ocr(pic_path)
        # print(result)
        for j in range(20):
            x = result[0][0][1][0]
            dic[i] = x
    except:
        pass

# print(dic)
with open(save_path, 'w', newline='',encoding = 'utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for item in dic:
        writer.writerow([item, dic[item]])

