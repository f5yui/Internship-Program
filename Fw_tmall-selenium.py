"""
浏览器=浏览器内核+可视化界面
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from bs4 import BeautifulSoup

# headless(只用到浏览器的内核部分)
visit_url = 'https://s.taobao.com/search?spm=a230r.1.1998181369.1.5c9148b2FgqiZl&q=%E9%A1%B9%E9%93%BE&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&p4ppushleft=%2C44&tab=all'
save_floder = 'C:/Users/Administrator/Desktop/data'
file_name = 'data.txt'
if not os.path.exists(save_floder):
    os.makedirs(save_floder)
counter = 1
options = Options()
# 启用headless模式
# options.headless = True
driver = webdriver.Chrome(executable_path='driver/chromedriver.exe', options=options)
driver.get(visit_url)


w = input("输入页数")
w = int(w)
for i in range(w):
    # 隐式等待，保证当前访问页面的数据尽量加载完整，再执行后续代码
    driver.implicitly_wait(20)
    scrollTop = 500
    for i in range(8):
        driver.execute_script('var scrollTop=document.documentElement.scrollTop=' + str(scrollTop))
        sleep(5)
        scrollTop += 500
    content = driver.page_source

    doc = BeautifulSoup(content, 'html.parser')
    necklaces = doc.select('#mainsrp-itemlist .J_MouserOnverReq')
    for necklace in necklaces:
        necklace_name = necklace.select('.title a')[0]
        necklace_price = necklace.select('.price')[0]
        necklace_deal_cnt = necklace.select('.deal-cnt')[0]
        shop_name = necklace.select('.shop a')[0]
        shop_location = necklace.select('.location')[0]
        necklace_pic = necklace.select('.pic img')[0].get('src')
        necklace_pic = "http:" + necklace_pic
        with open(os.path.join(save_floder, file_name), 'a', encoding='utf-8') as obj:
            obj.write(str(counter) + '\t' + necklace_name.text.strip(' \n\r\t') + '\t' + necklace_price.text.strip('\n') + '\t' + necklace_deal_cnt.text + '\t' + shop_name.text.strip('\n') + '\t' + shop_location.text + '\t' + necklace_pic + '\n')

        counter += 1
    else:
        print(str(counter - 1) + '条数据')
    search_button = driver.find_element_by_class_name('next')
    search_button.click()
    # 保持当前操作窗口永远是最新打开的
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
else:
    print("完成")
