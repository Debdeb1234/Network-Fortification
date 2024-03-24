import tkinter as tk
from tkinter import messagebox
import subprocess

def execute_headers_script():
    try:
        subprocess.run(["python", "headers.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error executing headers.py: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "headers.py not found in the same directory.")

def execute_xss_script():
    xss_script = r"D:\Firewall stuff\NF1-Dhanesh-s\NF1-Dhanesh-s\PwnXSS\PwnXSS\pwnxss.py"  
    xss_command = ["python", "-u", xss_script]

    try:
        xss_process = subprocess.Popen(xss_command)
        xss_process.wait()  # Wait for the process to terminate
    except FileNotFoundError:
        messagebox.showerror("Error", "pwnxss.py not found in the specified directory.")
    except KeyboardInterrupt:
        messagebox.showinfo("Info", "Execution interrupted.")

def execute_sqlmap_script(target_url, sqlmap_command):
    try:
        subprocess.run(sqlmap_command, check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error executing sqlmap command: {e}")

def select_sqlmap_command(target_url):
    # Implement the select_sqlmap_command function
    pass

def check_sql_injection(target_url):
    # Implement the check_sql_injection function
    pass

def handle_choice(choice):
    if choice == '1':
        execute_headers_script()
    elif choice == '2':
        execute_xss_script()
    elif choice == '3':
        target_url = input("Enter the target server URL: ")
        check_sql_injection(target_url)
    elif choice == '4':
        print("Goodbye!")
        root.destroy()
    else:
        messagebox.showerror("Error", "Invalid choice. Please select a valid option.")

def show_menu():
    menu_window = tk.Tk()
    menu_window.title("Menu")
    
    label = tk.Label(menu_window, text="Choose an option:")
    label.pack()

    button_headers = tk.Button(menu_window, text="Headers", command=lambda: handle_choice('1'))
    button_headers.pack()

    button_xss = tk.Button(menu_window, text="XSS", command=lambda: handle_choice('2'))
    button_xss.pack()

    button_sql_injection = tk.Button(menu_window, text="Check for SQL Injection", command=lambda: handle_choice('3'))
    button_sql_injection.pack()

    button_quit = tk.Button(menu_window, text="Quit", command=lambda: handle_choice('4'))
    button_quit.pack()

    menu_window.mainloop()

if __name__ == "__main__":
    show_menu()
