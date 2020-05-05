import requests
from bs4 import BeautifulSoup


url = 'https://movie.douban.com/top250'
with open('douban.txt','w',encoding='utf-8') as f:
    while url:
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

        r=requests.get(url,headers=headers)
        soup = BeautifulSoup(r.text,'lxml')

        for each in soup.find_all('div',class_='info'):
            img_url = each.previous_sibling.previous_sibling.a.img['src']
            title=each.find('div',class_='hd').get_text(strip=True).replace('\xa0','')
            actor = list(each.find('p',class_='').strings)[0].strip().replace('\xa0','')
            #将生成器list化后索引，strip()去除两边空格再用空字符替换&nbsp
            type_ = list(each.find('p',class_='').strings)[1].strip().replace('\xa0','')
            score = each.find('div',class_='star').get_text('/',strip=True)
            if each.find('span',class_='inq'):#注意有部电影没有总结，也就没有<span class="inq">标签这里用if检测一下防止None使用string方法报错
                quote = each.find('span', class_='inq').string
            else:
                quote = '没有总结哦'
            f.writelines([img_url, title, actor, type_, score, quote])
            f.write('\r\n')
            try:#到最后一页时没有下一页按钮，会报TypeError，这时用try语句让url=None使while循环停止
                url = 'https://movie.douban.com/top250' + soup.find('span',class_='next').a['href']
            except TypeError:
                url = None
print("已完成")