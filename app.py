import os
import re
import sys
import yaml

# --------------------------------------------------
# SECTION: CONSOLE

def console_help():
    print("""
python app.py [--install | --update | --start | --stop | --view | --auth <token> <chat>]

Options:
  --install     Install the application.
  --update      Update the application with repo.
  --start       Start the bot.
  --stop        Stop the bot, terminate deamon.
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
    lines[15] = bot_token_line
    if root_chat_line:
        lines[16] = root_chat_line
    with open("config.yaml", 'w') as file:
        file.writelines(lines)

def parse_config():
    return "0xffffffff"

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
            print(f"Founded pid: {pid}")
            update_pid(pid)
        else:
            print("invalid pid")
    else:
        print("No pid found.")
    
# --------------------------------------------------
# SECTION: STOP

def stop_application():
    pid = get_pid()
    if pid:
        call_daemon("--kill", pid)
        update_pid("")
        print("> Killed successfully")
    else:
        print("> App is not running")

# --------------------------------------------------
# SECTION: VIEW

def view_application():
    if os.path.isfile("daemons.txt"):
        with open("daemons.txt", "r") as file:
            daemon_pid = file.read().strip()        
        if daemon_pid:
            print("Daemon process is running with PID:", daemon_pid)
        else:
            print("Daemon PID does not exist in daemons.txt.")
    else:
        print("Daemons file does not exist.")

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
    elif "--view" in sys.argv:
        view_application()
    elif "--auth" in sys.argv:
        bot_token = sys.argv[2] if len(sys.argv) >= 3 else ""
        chat_id = sys.argv[3] if len(sys.argv) >= 4 else ""
        auth_application(bot_token, chat_id)
    else:
        console_help()
        sys.exit(0)
