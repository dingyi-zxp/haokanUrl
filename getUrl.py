import csv
import re

from bs4 import BeautifulSoup
import requests


# 获取视频链接
def videoUrl(list_url: list) -> list:
    video_url = []

    for url in list_url:
        r = requests.get(url)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        url_script = str(soup.find("script", {"id": "_page_data"}).text)
        url = str(re.findall(r'"playurl":".*","clarityUrl"', url_script)[0])
        video_url.append(url.split("\"")[3])
    return video_url


def selectVideoSearch(search: str, num: int) -> list:
    list_src = []
    list_title = []
    query = {'query': search, 'rn': 10, 'type': 'video', 'pn': 1}
    for i in range(1, num + 1):
        print(i)
        query['pn'] = i
        r = requests.get("https://haokan.baidu.com/web/search/api?", params=query)
        data = r.json()
        # print(data)
        data_list = data['data']['list']
        for src in data_list:
            video_url = src['url']
            list_src.append(video_url)
            list_title.append(src['title'])
    return list_src, list_title


if __name__ == "__main__":
    print("good")
    search = input('请输入想查找的视频：')
    num = int(input('请输入需要多少的视频链接(10 * )'))
    print("-L- 只能获取大概的数量")
    list_url, list_title = selectVideoSearch(search, num)
    video_url = videoUrl(list_url)
    print(list_title)
    print(len(video_url))
    with open('./URLs.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(list_title)
        writer.writerow(video_url)
