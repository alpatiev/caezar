import os
import sys
import daemon

# --------------------------------------------------
# SECTION: DAEMON

def call_daemon(command, value):
    bash_script_path = f"./daemon.sh {command} {value}"
    output_stream = os.popen(bash_script_path)
    output = output_stream.read()
    output_stream.close()
    return output

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
# SECTION: INSTALL

def install_application():
    print("install")

# --------------------------------------------------
# SECTION: UPDATE

def update_application():
    print("updateee")

# --------------------------------------------------
# SECTION: START

def start_application():
    print("Starting the application...")
    if os.path.isfile("daemons.txt"):
        print("daemons.txt exists.")
        with open("daemons.txt", "r") as file:
            existing_pid = file.read().strip()
        if existing_pid:
            print("Daemon already running with PID:", existing_pid)
            return existing_pid

    output = call_daemon("--boot", "python bot/boot.py")
    # Print the output
    print(output)
    

# --------------------------------------------------
# SECTION: STOP

def stop_application():
    print("stop")

# --------------------------------------------------
# SECTION: VIEW

def view_application():
    # Check if the daemons.txt file exists
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

def auth_application(bot_token, root_chat, path="bot/config.yaml"):
    with open(path, 'r') as file:
        lines = file.readlines()
    bot_token_line = f"  bot_token: \"{bot_token}\"\n"
    root_chat_line = f"  root_chat: \"{root_chat}\"\n"
    lines[9] = bot_token_line
    if root_chat_line:
        lines[10] = root_chat_line
    with open(path, 'w') as file:
        file.writelines(lines)

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
