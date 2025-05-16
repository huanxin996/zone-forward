# QQ空间自动转发工具 🚀

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)
![Last Commit](https://img.shields.io/badge/last%20commit-May%202025-orange)
![Made with Love](https://img.shields.io/badge/made%20with-%E2%9D%A4-red)

## 📝 项目简介

这是一个能够自动拉取QQ空间说说并转发到其他社交平台的工具。该项目可以：

- 🔄 自动登录QQ空间并获取最新说说
- 💾 将说说内容（包括文字和图片）保存到本地数据库
- 🚀 通过自定义机器人将内容转发到其他平台
- 🛡️ 支持多层转发内容解析
- 📊 简单的运行状态日志

## 🛠️ 技术架构

- **QZoneAPI**: 用于QQ空间登录和内容获取
- **SQLite**: 本地数据存储与管理
- **异步编程**: 基于asyncio的高效异步操作
- **可扩展接口**: 支持自定义平台机器人对接

## 📋 功能特性

- **自动拉取**: 定时获取QQ空间最新说说
- **智能解析**: 支持文字、图片以及多层转发内容
- **本地存储**: 使用SQLite保存所有内容，防止重复转发
- **灵活配置**: 支持多种配置文件格式(json, yaml, toml, ini等)
- **定期备份**: 自动备份数据库，防止数据丢失
- **自定义转发**: 开放接口允许对接任何社交平台

## ⚙️ 安装与配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建配置文件

在项目根目录下创建config文件夹，并在其中创建配置文件(支持多种格式)，可以参考utils/config.py里的内容来写对应的配置读取：

#### 配置文件示例 (config/config.json)

```json
{
  "qq": "你的QQ号",
  "auto_login": true,
  "forward_interval": 120,
  "platform_configs": {
    "weibo": {
      "app_key": "你的微博AppKey",
      "app_secret": "你的微博AppSecret",
      "redirect_uri": "回调URL",
      "access_token": "访问令牌"
    },
    "telegram": {
      "bot_token": "你的TG机器人Token",
      "chat_id": "目标聊天ID"
    }
  }
}
```

## 🔌 定制你的转发机器人

本项目设计为高度可扩展，你可以轻松实现自己的转发机器人。只需创建或修改bot.py文件：

### 基础机器人模板

```python
# 示例: utils/bot.py
class BaseBot:
    def __init__(self, config):
        self.config = config
        # 初始化你的平台API客户端
        
    def post_text(self, text):
        """发布纯文本内容"""
        raise NotImplementedError("请在子类中实现此方法")
        
    def post_text_with_media(self, text, media_url):
        """发布带媒体的内容"""
        raise NotImplementedError("请在子类中实现此方法")

# 示例: 微博机器人
class WeiboBot(BaseBot):
    def post_text(self, text):
        # 实现微博文本发布逻辑
        print(f"发布到微博: {text[:20]}...")
        
    def post_text_with_media(self, text, media_url):
        # 实现微博带图片发布逻辑
        print(f"发布到微博(带图片): {text[:20]}..., 图片: {media_url}")
        
# 示例: Telegram机器人
class TelegramBot(BaseBot):
    def post_text(self, text):
        # 实现Telegram消息发送逻辑
        print(f"发送到Telegram: {text[:20]}...")
        
    def post_text_with_media(self, text, media_url):
        # 实现Telegram带图片消息发送逻辑
        print(f"发送到Telegram(带图片): {text[:20]}..., 图片: {media_url}")

# 导出你想使用的机器人类
Bot = WeiboBot  # 或 TelegramBot, 或者其他自定义机器人类
```

## 🚀 使用方法

### 1. 基本运行

```bash
python main.py
```

首次运行时，程序会要求你登录QQ空间，之后会自动保存登录状态。

### 2. 测试API连接

```bash
python test_qzone.py
```

## 📊 数据流程

1. **自动登录** QQ空间获取授权信息
2. **定期拉取** 最新说说内容
3. **解析处理** 说说的文字、图片和转发内容
4. **保存到数据库** 防止重复处理
5. **转发到平台** 通过自定义机器人发布到目标平台
6. **标记状态** 更新数据库中的转发状态

## 🔄 定制化开发

### 添加新的平台支持

1. 在bot.py中创建新的机器人类
2. 实现`post_text`和`post_text_with_media`以及`post_media`方法
3. 更新配置文件，添加新平台的认证信息

### 调整转发内容格式

修改main.py中的转发逻辑，可以自定义:

```python
# 自定义转发格式
text = f"📱QQ空间动态: {content.get('content', '')}"
if repost:
    text += f"\n\n💬转发: {repost.get('content', '')}"
```

## 🛡️ 数据安全

- 所有QQ登录信息存储在本地，不会上传到任何服务器
- 数据库定期自动备份，备份文件存储在db_rl目录下
- 所有API密钥和令牌仅保存在本地配置文件中

## 📈 未来计划

- [ ] 支持更多QQ空间内容类型(日志、相册等)
- [ ] 提供Web界面进行可视化管理
- [ ] 增加内容过滤和转换规则
- [ ] 支持多账号管理

## 🤝 贡献指南

欢迎提交Pull Request或Issues来帮助改进这个项目!

1. Fork这个仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建一个Pull Request

## 📜 许可证

本项目采用MIT许可证 - 详情请参阅LICENSE文件

## 📧 联系方式

如有问题或建议，请提交Issue或通过以下方式联系我: [mc.xiaolang@foxmail.com](mailto:mc.xiaolang@foxmail.com)

---

**免责声明**: 本工具仅供学习和个人使用，请遵守相关平台的使用条款和政策。使用者需对自己的行为负责。
