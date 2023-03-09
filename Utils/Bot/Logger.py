"""Events and errors Logger. Logs errors and tracebacks."""

import traceback, json, Config
from datetime import datetime


# This is executed when bot starts.
def on_ready():

    # Update logs level in settings.json according to config.
    update_logs_lvl(datetime.now())

    # Create file {current time}.txt where all logs for this session will be stored.
    create_logs_file(datetime.now())

       
def update_logs_lvl(now):

    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)
        data["logs_lvl"] = Config.Bot.logs_lvl

    with open("./logs/settings.json", "w", encoding="utf-8") as settings:
        json.dump(data, settings, sort_keys=True, indent=4, ensure_ascii=False)
        print(f"[{now.strftime('%m/%d/%Y, %H:%M:%S')}] [SANYA/INFO]: Logs level updated according to config.")


def create_logs_file(now):

    with open(file=f"./logs/{now.strftime('%m-%d-%Y-%H-%M-%S')}.txt", mode="w", encoding="utf-8") as logs:
        logs.write(f"[{now.strftime(f'%m/%d/%Y, %H:%M:%S')}] [SANYA/LOGS]: Logs file created.")

    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)

    with open("./logs/settings.json", "w", encoding="utf-8") as settings:
        data["logs_file"] = f"{now.strftime('%m-%d-%Y-%H-%M-%S')}.txt"
        json.dump(data, settings, sort_keys=True, indent=4, ensure_ascii=False)


def log(module: str, logs_type: str, text: str):
    """
    Log any message. 
    
    If `logs_lvl` is set to `3`, the message will be logged to both *file* and *console*.

    If `logs_lvl` is set to `2`, the message will be logged to *file* only.
    
    If `logs_lvl` is set to `1`, the message will be logged to *console* only.

    If `logs_lvl` is set to `0`, this function will do nothing.
    """

    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)
        logs_lvl = data["logs_lvl"]
        logs_file = data["logs_file"]

    if logs_lvl in [2, 3]:
        with open(file=f"./logs/{logs_file}", mode="a", encoding="utf-8") as logs:
            logs.write(f"\n[{datetime.now().strftime(f'%m/%d/%Y, %H:%M:%S')}] [{module}/{logs_type}]: {text}")

    if logs_lvl in [1, 3]:
        print(f"[{datetime.now().strftime(f'%m/%d/%Y, %H:%M:%S')}] [{module}/{logs_type}]:", text)
        

def log_traceback():
    """Log last error traceback."""

    with open("./logs/settings.json", "r", encoding="utf-8") as settings:
        data = json.load(settings)
        logs_lvl = data["logs_lvl"]
        logs_file = data["logs_file"]

    if logs_lvl in [2, 3]:
        with open(file=f"./logs/{logs_file}", mode="a", encoding="utf-8") as logs:
            logs.write(f"\n{traceback.format_exc()}")

    if logs_lvl == 1:
        print(f"[{datetime.now().strftime(f'%m/%d/%Y, %H:%M:%S')}] Critical error in the application. Trackeback was saved to the logs.")
    
    if logs_lvl == 3:
        print(f"[{datetime.now().strftime(f'%m/%d/%Y, %H:%M:%S')}] Critical error in the application. Trackeback was saved to the logs.")
