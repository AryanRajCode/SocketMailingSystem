from flask import Flask, render_template, request, redirect, url_for, flash
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'

HOST = '127.0.0.1'
PORT = 65432

def send_receive(command, *args):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        message = f"{command}|{'|'.join(args)}"
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
        return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read_mail', methods=['GET', 'POST'])
def read_mail():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = send_receive("RECEIVE_MAIL", username, password)
        flash(response, 'info')
        return redirect(url_for('index'))
    return render_template('read_mail.html')

@app.route('/write_mail', methods=['GET', 'POST'])
def write_mail():
    if request.method == 'POST':
        username = request.form['username']
        recipient = request.form['recipient']
        message = request.form['message']
        password = request.form['password']
        response = send_receive("SEND_MAIL", username, recipient, message, password)
        flash(response, 'info')
        return redirect(url_for('index'))
    return render_template('write_mail.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = send_receive("CREATE_USER", username, password)
        flash(response, 'info')
        return redirect(url_for('index'))
    return render_template('create_user.html')

@app.route('/delete_mails', methods=['GET', 'POST'])
def delete_mails():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = send_receive("DELETE_MAILS", username, password)
        flash(response, 'info')
        return redirect(url_for('index'))
    return render_template('delete_mails.html')

if __name__ == '__main__':
    app.run(debug=True)
