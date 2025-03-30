import os
import random
import time

from DrissionPage import Chromium, ChromiumOptions
from dotenv import load_dotenv

load_dotenv()


def human_like_input(element, text):
    """模拟人类输入行为，包含变速输入、偶尔的错误和修正"""
    # 清空输入框
    element.clear()

    typed_text = ""
    for char in text:
        # 随机决定是否"犯错"(大约5%的概率)
        if random.random() < 0.05 and len(typed_text) > 0:
            # 输入错误字符
            wrong_char = chr(ord(char) + random.randint(1, 5))
            element.input(wrong_char)
            typed_text += wrong_char

            # 等待一小段时间后发现"错误"
            time.sleep(random.uniform(0.3, 0.7))

            # 删除错误字符
            element.input('\b')
            typed_text = typed_text[:-1]
            time.sleep(random.uniform(0.2, 0.5))

        # 输入正确字符
        element.input(char)
        typed_text += char

        # 随机间隔时间，模拟打字速度变化
        time.sleep(random.uniform(0.05, 0.25))

    # 输入完成后可能的短暂停顿
    time.sleep(random.uniform(0.5, 1.2))


if __name__ == '__main__':
    # browser = Chromium(ChromiumOptions().headless())
    browser = Chromium()
    tab = browser.latest_tab
    tab.get(
        'https://account.xiaomi.com/fe/service/login/password?sid=miui_vip&qs=%253Fcallback%253Dhttps%25253A%25252F%25252Fapi.vip.miui.com%25252Fsts%25253Fsign%25253DebkFH%2525252BMQmjxjfKc2NjnX3gE8r20%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi.vip.miui.com%2525252Fpage%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb.vip.miui.com%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FboardLive%252525253Fapp_version%252525253Ddev.20051%25252526time%2525253D1743342077662%2526sid%253Dmiui_vip&callback=https%3A%2F%2Fapi.vip.miui.com%2Fsts%3Fsign%3DebkFH%252BMQmjxjfKc2NjnX3gE8r20%253D%26followup%3Dhttps%253A%252F%252Fapi.vip.miui.com%252Fpage%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb.vip.miui.com%25252Fpage%25252Finfo%25252Fmio%25252Fmio%25252FboardLive%25253Fapp_version%25253Ddev.20051%2526time%253D1743342077662&_sign=nvp5AxUt9LpCUk3g58NC07exdZU%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=&_locale=zh_CN')

    account = os.getenv('ACCOUNT')
    password = os.getenv('PASSWORD')
    tab.ele('@@name=account@@class=mi-input__input').input(account)
    tab.ele('@@name=password@@class=mi-input__input').input(password)

    # 同意协议
    tab.ele('@@type=checkbox@@class=ant-checkbox-input').click()
    # 点击登录
    tab.ele('@@type=submit@@class=mi-button mi-button--primary mi-button--fullwidth').click()

    tab.wait.load_start()

    # tab.wait(5)
    # tab.close()

    # # 关闭浏览器
    # browser.quit()
