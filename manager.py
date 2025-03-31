import json
import os
from typing import Dict, List, Optional, Any


class CookiesManager:
    """
    Cookie管理器类：用于持久化存储、读取和更新cookie
    """

    def __init__(self, storage_path: str = "cookies.json"):
        """
        初始化Cookie管理器

        参数:
            storage_path: cookie存储的文件路径，默认为当前目录下的cookies.json
        """
        self.storage_path = storage_path
        self.cookies = self._load_cookies()

    def _load_cookies(self) -> List[Dict[str, str]]:
        """
        从存储文件加载cookie

        返回:
            包含所有cookie的列表
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"警告: {self.storage_path}文件解析失败，将创建新的cookie存储")
                return []
        return []

    def _save_cookies(self) -> None:
        """
        将cookies保存到存储文件
        """
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.cookies, ensure_ascii=False, indent=4))

    def add_cookie(self, cookie: Dict[str, str]) -> None:
        """
        添加单个cookie

        参数:
            cookie: 包含cookie信息的字典，需要包含name, value和domain字段
        """
        if not all(key in cookie for key in ['name', 'value', 'domain']):
            raise ValueError("cookie必须包含'name', 'value'和'domain'字段")

        # 检查是否已存在相同name和domain的cookie，如果存在则更新
        self.update_cookie(cookie)

    def add_cookies(self, cookies: List[Dict[str, str]]) -> None:
        """
        批量添加多个cookie

        参数:
            cookies: 包含多个cookie字典的列表
        """
        for cookie in cookies:
            self.add_cookie(cookie)

    def get_cookie(self, name: str, domain: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        获取指定的cookie

        参数:
            name: cookie的名称
            domain: cookie的域名（可选），如果不指定则只按name匹配

        返回:
            找到的cookie字典，如果未找到则返回None
        """
        for cookie in self.cookies:
            if cookie['name'] == name:
                if domain is None or cookie['domain'] == domain:
                    return cookie
        return None

    def get_cookies_by_domain(self, domain: str) -> List[Dict[str, str]]:
        """
        获取指定域名的所有cookie

        参数:
            domain: 要查询的域名

        返回:
            包含指定域名cookie的列表
        """
        return [cookie for cookie in self.cookies if cookie['domain'] == domain]

    def get_all_cookies(self) -> List[Dict[str, str]]:
        """
        获取所有cookie

        返回:
            包含所有cookie的列表
        """
        return self.cookies

    def update_cookie(self, cookie: Dict[str, str]) -> bool:
        """
        更新cookie，如果不存在则添加

        参数:
            cookie: 包含cookie信息的字典，需要包含name, value和domain字段

        返回:
            如果更新了现有cookie则返回True，如果添加了新cookie则返回False
        """
        if not all(key in cookie for key in ['name', 'value', 'domain']):
            raise ValueError("cookie必须包含'name', 'value'和'domain'字段")

        for i, existing_cookie in enumerate(self.cookies):
            if (existing_cookie['name'] == cookie['name'] and
                    existing_cookie['domain'] == cookie['domain']):
                # 更新现有cookie
                self.cookies[i] = cookie
                self._save_cookies()
                return True

        # 如果没有找到匹配的cookie，则添加新cookie
        self.cookies.append(cookie)
        self._save_cookies()
        return False

    def delete_cookie(self, name: str, domain: Optional[str] = None) -> bool:
        """
        删除指定的cookie

        参数:
            name: cookie的名称
            domain: cookie的域名（可选），如果不指定则只按name匹配

        返回:
            如果成功删除则返回True，否则返回False
        """
        initial_length = len(self.cookies)

        if domain is None:
            self.cookies = [cookie for cookie in self.cookies if c['name'] != name]
        else:
            self.cookies = [cookie for cookie in self.cookies if not (c['name'] == name and c['domain'] == domain)]

        if len(self.cookies) < initial_length:
            self._save_cookies()
            return True
        return False

    def clear_cookies(self, domain: Optional[str] = None) -> int:
        """
        清除所有cookie或指定域名的cookie

        参数:
            domain: 要清除的域名（可选），如果不指定则清除所有cookie

        返回:
            清除的cookie数量
        """
        initial_length = len(self.cookies)

        if domain is None:
            self.cookies = []
        else:
            self.cookies = [cookie for cookie in self.cookies if c['domain'] != domain]

        removed_count = initial_length - len(self.cookies)
        if removed_count > 0:
            self._save_cookies()
        return removed_count

    def to_dict_format(self) -> Dict[str, Dict[str, Any]]:
        """
        将cookies转换为字典格式，便于某些库使用

        返回:
            以cookie名称为键的字典
        """
        result = {}
        for cookie in self.cookies:
            result[cookie['name']] = {
                'value': cookie['value'],
                'domain': cookie['domain']
            }
        return result


# 使用示例
if __name__ == "__main__":
    # 创建cookie管理器实例
    manager = CookiesManager("miui_cookies.json")

    # 添加示例cookie
    example_cookies = [
        {
            'name': 'miui_vip_ph',
            'value': 'O0ZqH1f/qdg==',
            'domain': '.vip.miui.com'
        },
        {
            'name': 'miui_vip_slh',
            'value': '6OqIvmcLagdao=',
            'domain': '.vip.miui.com'
        },
        {
            'name': 'cUserId',
            'value': 'iOLgSRPkeavcmeMwnZY',
            'domain': '.miui.com'
        },
        {
            'name': 'miui_vip_serviceToken',
            'value': 'IA2BKMwRB8IbWsj7Ts=',
            'domain': '.vip.miui.com'
        }
    ]

    manager.add_cookies(example_cookies)

    # 获取特定域名的所有cookie
    vip_cookies = manager.get_cookies_by_domain('.vip.miui.com')
    print("vip.miui.com的所有cookie:")
    for c in vip_cookies:
        print(f"  {c['name']}: {c['value']}")

    # 更新某个cookie
    manager.update_cookie({
        'name': 'cUserId',
        'value': 'NEW_VALUE_HERE',
        'domain': '.miui.com'
    })

    # 验证更新结果
    updated_cookie = manager.get_cookie('cUserId')
    print(f"\n更新后的cUserId: {updated_cookie['value']}")

    # 打印所有cookie
    print("\n所有保存的cookie:")
    for c in manager.get_all_cookies():
        print(f"  {c['name']} ({c['domain']}): {c['value']}")
