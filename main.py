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
    command = ["python", "C:\\Users\\kisho\\OneDrive\\Documents\\GitHub\\Network-Fortification\\PwnXSS\\PwnXSS\\pwnxss.py"]
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

def select_sqlmap_command(target_url):
    sqlmap_command = ["python", "C:\\Users\\kisho\\OneDrive\\Documents\\GitHub\\Network-Fortification\\sqlmap-master\\sqlmap.py"]  # Define sqlmap_command here
    while True:
        print("SQLMap Commands:")
        print("1. Using a proxy")
        print("2. Basic authentication")
        print("3. Default")
        print("4. --dbs")
        print("5. -tables")
        print("6. -columns -D DBNAME -T TABLENAME")
        print("7. --dump")
        print("8. --dump-all")
        print("9. --threads=THREADS")
        print("10. --level=LEVEL")
        print("11. --risk=RISK")
        print("12. --tamper=TAMPER")
        print("13. --os-shell")
        print("14. --batch")
        print("15. --proxy=PROXY")
        print("16. --crawl=CRAWL_DEPTH")
        print("17. --flush-session")
        print("18. --cookie=COOKIE")
        print("19. --exclude-sysdbs")
        print("20. --exclude=\"REGEX\"")
        print("21. Go back to the main menu")
        
        choice = input("Enter your choice (1-21): ")
        if choice == '21':
            return None
        elif choice in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'}:
            value = input(f"Enter value for option {choice}: ")
            if choice == '1':
                proxy_address = value
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--proxy", proxy_address, "--batch"])
            elif choice == '2':
                username = input("Enter the basic auth username: ")
                password = input("Enter the basic auth password: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--auth-type", "basic", "--auth-cred", f"{username}:{password}", "--batch"])
            elif choice == '3':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--batch"])
            elif choice == '4':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--dbs", "--batch"])
            elif choice == '5':
                database = input("Enter the database name: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"-D {database}", "--tables", "--batch"])
            elif choice == '6':
                database = input("Enter the database name: ")
                table = input("Enter the table name: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"-D {database} -T {table}", "--columns", "--batch"])
            elif choice == '7':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--dump", "--batch"])
            elif choice == '8':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--dump-all", "--batch"])
            elif choice == '9':
                threads = input("Enter number of threads: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--threads={threads}", "--batch"])
            elif choice == '10':
                level = input("Enter scan level (1-5): ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--level={level}", "--batch"])
            elif choice == '11':
                risk = input("Enter risk level (1-3): ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--risk={risk}", "--batch"])
            elif choice == '12':
                tamper_script = input("Enter path to tamper script: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--tamper={tamper_script}", "--batch"])
            elif choice == '13':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--os-shell", "--batch"])
            elif choice == '14':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--batch"])
            elif choice == '15':
                proxy_address = input("Enter the proxy address (e.g., http://proxy_address:port): ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--proxy={proxy_address}", "--batch"])
            elif choice == '16':
                crawl_depth = input("Enter the crawl depth: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--crawl={crawl_depth}", "--batch"])
            elif choice == '17':
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, "--flush-session", "--batch"])
            elif choice == '18':
                cookie = input("Enter the cookie string: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--cookie={cookie}", "--batch"])
            elif choice == '19':
                sqlmap_command.extend(["python","sqlmap.py", "-u", target_url, "--exclude-sysdbs", "--batch"])
            elif choice == '20':
                regex = input("Enter the regex pattern to exclude: ")
                sqlmap_command.extend(["python", "sqlmap.py", "-u", target_url, f"--exclude=\"{regex}\"", "--batch"])
            return sqlmap_command
        else:
            print("Invalid choice. Please select a valid option.")

def check_sql_injection():
    target_url = input("Enter the target server URL: ")
    sqlmap_command = select_sqlmap_command(target_url)
    if sqlmap_command:
        execute_sqlmap_script(sqlmap_command)

def execute_headers_script():
    try:
        subprocess.run(["python", "headers.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing headers.py: {e}")
    except FileNotFoundError:
        print("headers.py not found in the same directory.")

def execute_sqlmap_script(sqlmap_command):
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing sqlmap command: {e}")

def show_menu():
    print("Menu:")
    print("1. Headers")
    print("2. XSS")
    print("3. Check for SQL Injection (Using sqlmap)")
    print("4. Quit")

# Main loop and menu
while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        execute_headers_script()
    elif choice == '2':
        execute_xss_script()
    elif choice == '3':
        check_sql_injection()
    elif choice == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")
