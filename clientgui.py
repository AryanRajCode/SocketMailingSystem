import tkinter as tk
from tkinter import messagebox, simpledialog
import socket

print('''Enter S To Select ip 
      Or
Enter D to Use Default ip''')
a = input("Enter : ")
if a.lower() == "d":
    HOST = '127.0.0.1'
    PORT = 65432
elif a.lower() == "s":
    HOST = input("Enter Ip :")
    PORT = int(input("Enter Port : "))  # Convert input to int
    
else:
    print("Enter Valid Option")
    exit()  # Added parentheses and parentheses to the function call


class MailClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail Client")

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        try:
            self.read_button = tk.Button(root, text="Read Mails", command=self.read_mail)
            self.read_button.grid(row=2, column=0, padx=5, pady=5)
            self.write_button = tk.Button(root, text="Write Mail", command=self.write_mail)
            self.write_button.grid(row=2, column=1, padx=5, pady=5)
            self.create_button = tk.Button(root, text="Create User", command=self.create_user)
            self.create_button.grid(row=3, column=0, padx=5, pady=5)
            self.delete_button = tk.Button(root, text="Delete Mails", command=self.delete_mails)
            self.delete_button.grid(row=3, column=1, padx=5, pady=5)
        except:
                pass
        self.message_label = tk.Label(root, text="Message:")
        self.message_label.grid(row=4, column=0, padx=5, pady=5)
        self.message_entry = tk.Text(root, height=5, width=30)
        self.message_entry.grid(row=4, column=1, padx=5, pady=5)

        self.send_button = tk.Button(root, text="Send Message", command=self.send_message)
        self.send_button.grid(row=5, column=1, padx=5, pady=5)

                
    def send_receive(self, command, *args):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            message = f"{command}|{'|'.join(args)}"
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            return response
    try :
        def read_mail(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            response = self.send_receive("RECEIVE_MAIL", username, password)
            if response.startswith("ERROR"):
                messagebox.showerror("Error", response)
            else:
                messagebox.showinfo("Mail", response)
    except:
        pass
    try:
        def write_mail(self):
            self.message_entry.delete(1.0, tk.END)
    except:
        pass
    try:
        def create_user(self):
            username = simpledialog.askstring("Create User", "Enter new username:")
            if username:
                password = simpledialog.askstring("Create User", "Enter password:")
                if password:
                    response = self.send_receive("CREATE_USER", username, password)
                if response.startswith("ERROR"):
                    messagebox.showerror("Error", response)
                else:
                    messagebox.showinfo("User Creation", response)
    except:
        pass
    try:
        def delete_mails(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            response = self.send_receive("DELETE_MAILS", username, password)
            if response.startswith("ERROR"):
                messagebox.showerror("Error", response)
            else:
                messagebox.showinfo("Mail Deletion", response)
    except:
        pass
    try:
        def send_message(self):
            recipient = simpledialog.askstring("Recipient", "Enter recipient's username:")
            if recipient:
                message = self.message_entry.get(1.0, tk.END)
                username = self.username_entry.get()
                password = self.password_entry.get()
                response = self.send_receive("SEND_MAIL", username, recipient, message, password)
                if response.startswith("ERROR"):
                    messagebox.showerror("Error", response)
                else:
                    messagebox.showinfo("Mail", response)
    except:
        pass
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MailClientGUI(root)
    root.mainloop()
