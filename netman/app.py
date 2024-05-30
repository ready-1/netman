from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from netman.auth import login_to_api, logout_from_api  # Use absolute import
from netman.models import User  # Use absolute import

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    user_data = User.get(username)
    if user_data:
        user = UserMixin()
        user.id = username
        return user
    return None

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_to_api(username, password):
            user_data = User.get(username)
            if user_data:
                user = UserMixin()
                user.id = username
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('User not found in local storage')
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    if logout_from_api():
        logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.create(username, password):
            flash('User registered successfully')
            return redirect(url_for('login'))
        else:
            flash('Username already exists')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)