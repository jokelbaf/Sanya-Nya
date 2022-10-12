"""Events and errors Logger. Logs errors and tracebacks.
It can also create required log Files if not excist."""

import traceback, json, Config
from datetime import datetime 
       
def update_logs_lvl(now):
    with open("./logs/settings.json", "r+", encoding="utf-8") as settings:
        lvl = Config.Bot.logs_lvl()
        data = json.load(settings)
        data["logs_lvl"] = lvl
        json.dump(data, settings, sort_keys=True, indent=4, ensure_ascii=False)
        print(f"[{now.strftime('%m/%d/%Y, %H:%M:%S')}] [SANYA/INFO]: Уровень логов обновлён согласно заданному в конфиге.")


def recreate_settings(now):
    with open("./logs/settings.json", "w", encoding="utf-8") as settings:
        settings.truncate(0)
    
    with open("./logs/settings.json", "r+", encoding="utf-8") as settings:
        data = Config.Logs.data()
        data["logs_file"] = f"{now.strftime('%m-%d-%Y-%H-%M-%S')}.txt"
        json.dump(data, settings, sort_keys=True, indent=4, ensure_ascii=False)
        print(f"[{now.strftime('%m/%d/%Y, %H:%M:%S')}] [SANYA/INFO]: Файл настроек логов (./logs/settings.json) был создан/пересоздан.")


def log(module: str, logs_type: str, text: str):
    now = datetime.now()
    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)
        logs_lvl = data["logs_lvl"]
        logs_file = data["logs_file"]
    if logs_lvl in [2, 3]:
        with open(file=f"./logs/{logs_file}", mode="a", encoding="utf-8") as logs:
            logs.write(f"\n[{now.strftime(f'%m/%d/%Y, %H:%M:%S')}] [{module}/{logs_type}]: {text}")
    if logs_lvl in [1, 3]:
        print(f"[{now.strftime(f'%m/%d/%Y, %H:%M:%S')}] [{module}/{logs_type}]:", text)
        

def log_traceback():
    now = datetime.now()
    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)
        logs_lvl = data["logs_lvl"]
        logs_file = data["logs_file"]
    if logs_lvl in [2, 3]:
        with open(file=f"./logs/{logs_file}", mode="a", encoding="utf-8") as logs:
            logs.write(f"\n{traceback.format_exc()}")
    if logs_lvl == 1:
        print(f"[{now.strftime(f'%m/%d/%Y, %H:%M:%S')}] Критическая ошибка в приложении. Трассировка сохранена в логах.")
    if logs_lvl == 3:
        print(f"[{now.strftime(f'%m/%d/%Y, %H:%M:%S')}] Критическая ошибка в приложении. Трассировка сохранена в логах.")
