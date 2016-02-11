import requests, re, shutil, os

threadUrl = ""
source = ""
TARGET = r"D:\Pictures\imageDumps"

def main(TARGET):
    threadUrl = input("URL: ")
    folder = input("folder name: ")
    TARGET += ('\\' + folder)
    source = requests.get(threadUrl).content.decode()
    tags = re.findall('File:.*?<a[^<>]*href="//(.*?)".*?>(.*?)</a>', source)
    if not os.path.exists(TARGET):
        os.makedirs(TARGET)

    for item in tags:
        with open(TARGET + '\\' + item[1], 'wb') as file:
            shutil.copyfileobj(requests.get("http://"+item[0], stream=True).raw, file)
        print(item[0])
        print(item[1])

main(TARGET)
