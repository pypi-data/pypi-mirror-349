import json
import logging
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

CWD = Path.cwd()
HOME = Path.home()
CONFIG_DIR = HOME / ".pycmd2"


class Settings:
    def __init__(
        self,
        config_dir: Path,
        default_config: Optional[Dict[str, Any]] = None,
    ):
        """初始化配置管理器

        Args:
            config_dir: 配置文件目录路径
            default_config: 默认配置字典，当配置文件不存在时使用
        """
        self.config_dir = config_dir
        self.config_file = self.config_dir / "config.json"

        if self.config_file.exists():
            self.load_config()
        else:
            self.config = default_config if default_config else {}

    def load_config(self):
        try:
            with open(self.config_file) as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error loading config: {e}")
            self.config = {}
        except FileNotFoundError:
            logging.error(f"Config file not found: {self.config_file}")
            self.config = {}
        except Exception as e:
            logging.error(f"Error loading config: {e}")
            self.config = {}
        else:
            logging.info(f"Loading config from {self.config_file}")

    def save_config(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving config: {e}")
        else:
            logging.info(f"Config saved to {self.config_file}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        self.config[key] = value
        self.save_config()

    def delete(self, key: str):
        del self.config[key]
        self.save_config()


def get_settings(
    config_dir: Optional[Path] = None,
    default_config: Optional[Dict[str, Any]] = None,
) -> Settings:
    """获取配置管理器实例

    Args:
        config_dir: 配置文件目录路径，默认为用户主目录下的 .pycmd2
        default_config: 默认配置字典，当配置文件不存在时使用
    例如:
        {
            "key": "value",
            "key2": 123,
            "key3": True,
            "key4": ["a", "b", "c"],
            "key5": {"subkey": "subvalue"}
        }

    Returns:
        Settings 实例
    """
    if config_dir is None:
        config_dir = CONFIG_DIR
    return Settings(config_dir, default_config)
