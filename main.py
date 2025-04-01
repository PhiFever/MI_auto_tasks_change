import os
import random
import time

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage._functions.cookies import CookiesList
from DrissionPage.common import Keys
from DrissionPage._pages.mix_tab import MixTab
from dotenv import load_dotenv
from rich.pretty import pprint

from manager import CookiesManager

load_dotenv()


# 或许可以使用tab.actions.type()来模拟人类输入 https://www.drissionpage.cn/browser_control/actions/#-type
# 定位语法：https://www.drissionpage.cn/browser_control/get_elements/syntax
def human_like_input(current_tab: MixTab, locator: str, input_text: str) -> str:
    """模拟人类输入行为，包含变速输入、偶尔的错误和修正"""
    # 清空输入框
    element = current_tab.ele(locator)
    element.clear()
    # 设置默认犯错概率
    default_error_rate = 0.05

    typed_text = ""
    for char in input_text:
        # 随机决定是否"犯错"(大约5%的概率)
        if random.random() < default_error_rate and len(typed_text) > 0:
            # 输入错误字符
            wrong_char = chr(ord(char) + random.randint(1, 5))
            element.input(wrong_char)
            typed_text += wrong_char

            # 等待一小段时间后发现"错误"
            time.sleep(random.uniform(0.3, 0.7))

            # 删除错误字符
            current_tab.actions.key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE)
            typed_text = typed_text[:-1]
            time.sleep(random.uniform(0.2, 0.5))

        # 输入正确字符
        element.input(char)
        typed_text += char

        # 随机间隔时间，模拟打字速度变化
        time.sleep(random.uniform(0.15, 0.25))  # 调整了最小值，使输入更自然

    # 输入完成后可能的短暂停顿
    time.sleep(random.uniform(0.5, 1.2))

    return typed_text


def login(current_tab: MixTab) -> CookiesList:
    current_tab.get(
        'https://account.xiaomi.com/fe/service/login/password?sid=miui_vip&qs=%253Fcallback%253Dhttps%25253A%25252F%25252Fapi.vip.miui.com%25252Fsts%25253Fsign%25253DebkFH%2525252BMQmjxjfKc2NjnX3gE8r20%2525253D%252526followup%25253Dhttps%2525253A%2525252F%2525252Fapi.vip.miui.com%2525252Fpage%2525252Flogin%2525253FdestUrl%2525253Dhttps%252525253A%252525252F%252525252Fweb.vip.miui.com%252525252Fpage%252525252Finfo%252525252Fmio%252525252Fmio%252525252FboardLive%252525253Fapp_version%252525253Ddev.20051%25252526time%2525253D1743342077662%2526sid%253Dmiui_vip&callback=https%3A%2F%2Fapi.vip.miui.com%2Fsts%3Fsign%3DebkFH%252BMQmjxjfKc2NjnX3gE8r20%253D%26followup%3Dhttps%253A%252F%252Fapi.vip.miui.com%252Fpage%252Flogin%253FdestUrl%253Dhttps%25253A%25252F%25252Fweb.vip.miui.com%25252Fpage%25252Finfo%25252Fmio%25252Fmio%25252FboardLive%25253Fapp_version%25253Ddev.20051%2526time%253D1743342077662&_sign=nvp5AxUt9LpCUk3g58NC07exdZU%3D&serviceParam=%7B%22checkSafePhone%22%3Afalse%2C%22checkSafeAddress%22%3Afalse%2C%22lsrp_score%22%3A0.0%7D&showActiveX=false&theme=&needTheme=false&bizDeviceType=&_locale=zh_CN')
    human_like_input(current_tab, '@@name=account@@class=mi-input__input', os.getenv('ACCOUNT'))
    human_like_input(current_tab, '@@name=password@@class=mi-input__input', os.getenv('PASSWORD'))
    current_tab.wait(random.uniform(0.1, 0.5))
    # 同意协议
    current_tab.ele('@@type=checkbox@@class=ant-checkbox-input').click()
    current_tab.wait(random.uniform(0.1, 0.5))
    # 点击登录
    current_tab.ele('@@type=submit@@class=mi-button mi-button--primary mi-button--fullwidth').click()
    current_tab.wait.load_start()

    return current_tab.cookies()


if __name__ == '__main__':
    # browser = Chromium(ChromiumOptions().headless())
    browser = Chromium()
    tab: MixTab = browser.latest_tab
    cookies_manager = CookiesManager('miui_cookies.json')
    last_cookies = cookies_manager.get_all_cookies()
    if not last_cookies:
        cookies = login(tab)
        cookies_manager.add_cookies(cookies)
    else:
        for cookie in last_cookies:
            tab.set.cookies(cookie)
        tab.get('https://web.vip.miui.com/page/info/mio/mio/boardLive')

    tab.wait.load_start()
    print('登录成功')

    # 随便点一个贴子，浏览15秒
    tab.actions.move_to(ele_or_loc=(1100, 725), duration=0.5).click()
    tab.wait(15)

    # 签到
    # 关闭浏览器
    browser.quit()
