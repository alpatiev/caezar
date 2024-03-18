import os
import re
import sys
import yaml
import time

# --------------------------------------------------
# SECTION: CONSOLE

def console_help():
    print("""
python app.py [--install | --update | --start | --stop   |   
               --reboot  | --view   | --auth <token> <chat>]

Options:
  --install     Install the application.
  --update      Update the application with repo and run.
  --start       Start the bot on background.
  --stop        Stop the bot, terminate deamon.
  --reboot      Restarting this bot.
  --view        Enter application console
  --auth        Save new configuration, 
                requires token and chat arguments.
                Example: --auth <token> <chat>
""")

# --------------------------------------------------
# SECTION: DAEMON

def call_daemon(command, value=None):
    bash_script_path = f"./daemon.sh {command} {value}"
    output_stream = os.popen(bash_script_path)
    output = output_stream.read()
    output_stream.close()
    return output

# --------------------------------------------------
# SECTION: CONFIG

def get_pid():
    with open("config.yaml", 'r') as file:
        lines = file.readlines()
    pid_line = lines[9] 
    pid_value = pid_line.split(":")[1].strip().strip("\"")
    return int(pid_value) if pid_value else None

def update_pid(new_pid):
    with open("config.yaml", 'r') as file:
        lines = file.readlines()   
    lines[9] = f"  pid: \"{new_pid}\"\n"
    with open("config.yaml", 'w') as file:
        file.writelines(lines)

def update_auth(bot_token, root_chat):
    with open("config.yaml", 'r') as file:
        lines = file.readlines()
    bot_token_line = f"  bot_token: \"{bot_token}\"\n"
    root_chat_line = f"  root_chat: \"{root_chat}\"\n"
    lines[16] = bot_token_line
    if root_chat_line:
        lines[17] = root_chat_line
    with open("config.yaml", 'w') as file:
        file.writelines(lines)

def parse_config():
    with open("config.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
    #auth_token = data.get("authentification", {}).get("bot_token", None)
    return data

# --------------------------------------------------
# SECTION: INSTALL

def install_application():
    os.system("pip install -r requirements.txt")
    os.system("chmod +x ./daemon.sh")

# --------------------------------------------------
# SECTION: UPDATE

def update_application():
    stop_application()
    os.system("git fetch origin")
    os.system("git reset --hard origin/master")
    start_application()

# --------------------------------------------------
# SECTION: START

def start_application():
    output = call_daemon("--boot")
    match = re.search(r'pid:(\d+)', output)
    if match:
        pid_str= ''.join(filter(str.isdigit, match.group(1)))
        if pid_str:
            pid = int(pid_str) 
            print(f">>> launched on pid: {pid}")
            update_pid(pid)
        else:
            print(">>> error: invalid pid")
    else:
        print(">>> error: no pid found")
    
# --------------------------------------------------
# SECTION: STOP

def stop_application():
    pid = get_pid()
    if pid:
        print(f">>> calling kill pid: {pid}..")
        call_daemon("--kill", pid)
        update_pid("")
    else:
        print(">>> bot is not running")

# --------------------------------------------------
# SECTION: REBOOT

def reboot_application():
    stop_application()
    time.sleep(2)
    start_application()

# --------------------------------------------------
# SECTION: VIEW

def view_application():
    pid = get_pid()
    if pid:
        print(f">>> running on pid: {pid}")
    else:
        print(">>> no daemon found")

# --------------------------------------------------
# SECTION: AUTH

def auth_application(bot_token, root_chat):
    update_auth(bot_token, root_chat)

# --------------------------------------------------
# ENTITY: APPLICATION

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        console_help()
        sys.exit(0)

    if "--install" in sys.argv:
        install_application()
    elif "--update" in sys.argv:
        update_application()
    elif "--start" in sys.argv:
        start_application()
    elif "--stop" in sys.argv:
        stop_application()
    elif "--reboot" in sys.argv:
        reboot_application()
    elif "--view" in sys.argv:
        view_application()
    elif "--auth" in sys.argv:
        bot_token = sys.argv[2] if len(sys.argv) >= 3 else ""
        chat_id = sys.argv[3] if len(sys.argv) >= 4 else ""
        auth_application(bot_token, chat_id)
    else:
        console_help()
        sys.exit(0)
