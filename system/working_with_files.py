import json
from loguru import logger

def load_bot_info(messages):
    try:
        with open(messages, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        logger.error(f"Ошибка: {e}")


def save_bot_info(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
