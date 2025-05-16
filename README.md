# QQ空间-Twitter自动转发工具

## 关于API错误403问题的解决方案

从 2023 年开始，Twitter API 政策发生了重大变更。免费API访问**只限于非常少量的端点**，包括发推文在内的大多数写入功能都需要付费订阅计划：

- 免费级别 (Free)：几乎不包括任何写入API
- 基础级别 (Basic - $100/月起)：包含部分API，每月可发布1500条推文
- 企业级别和企业级别+：提供更多API功能

## 本代码适配策略

为应对这一限制，本代码采用了多重尝试方案：

1. **尝试Twitter API v2**：首先尝试使用v2端点 `create_tweet`
2. **备用Twitter API v1.1**：如v2失效，尝试v1.1的 `update_status` 
3. **本地草稿保存**：如果API调用全部失败，内容会保存在 `twitter_drafts` 文件夹，可手动发布

## 要完全解决问题的方案

1. **付费升级Twitter API**：访问 https://developer.twitter.com/en/portal/products/basic 购买Basic套餐
2. **替代自动发布方式**：
   - 使用自动化浏览器(如Selenium)模拟网页操作发布推文
   - 考虑使用其他平台如Mastodon, Bluesky等

## 使用此代码的临时方案

如API调用均失败，程序将：
1. 继续从QQ空间拉取内容到数据库
2. 保存所有待发布内容到 `twitter_drafts` 文件夹
3. 你可手动查看此文件夹内容并发布到Twitter

## 诊断您的API状态

```python
import tweepy
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

# 测试v1.1
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
try:
    user = api.verify_credentials()
    print("v1.1认证成功:", user.screen_name)
except Exception as e:
    print("v1.1认证失败:", e)

# 测试v2
client = tweepy.Client(
    consumer_key=API_KEY, 
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN, 
    access_token_secret=ACCESS_TOKEN_SECRET
)
try:
    user = client.get_me()
    print("v2认证成功:", user.data)
except Exception as e:
    print("v2认证失败:", e)
```
