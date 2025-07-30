import os
import json
import logging

logger = logging.getLogger()

class StorageService:
    def __init__(self):
        # 优先使用环境变量配置的路径，如果没有则使用默认路径
        self.base_path = os.environ.get('STORAGE_PATH', '/mnt/app')
        # 确保基础目录存在
        os.makedirs(self.base_path, exist_ok=True)

    def save_to_file(self, filename, content):
        """保存内容到文件"""
        try:
            filepath = os.path.join(self.base_path, filename)
            with open(filepath, 'w') as f:
                if isinstance(content, (dict, list)):
                    json.dump(content, f, ensure_ascii=False, indent=2)
                else:
                    f.write(str(content))
            logger.info(f"Successfully saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save to {filepath}: {str(e)}")
            raise

    def load_from_file(self, filename):
        """从文件加载内容"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if not os.path.exists(filepath):
                return None
            with open(filepath, 'r') as f:
                content = f.read()
                try:
                    return json.loads(content)
                except:
                    return content
        except Exception as e:
            logger.error(f"Failed to load from {filepath}: {str(e)}")
            return None 