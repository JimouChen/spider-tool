# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
# from selenium.webdriver import chromium
from urllib.request import urlretrieve

import ddddocr
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import time, sleep
import re
from bs4 import BeautifulSoup
from zhihu_params import *

click_js = 'arguments[0].click();'


class ZhiHuCrawler:
    @staticmethod
    def login(driver: WebDriver, uname, psw):
        driver.get(login_url)
        sleep(1)
        login_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[1]/div[2]'
        choose_btn = driver.find_element_by_xpath(login_xpath)
        driver.execute_script(click_js, choose_btn)
        sleep(1)
        uname_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div/label/input'
        psw_xpath = '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[3]/div/label'
        driver.find_element_by_xpath(uname_xpath).send_keys(uname)
        driver.find_element_by_xpath(psw_xpath).send_keys(psw)
        login_btn = driver.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button')
        driver.execute_script(click_js, login_btn)
        sleep(2)
        # 进入滑动滑块页面
        driver = ZhiHuCrawler.handle_move_block(driver)
        return driver

    @staticmethod
    def handle_move_block(driver: WebDriver):
        cur_html = driver.page_source
        soup = BeautifulSoup(cur_html, 'lxml')
        background_link = soup.find('img', {'class': 'yidun_bg-img'}).attrs['src']
        target_link = soup.find('img', {'class': 'yidun_jigsaw'}).attrs['src']
        VerityUtils.download_web_img(background_link, background_img_path)
        VerityUtils.download_web_img(target_link, target_img_path)
        sleep(1)
        loc = VerityUtils.get_match_slice_loc(target_img_path, background_img_path)
        # move_dist = (loc['target'][0] + loc['target'][2]) / 2
        move_dist = loc['target'][0] - 45
        target_xpath = '//html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[2]'
        # 找到滑块位置
        target_btn = driver.find_element_by_xpath(target_xpath)
        sleep(2)
        ActionChains(driver).drag_and_drop_by_offset(target_btn, move_dist, 0).perform()
        sleep(3)
        return driver

    @staticmethod
    def crawl(driver: WebDriver, url):
        driver.get(url)
        sleep(1)
        print(driver.title)
        close_xpath = '/html/body/div[5]/div/div/div/div[2]/button'
        close_btn = driver.find_element_by_xpath(close_xpath)
        sleep(1)
        driver.execute_script(click_js, close_btn)
        sleep(1)


class VerityUtils:
    @staticmethod
    def download_web_img(img_url, file_path):
        urlretrieve(img_url, file_path)

    @staticmethod
    def get_match_slice_loc(target_img, background_img):
        det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        with open(target_img, 'rb') as f:
            target_bytes = f.read()
        with open(background_img, 'rb') as f:
            background_bytes = f.read()
        location = det.slide_match(target_bytes, background_bytes, simple_target=True)
        print(location)
        return location
