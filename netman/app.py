from flask import Flask, render_template, request, redirect, url_for, session
import requests
import yaml

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Authenticate user
    session['username'] = username
    return redirect(url_for('index'))

@app.route('/configure', methods=['POST'])
def configure():
    if 'username' not in session:
        return redirect(url_for('index'))
    port = request.form['port']
    config = request.form['config']
    # Make API request to configure the port
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)