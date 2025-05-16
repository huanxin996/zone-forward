from utils.bot import TwitterBot
from utils.config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from utils.zone_client import fetch_and_print_self_latest_shuoshuo, login_manager, db
import asyncio
import time

def get_unforwarded_shuoshuo(qq: str):
    """获取本地数据库中未转发的说说"""
    with db._lock:
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        c = conn.cursor()
        c.execute('SELECT id, content FROM shuoshuo WHERE qq = ? AND is_forward = 0', (qq,))
        rows = c.fetchall()
        conn.close()
        return rows

def mark_shuoshuo_forwarded(qq: str, shuoshuo_id: str):
    """标记说说为已转发"""
    with db._lock:
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        c = conn.cursor()
        c.execute('UPDATE shuoshuo SET is_forward = 1 WHERE qq = ? AND id = ?', (qq, shuoshuo_id))
        conn.commit()
        conn.close()

async def forward_to_twitter():
    bot = TwitterBot(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    qq, g_tk, cookies_str = login_manager.get_login_info()
    if not (qq and g_tk and cookies_str):
        print("未检测到本地登录缓存，无法自动拉取说说,请先登录QQ空间")
        stats = await login_manager.login()
        if stats:
            qq, g_tk, cookies_str = login_manager.get_login_info()
        else:
            print("登录失败，请检查QQ空间登录信息")
            return
    # 定期拉取说说
    while True:
        print("开始拉取QQ空间说说...")
        await fetch_and_print_self_latest_shuoshuo(qq, g_tk, cookies_str)
        print("检查未转发说说...")
        unforwarded = get_unforwarded_shuoshuo(str(qq))
        for shuoshuo_id, content_json in unforwarded:
            try:
                import json
                content = json.loads(content_json)
                text = content.get('content', '')
                images = content.get('images', [])
                repost = content.get('repost')
                # 拼接转发内容
                if repost:
                    text += '\n转发内容：' + repost.get('content', '')
                    if repost.get('images'):
                        images += repost['images']
                if images:
                    # 只发第一张图
                    bot.post_text_with_media(text, images[0]['url'])
                else:
                    bot.post_text(text)
                mark_shuoshuo_forwarded(str(qq), shuoshuo_id)
                print(f"已转发说说: {shuoshuo_id}")
            except Exception as e:
                print(f"转发说说失败: {shuoshuo_id}, 错误: {e}")
        print("等待下次拉取...")
        time.sleep(120)  # 每2分钟拉取一次

if __name__ == "__main__":
    asyncio.run(forward_to_twitter())

