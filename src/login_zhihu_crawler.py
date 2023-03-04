# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from time import sleep
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from playwright.sync_api import Page, sync_playwright, Playwright
import ddddocr

url = 'https://www.zhihu.com/signin?next=%2F'
fresh_url = 'https://zhuanlan.zhihu.com/p/xxxxx' # target url to crawl
target_img_path = './target.jpg'
background_img_path = './background.jpg'


def download_web_img(img_url, file_path):
    urlretrieve(img_url, file_path)


def get_match_slice_loc(target_img, background_img):
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open(target_img, 'rb') as f:
        target_bytes = f.read()
    with open(background_img, 'rb') as f:
        background_bytes = f.read()
    location = det.slide_match(target_bytes, background_bytes, simple_target=True)
    print(location)
    return location


def login_zhihu(page: Page, uname, psw):
    login_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[1]/div[2]'
    page.goto(url)
    page.wait_for_timeout(2000)
    print(page.title())
    page.click(login_xpath)
    page.wait_for_timeout(1000)
    uname_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div/label/input'
    psw_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[3]/div/label'
    page.locator(uname_xpath).fill(uname)
    page.locator(psw_xpath).fill(psw)
    page.wait_for_timeout(1000)
    page.click('//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button')
    page.wait_for_timeout(1000)
    cur_html = page.content()
    soup = BeautifulSoup(cur_html, 'lxml')
    background_link = soup.find('img', {'class': 'yidun_bg-img'}).attrs['src']
    target_link = soup.find('img', {'class': 'yidun_jigsaw'}).attrs['src']
    download_web_img(background_link, background_img_path)
    download_web_img(target_link, target_img_path)
    sleep(1)
    loc = get_match_slice_loc(target_img_path, background_img_path)
    move_dist = (loc['target'][0] + loc['target'][2]) / 2
    target_xpath = '//html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]'
    # 找到滑块位置
    target_btn = page.locator(target_xpath)
    box = target_btn.bounding_box()
    # 鼠标放到滑块中心
    page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    page.mouse.down()
    page.mouse.move(box['x'] + box['width'] / 4 + move_dist, box['y'] + box['height'] / 2)
    page.wait_for_timeout(1000)
    page.mouse.up()
    page.wait_for_timeout(8000)
    print(page.title())
    
    page.goto(fresh_url)
    page.wait_for_timeout(2000)
    for i in range(10):
        page.goto(fresh_url)
        page.wait_for_timeout(500)
    print(page.title())


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser = sp.firefox.launch(headless=False,
                                    chromium_sandbox=False)
        context = browser.new_context()
        page = context.new_page()
        login_zhihu(page, 'your username/phone', 'your password')

        context.close()
        browser.close()
