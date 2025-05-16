from utils.config_utils import read_config_from_directories
import os
from loguru import logger as log

# 使用命令台目录下的config目录作为配置目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIRS = [os.path.join(BASE_DIR, 'config')]

log.debug(f"读取配置文件: {CONFIG_DIRS}")

_config = read_config_from_directories(CONFIG_DIRS)

log.debug(f"获取到的配置文件为: {_config}")

API_KEY = _config.get('api_key') if _config else None
API_SECRET = _config.get('api_secret') if _config else None
ACCESS_TOKEN = _config.get('access_token') if _config else None
ACCESS_TOKEN_SECRET = _config.get('access_token_secret') if _config else None

TWITTER_CONFIG = {
    'api_key': API_KEY,
    'api_secret': API_SECRET,
    'access_token': ACCESS_TOKEN,
    'access_token_secret': ACCESS_TOKEN_SECRET
}