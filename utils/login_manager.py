import json
import os

class LoginManager:
    def __init__(self, cache_path='login_cache.json'):
        data_dir = os.path.join(os.getcwd(), 'data')
        self.cache_path = os.path.join(data_dir, cache_path)
        self.qq = None
        self.bkn = None
        self.cookies = None
        self.cookies_str = None
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.qq = data.get('qq')
                    self.bkn = data.get('bkn')
                    self.cookies = data.get('cookies')
                    self.cookies_str = data.get('cookies_str')
            except Exception:
                pass

    def save_cache(self):
        data = {
            'qq': self.qq,
            'bkn': self.bkn,
            'cookies': self.cookies,
            'cookies_str': self.cookies_str
        }
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def login(self, login_obj):
        result = await login_obj.login()
        if result and result.get('code') == 0:
            qq_str = result.get('qq')
            if qq_str and isinstance(qq_str, str) and qq_str.startswith('o'):
                self.qq = int(qq_str[1:])
            else:
                self.qq = int(qq_str)
            self.bkn = result.get('bkn')
            self.cookies = result.get('cookies')
            self.cookies_str = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            self.save_cache()
            return True
        return False

    def get_login_info(self):
        return self.qq, self.bkn, self.cookies_str