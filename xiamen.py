import lxml
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import openpyxl


def get_html_text(url):
    try:
        h = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }
        r = requests.get(url, headers=h, timeout=3000)
        r.raise_for_status()   # 如果不是200，则引发HTTPError异常
        r.encoding = r.apparent_encoding  # 根据内容去确定编码格式
        return r.text
    except BaseException as e:
        print("出现异常：", e)
        return str(e)


def writefile(file_name, content_str):  # 将数据写入文件
    with open(file_name, "w", encoding='utf-8', ) as f:
        f.write(content_str)
        f.close


def write_excel(file_name, list_content):
    wb = openpyxl.Workbook()  # 新建Excel工作簿
    st = wb.active
    st['A1'] = "厦门11月份天气统计" # 修改为自己的标题
    for key in list_content:
        st.append(key)
    wb.save(file_name)  # 新工作簿的名称


def show_plot(x, y1, y2):
    plt.rcParams['font.sans-serif'] = ['KaiTi']
    plt.title("厦门11月份最高气温和最低气温")  # 设置图的标题
    plt.xlabel("日期")  # x轴标签
    plt.xticks(rotation=270)
    plt.ylabel("温度/℃")  # y轴标签
    plt.plot(x, y1, color="blue", linewidth=2.0, linestyle="--")
    plt.plot(x, y2, color="red", linewidth=2.0, linestyle="--")
    plt.legend(labels=["评分"], loc="best")  # 设置图例
    plt.savefig('天气.png')
    plt.show()  # 展示绘图


if __name__ == '__main__':
    print('开始爬虫')
    url = 'https://www.baidutianqi.com/history/59134-201911.htm'
    html_text = get_html_text(url)   # 获得网页响应
    writefile("data_html.txt", html_text)  # 源码写入文件
    print('开始解析')
    soup = BeautifulSoup(html_text, "lxml")  # 解析源码
    tr = soup.find_all('tr')  # 获得tr属性
    contents = []
    for td in tr:
        context = td.text.strip().split('\n')
        contents.append(context)
    write_excel('weather.xlsx', contents)  # 数据写入excel
    all_str = ''
    for it in contents:
        for j in it:
            all_str += j
        all_str += '\n'
    writefile('weather.csv', all_str)
    date = []
    high = []
    low = []
    for i in contents:
        if i[0] == '日期':
            continue
        date.append(i[0])
        low.append(i[1])
        high.append(i[2])
    show_plot(date, low, high)  # 制作折线图