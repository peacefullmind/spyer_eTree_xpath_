import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import etree

def getpd(url):
    r = requests.get(url)
    html = r.text
    Selector = etree.HTML(html)

    data = pd.DataFrame(columns=['名称', '类型', '地区', '时长', '上映时间', '评分'])

    for i in range(1, 11):
        list = []
        name = Selector.xpath('//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/a/h2'.format(i))[0].text
        try:
            leixing_all = Selector.xpath(
                '//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/div[1]/button'.format(i))
        except:
            leixing_all = ''
        l = len(leixing_all)

        leixing_out = ''
        temp = []
        try:
            for j in range(1, l + 1):
                leixing = \
                    Selector.xpath(
                        '//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/div[1]/button[{}]/span'.format(i, j))[
                        0].text
                temp.append(leixing)
            leixing_out = ','.join(temp)
        except:
            leixing_out = ' '

        try:
            diqu = Selector.xpath('//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/div[2]/span[1]'.format(i))[
                0].text
        except:
            diqu = ''

        try:
            shichang = Selector.xpath('//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/div[2]/span[3]'.format(i))[
                0].text
        except:
            shichang = ''

        try:
            time = Selector.xpath('//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[2]/div[3]/span'.format(i))[
                0].text.replace('上映', '')
        except:
            time = ' '

        try:
            fen = Selector.xpath('//*[@id="index"]/div[1]/div[1]/div[{}]/div/div/div[3]/p[1]'.format(i))[0].text.strip()
        except:
            fen = ''

        list = [name, leixing_out, diqu, shichang, time, fen]
        data.loc[i - 1] = list

    return data



data = pd.DataFrame(columns=['名称', '类型', '地区', '时长', '上映时间', '评分'])
for i in range(1,11):
    url='https://ssr1.scrape.center/page/{}'.format(i)
    temp=getpd(url)
    data=data.append(temp,ignore_index=True)
    # print(temp)

print(data)
data.to_excel('结果.xlsx')