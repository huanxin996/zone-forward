import os,json,configparser,toml,yaml
from typing import List, Optional, Any

def read_config_from_directories(directories: List[str]) -> Optional[Any]:
    """读取配置"""
    config_filenames = [
        'config.json', 'config.yaml', 'config.yml', 'config.toml', 'config.env', 'config.ini', '.env'
    ]
    for directory in directories:
        for filename in config_filenames:
            config_path = os.path.join(directory, filename)
            if os.path.exists(config_path):
                try:
                    if filename.endswith('.json'):
                        with open(config_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if data:
                                return data
                    elif filename.endswith(('.yaml', '.yml')):
                        with open(config_path, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if data:
                                return data
                    elif filename.endswith('.toml'):
                        with open(config_path, 'r', encoding='utf-8') as f:
                            data = toml.load(f)
                            if data:
                                return data
                    elif filename.endswith('.ini'):
                        parser = configparser.ConfigParser()
                        parser.read(config_path, encoding='utf-8')
                        data = {section: dict(parser.items(section)) for section in parser.sections()}
                        if data:
                            return data
                    elif filename.endswith('.env') or filename == '.env':
                        data = {}
                        with open(config_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith('#') and '=' in line:
                                    k, v = line.split('=', 1)
                                    data[k.strip()] = v.strip()
                        if data:
                            return data
                except Exception:
                    continue
    return None
