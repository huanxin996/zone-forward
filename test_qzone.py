import asyncio
from utils.login_manager import LoginManager
from qzone_api import QzoneApi, QzoneLogin

async def main():
    # 登录QQ空间
    login_manager = LoginManager()
    #:请在这里自行管理你的cookies和g_tk等参数
    #TODO：
    # 模块不会存储登录cookies，请自行管理

    # 实例化API
    qzone = QzoneApi()
    login = QzoneLogin()
    qq, g_tk, cookies_str = login_manager.get_login_info()
    if not (qq and g_tk and cookies_str):
        print("未检测到本地登录缓存，无法自动拉取说说,请先登录QQ空间")
        stats = await login_manager.login(login)
        if stats:
            qq, g_tk, cookies_str = login_manager.get_login_info()
        else:
            print("登录失败，请检查QQ空间登录信息")
            return
    
    await qzone._send_zone(
        target_qq=int(qq),
        content="Hello QZone-API!",
        cookies=cookies_str,
        g_tk=g_tk
    )
    print("发送说说成功!")

if __name__ == "__main__":
    asyncio.run(main())