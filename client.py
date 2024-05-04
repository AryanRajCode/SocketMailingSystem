import socket
import sys
import os

os.system("clear")
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



def send_receive(command, *args):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        message = f"{command}|{'|'.join(args)}"
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        return response

def read_mail():
    username = input("Enter Your Name: ")
    password = input("Enter Your Password: ")
    response = send_receive("RECEIVE_MAIL", username, password)
    print("Your Mails:")
    print(response)

def write_mail():
    username = input("Enter Your Name: ")
    recipient = input("Whom You Want To Send: ")
    message = input("Enter Message: ")
    
    password = input("Enter Your Password: ")
    response = send_receive("SEND_MAIL", username, recipient, message, password)
    print(response)
#  username,
def create_user():
    username = input("Enter Your Name: ")
    password = input("Enter a Password (at least 6 characters): ")
    response = send_receive("CREATE_USER", username, password)
    print(response)

def delete_mails():
    username = input("Enter Your Name: ")
    password = input("Enter Your Password: ")
    response = send_receive("DELETE_MAILS", username, password)
    print(response)

def show_menu():
    print("\nOptions:")
    print("1. Read Mails")
    print("2. Write A Mail")
    print("3. Create User")
    print("4. Delete My Mails")
    print("5. Exit")

def main():
    print("\nWelcome to Mail Client")
    while True:
        show_menu()
        option = input("Enter an Option: ")

        if option == '1':
            read_mail()
        elif option == '2':
            write_mail()
        elif option == '3':
            create_user()
        elif option == '4':
            delete_mails()
        elif option == '5':
            print("Closing")
            sys.exit()
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
