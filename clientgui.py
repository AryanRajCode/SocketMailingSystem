import tkinter as tk
from tkinter import messagebox, simpledialog
import socket

def get_host_port():
    print('''Enter S To Select IP 
      Or
Enter D to Use Default IP''')
    choice = input("Enter : ").lower()
    if choice == "d":
        return '127.0.0.1', 65432
    elif choice == "s":
        host = input("Enter IP: ")
        port = int(input("Enter Port: "))
        return host, port
    else:
        print("Enter a valid option")
        exit()

HOST, PORT = get_host_port()

class MailClientGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mail Client")

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Read Mails", command=self.read_mail).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Write Mail", command=self.write_mail).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Create User", command=self.create_user).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Delete Mails", command=self.delete_mails).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Message:").grid(row=4, column=0, padx=5, pady=5)
        self.message_entry = tk.Text(self.root, height=5, width=30)
        self.message_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Send Message", command=self.send_message).grid(row=5, column=1, padx=5, pady=5)

    def send_receive(self, command, *args):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            message = f"{command}|{'|'.join(args)}"
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            return response

    def read_mail(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = self.send_receive("RECEIVE_MAIL", username, password)
        if response.startswith("ERROR"):
            messagebox.showerror("Error", response)
        else:
            messagebox.showinfo("Mail", response)

    def write_mail(self):
        self.message_entry.delete(1.0, tk.END)

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

    def delete_mails(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = self.send_receive("DELETE_MAILS", username, password)
        if response.startswith("ERROR"):
            messagebox.showerror("Error", response)
        else:
            messagebox.showinfo("Mail Deletion", response)

    def send_message(self):
        recipient = simpledialog.askstring("Recipient", "Enter recipient's username:")
        if recipient:
            message = self.message_entry.get(1.0, tk.END).strip()
            username = self.username_entry.get()
            password = self.password_entry.get()
            response = self.send_receive("SEND_MAIL", username, recipient, message, password)
            if response.startswith("ERROR"):
                messagebox.showerror("Error", response)
            else:
                messagebox.showinfo("Mail", response)

if __name__ == "__main__":
    root = tk.Tk()
    app = MailClientGUI(root)
    root.mainloop()
