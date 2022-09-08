from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions

# 去除浏览器识别
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option("detach", True)


def get_abs_path():
    return


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

    driver.find_element(By.XPATH,
                        '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button').click()

    # 处理滑块验证
    # 标签定位滑块id
    span = driver.find_element(By.XPATH,
                               '/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]')

    action = ActionChains(driver)  # 行为链实例化
    action.click_and_hold(span)

    for i in range(10):
        action.move_by_offset(36, 0).perform()  # perform()立即执行动作链操作，move_by_offset(x, y):x水平方向  y竖直方向
        sleep(0.1)

    # 释放行为链
    action.release()
    print(driver.page_source)
    sleep(10)
    print('===' * 50, '\n\n\n\n\n')

    print(driver.page_source)
    driver.quit()
