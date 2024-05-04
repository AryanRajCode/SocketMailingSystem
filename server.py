import socket
import os

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

def receive_mail(username):
    try:
        with open(f"{username}.txt", 'r') as reader:
            mail_content = reader.read()
            return mail_content
    except FileNotFoundError:
        return "No mail found"
    except Exception as e:
        return f"ERROR: {e}"

def send_mail(sender, recipient, message):
    try:
        if not os.path.exists(f"{recipient}.txt"):
            with open(f"{recipient}.txt", 'w') as recipient_file:
                recipient_file.write('')
        with open(f"{recipient}.txt", 'a+') as recipient_file:
            recipient_file.write(f'Sender: {sender}\nMessage: {message}\n')
        return "Mail sent successfully"
    except Exception as e:
        return f"ERROR: {e}"

def create_user(username, password):
    if len(password) < 6:
        return "Password must be at least 6 characters long"
    try:
        with open('pass.txt', 'a+') as pass_file:
            pass_file.write(f'{username}:{password}\n')
        return "User created successfully"
    except Exception as e:
        return f"ERROR: {e}"

def delete_mails(username):
    try:
        os.remove(f"{username}.txt")
        return "Mails deleted successfully"
    except FileNotFoundError:
        return "No mails found for this user"
    except Exception as e:
        return f"ERROR: {e}"

def validate_credentials(username, password):
    try:
        with open('pass.txt', 'r') as pass_file:
            for line in pass_file:
                if line.strip() == f"{username}:{password}":
                    return True
        return False
    except Exception as e:
        return f"ERROR: {e}"

def handle_client_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        data = conn.recv(1024).decode()
        if not data:
            return

        command, *args = data.split("|")
        if command not in ["RECEIVE_MAIL", "SEND_MAIL", "CREATE_USER", "DELETE_MAILS", "VALIDATE_CREDENTIALS"]:
            response = "Invalid command"
        else:
            if command == "RECEIVE_MAIL":
                if len(args) != 2:
                    response = "Invalid arguments for RECEIVE_MAIL"
                else:
                    username, password = args
                    if validate_credentials(username, password):
                        response = receive_mail(username)
                    else:
                        response = "Invalid credentials"
            elif command == "SEND_MAIL":
                if len(args) != 4:
                    response = "Invalid arguments for SEND_MAIL"
                else:
                    sender, recipient, message, password = args
                    if validate_credentials(sender, password):
                        response = send_mail(sender, recipient, message)
                    else:
                        response = "Invalid credentials"
            elif command == "CREATE_USER":
                if len(args) != 2:
                    response = "Invalid arguments for CREATE_USER"
                else:
                    username, password = args
                    response = create_user(username, password)
            elif command == "DELETE_MAILS":
                if len(args) != 2:
                    response = "Invalid arguments for DELETE_MAILS"
                else:
                    username, password = args
                    if validate_credentials(username, password):
                        response = delete_mails(username)
                    else:
                        response = "Invalid credentials"
            elif command == "VALIDATE_CREDENTIALS":
                if len(args) != 2:
                    response = "Invalid arguments for VALIDATE_CREDENTIALS"
                else:
                    username, password = args
                    if validate_credentials(username, password):
                        response = "True"
                    else:
                        response = "False"

        conn.sendall(response.encode())

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            handle_client_connection(conn, addr)

if __name__ == "__main__":
    server()
