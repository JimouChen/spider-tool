# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
from playwright.sync_api import Page, sync_playwright, Playwright


class BrowserController:
    @staticmethod
    def load(sp: Playwright):
        browser = sp.chromium.launch(headless=True,
                                     chromium_sandbox=False)
        context = browser.new_context()
        page = context.new_page()

        return browser, context, page

    @staticmethod
    def clear(browser, context):
        context.close()
        browser.close()
