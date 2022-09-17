from time import sleep
from datetime import datetime
import pyautogui
# import tkinter
from PIL import ImageGrab
from PIL import ImageGrab
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import numpy as np
import cv2
from urllib.request import urlopen

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
    print(driver.page_source)
    print('==' * 50, end='\n\n\n')
    return driver


def load_link_img(link, save_img_path):
    if link is None:
        print('图片链接不能为空')
        exit(0)
    # link = 'https://img-blog.csdnimg.cn/20191124184305512.png'

    with urlopen(link) as f:
        data = f.read()
    with open(save_img_path, 'wb') as p:
        p.write(data)
    img = cv2.imread(save_img_path, 0)
    return img


def fresh_web_page(url='https://zhuanlan.zhihu.com/p/551826108'):
    driver = webdriver.Chrome(options=option)  # mac M1
    # driver.get("https://github.com/JimouChen")  # 刷新网址
    # url = 'https://zhuanlan.zhihu.com/p/551826108'
    driver.get(url=url)
    sleep(10)
    driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div[2]/button/svg').click()
    sleep(5)
    print(driver.page_source)
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


def login_zhihu(account='xxx',
                password='xxx'):
    driver = webdriver.Chrome(options=option)
    url = 'zhihu_login_link'
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
    # 手动滑动则不运行auto_slice
    # bg_img_xpath = '/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]'
    # bg_img_xpath = '//img[@class="yidun_bg-img"]'

    # slice_xpath = '/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]'
    # save_bg_path = '../static/img/bg.png'
    # save_slice_path = '../static/img/slice.png'

    # driver = auto_slice(driver,
    #                     bg_img_xpath,
    #                     slice_xpath,
    #                     save_bg_path,
    #                     save_slice_path)

    sleep(10)
    print(driver.page_source)
    # driver.quit()


def login_ipi_mail(uname='xxx',
                   psw='xxx'):
    driver = webdriver.Chrome(options=option)
    url = 'https://mail.ipi-tech.com'
    driver.get(url=url)

    account = driver.find_element(By.NAME, 'qquin')
    account.clear()
    account.send_keys(uname)

    password = driver.find_element(By.XPATH, '//*[@id="pp"]')
    password.click()
    password.send_keys(psw)

    driver.find_element(By.XPATH, '//*[@id="pwd_content"]/div[6]/a/input').click()

    sleep(3)
    driver.find_element(By.XPATH, '//*[@id="folder_1"]').click()
    print(driver.page_source)


def auto_youth_study():
    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support.select import Select
    # from selenium.webdriver.support import expected_conditions as EC
    index_url = 'https://news.cyol.com/gb/channels/vrGlAKDl/index.html'
    driver = webdriver.Chrome(options=option)
    driver.get(url=index_url)

    # courses = driver.find_element(By.XPATH, '/html/body/div[4]/div/ul')
    # print(courses)
    driver.find_element(By.XPATH, '/html/body/div[4]/div/ul/li[1]/a').click()
    sleep(3)

    # 切换到新窗口，要不然操作的是第一个窗口
    list_windows = driver.window_handles
    # print(list_windows)
    driver.switch_to.window(list_windows[1])
    sleep(2)
    # 用1 秒的时间把光标移动到x,y 位置,y竖向向下增加
    pyautogui.moveTo(350, 610, duration=1)
    pyautogui.click(button='left')

    pyautogui.moveTo(350, 580, duration=0.5)
    pyautogui.click(button='left')

    pyautogui.moveTo(350, 640, duration=1)
    pyautogui.click(button='left')

    pyautogui.moveTo(350, 150, duration=0.5)
    pyautogui.click(button='left')
    # 最后点击确定
    pyautogui.click(350, 800, button='left')
    sleep(5)
    # 最后点击开始学习
    pyautogui.click(350, 960, button='left')
    sleep(20)
    driver.quit()


def test_mouse_gui():
    # pyautogui.moveTo(350, 610, duration=1)
    # pyautogui.click(button='left')
    #
    # pyautogui.moveTo(350, 580, duration=0.5)
    # pyautogui.click(button='left')
    #
    # pyautogui.moveTo(350, 640, duration=1)
    # pyautogui.click(button='left')
    #
    # pyautogui.moveTo(350, 150, duration=0.5)
    # pyautogui.click(button='right')

    pyautogui.click(350, 960, button='right')


def test_get_mofan_com_doc():
    driver = webdriver.Chrome(options=option)
    driver.get(url='https://mofanpy.com/tutorials/machine-learning/torch/intro-speed-up-learning')
    words = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[4]/div[1]').text
    print(words)
    driver.quit()
