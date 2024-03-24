import subprocess

def execute_xss_script():
    print("PwnXSS Commands:")
    print("1. -u <target>")
    print("2. --payload")
    print("3. --depth")
    print("4. --method")
    print("5. --proxy")
    print("6. --about")
    print("7. --cookie")
    print("8. Execute PwnXSS")

    pwnxss_commands = []
    
    while True:
        choice = input("Enter your choice (or '8' to execute): ")
        
        if choice == '8':
            break
        
        if choice not in {'1', '2', '3', '4', '5', '6', '7'}:
            print("Invalid choice. Please select a valid option.")
            continue

        value = input(f"Enter value for option {choice}: ")
        pwnxss_commands.append((choice, value))

    # Constructing the final PwnXSS command
    command = ["python", "PwnXSS/PwnXSS/pwnxss.py"]
    for option, value in pwnxss_commands:
        if option == '1':
            command.extend(["-u", value])
        elif option == '2':
            command.extend(["--payload", value])
        elif option == '3':
            command.extend(["--depth", value])
        elif option == '4':
            command.extend(["--method", value])
        elif option == '5':
            command.extend(["--proxy", value])
        elif option == '6':
            command.append("--about")
        elif option == '7':
            command.extend(["--cookie", value])

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing PwnXSS command: {e}")
    except FileNotFoundError:
        print("PwnXSS script not found.")
    except KeyboardInterrupt:
        print("Execution interrupted.")

def show_menu():
    print("Menu:")
    print("1. Headers")
    print("2. XSS")
    print("3. Check for SQL Injection (Using sqlmap)")
    print("4. Quit")

def execute_headers_script():
    try:
        subprocess.run(["python", "headers.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing headers.py: {e}")
    except FileNotFoundError:
        print("headers.py not found in the same directory.")

def execute_sqlmap_script(target_url, sqlmap_command):
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing sqlmap command: {e}")

def select_sqlmap_command(target_url):
    while True:
        print("SQLMap Command Menu:")
        print("1. Using a proxy")
        print("2. Basic authentication")
        print("3. Default")
        print("4. Go back to the main menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            proxy_address = input("Enter the proxy address (e.g., http://proxy_address:port): ")
            sqlmap_command = [
                "python", r"C:\Users\kisho\OneDrive\Documents\GitHub\Network-Fortification\sqlmap-master\sqlmap.py", "-u", target_url,
                "--proxy", proxy_address, "--batch"
            ]
            execute_sqlmap_script(target_url, sqlmap_command)
        elif choice == '2':
            param1 = input("Enter param1 value: ")
            param2 = input("Enter param2 value: ")
            username = input("Enter the basic auth username: ")
            password = input("Enter the basic auth password: ")
            sqlmap_command = [
                "python", r"C:\Users\kisho\OneDrive\Documents\GitHub\Network-Fortification\sqlmap-master\sqlmap.py", "-u", target_url,
                "-data=param1={}&param2={}".format(param1, param2), "-p", "param1", "--auth-type", "basic",
                "--auth-cred", "{}:{}".format(username, password), "--batch"
            ]
            execute_sqlmap_script(target_url, sqlmap_command)
        elif choice == '3':
            sqlmap_command = [
                "python", r"C:\Users\kisho\OneDrive\Documents\GitHub\Network-Fortification\sqlmap-master\sqlmap.py", "-u", target_url,
                "--batch"
            ]
            execute_sqlmap_script(target_url, sqlmap_command)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select a valid option.")

def check_sql_injection(target_url):
    select_sqlmap_command(target_url)

# Main loop and menu
while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        execute_headers_script()
    elif choice == '2':
        execute_xss_script()
    elif choice == '3':
        target_url = input("Enter the target server URL: ")
        check_sql_injection(target_url)
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")
