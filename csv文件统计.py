import csv

# 逐行读取，并按照逗号进行分割
path = r"C:\Users\CUGac\PycharmProjects\astar\.venv\Scripts\video_detect\test.csv"
# 统计某个文字出现次数
dic = {}
with open(path, encoding='utf-8') as f:
    reader = csv.reader(f)
    for id, item in reader:
        print(id,item)
        # 统计某个文字出现次数
        if item in dic:
            dic[item] += 1
        else:
            dic[item] = 1
print(dic)