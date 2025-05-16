from qzone_api import QzoneApi, QzoneLogin
from utils.local_db import db
from utils.login_manager import LoginManager
import traceback

api = QzoneApi()
login_obj = QzoneLogin()
login_manager = LoginManager()

def parse_me_text(item: dict) -> dict:
    """
    解析说说内容，只保留content、images字段，并支持转发内容
    支持复杂的转发链(多次转发)
    """
    result = {
        "content": item.get("content", ""),
        "images": item.get("images", []) if item.get("images") else []
    }
    
    # 处理转发内容
    if "repost" in item and item["repost"]:
        repost = item["repost"]
        repost_content = {
            "content": repost.get("content", ""),
            "images": repost.get("images", []) if repost.get("images") else []
        }
        
        # 处理深层次转发链 - 在转发内容中也检查是否有转发
        if "repost" in repost and repost["repost"]:
            nested_repost = repost["repost"]
            repost_content["nested_repost"] = {
                "content": nested_repost.get("content", ""),
                "images": nested_repost.get("images", []) if nested_repost.get("images") else []
            }
            
        result["repost"] = repost_content
    
    return result

async def fetch_and_print_self_latest_shuoshuo(qq: int, g_tk: int, cookies: str):
    """拉取自身最新的多条说说并打印其结构内容，并分别整理后存入数据库"""
    try:
        result = await api.get_messages_list(qq, g_tk, cookies, num=5)
        if result and result.get('status') == 'ok' and result.get('data'):
            # 打印精简信息而不是整个result对象
            print(f"成功获取到 {len(result['data'])} 条说说")
            
            for latest in result['data']:
                try:
                    parsed = parse_me_text(latest)
                    print("\n发现说说，整理后内容摘要：")
                    content_preview = parsed.get("content", "")[:50] + "..." if len(parsed.get("content", "")) > 50 else parsed.get("content", "")
                    print(f"内容: {content_preview}")
                    print(f"图片数量: {len(parsed.get('images', []))}")
                    
                    if "repost" in parsed:
                        repost_content = parsed["repost"].get("content", "")[:50] + "..." if len(parsed["repost"].get("content", "")) > 50 else parsed["repost"].get("content", "")
                        print(f"转发内容: {repost_content}")
                        print(f"转发图片数量: {len(parsed['repost'].get('images', []))}")
                        
                        if "nested_repost" in parsed["repost"]:
                            print("包含多层转发内容")
                    
                    shuoshuo_id = latest.get('cur_key')
                    if shuoshuo_id and shuoshuo_id not in db.get_all_ids(str(qq)):
                        db.add_shuoshuo(str(qq), shuoshuo_id, parsed)
                        print(f"✓ 已保存说说: {shuoshuo_id}，等待转发")
                    else:
                        print(f"跳过 - 说说已存在: {shuoshuo_id}")
                except Exception as e:
                    print(f"处理单条说说时发生错误: {e}")
                    traceback.print_exc()
        else:
            error_msg = result.get('message', '未知错误') if result else '无响应'
            print(f"未获取到说说或拉取失败，错误: {error_msg}")
    except Exception as e:
        print(f"拉取说说时发生异常: {e}")
        traceback.print_exc()