from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import numpy as np
import cv2

# 去除浏览器识别
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option("detach", True)


def get_abs_path():
    return


def auto_slice(driver,
               bg_img_xpath=None,
               slice_xpath=None,
               save_bg_path=None,
               save_slice_path=None):
    # driver = webdriver.Chrome()

    # 拿到背景图片和滑块的图片链接并下载后加载进来
    bg_img_link = driver.find_element(By.XPATH, bg_img_xpath).get_attribute("src")
    slice_link = driver.find_element(By.XPATH, slice_xpath).get_attribute("src")
    bg_img = load_link_img(bg_img_link, save_bg_path)
    slice_img = load_link_img(slice_link, save_slice_path)
    # 获取偏移量
    result = cv2.matchTemplate(bg_img, slice_img, cv2.TM_CCOEFF_NORMED)
    # 查找slice_img在bg_img中的位置，返回result是一个矩阵，是每个点的匹配结果
    x, y = np.unravel_index(result.argmax(), result.shape)
    # 获取滑块
    element = driver.find_element(By.XPATH, slice_xpath)
    action = ActionChains(driver)
    action.click_and_hold(on_element=element).perform()
    action.move_to_element_with_offset(to_element=element, xoffset=y, yoffset=0).perform()
    action.release(on_element=element).perform()
    sleep(2)


def load_link_img(link, save_img_path):
    from urllib.request import urlopen
    # link = 'https://img-blog.csdnimg.cn/20191124184305512.png'
    with urlopen(link) as f:
        data = f.read()
    with open(save_img_path, 'wb') as p:
        p.write(data)
    img = cv2.imread(save_img_path, 0)
    return img


def fresh_web_page():
    driver = webdriver.Chrome(options=option)  # mac M1
    # driver.get("https://github.com/JimouChen")  # 刷新网址
    url = 'https://zhuanlan.zhihu.com/p/550383738'
    driver.get(url=url)

    try:
        for i in range(100):  # 刷新次数
            driver.refresh()  # 刷新网页
            print(f'[{datetime.now()}]:refresh times: {i + 1}')
            sleep(1.5)
        driver.quit()
        print('over -----')
    except:
        driver.quit()
        print('close driver finished')


def login_zhihu(account='xxx', password='xxx'):
    driver = webdriver.Chrome(options=option)
    url = 'https://www.zhihu.com/signin?next=%2F'
    driver.get(url=url)
    # 点击密码登陆
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[1]/div[2]').click()

    uname = driver.find_element(By.NAME, 'username')  # 或者用下面这个，一样的
    # uname = driver.find_element(By.XPATH,
    #                             '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div/label/input')
    uname.clear()
    uname.send_keys(account)
    psw = driver.find_element(By.NAME, 'password')
    psw.clear()
    psw.send_keys(password)
    # 输入用户名和密码后点登陆
    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button').click()

    # 处理滑块验证
    bg_img_xpath = '',
    slice_xpath = '',
    save_bg_path = '',
    save_slice_path = ''
    auto_slice(driver,
               bg_img_xpath,
               slice_xpath,
               save_bg_path,
               save_slice_path)

    print(driver.page_source)
    driver.quit()
