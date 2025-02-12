from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to a strong secret key

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="rootpass",
        database="mydatabase"
    )

# User Model
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Flask-Login User Loader
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1])
    return None

# Flask-WTF Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

@app.route('/')
def home():
    return "Flask app is running! <a href='/login'>Login</a>"

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_user(User(user[0], username))
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Try again."

    return render_template("login.html", form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {current_user.username}! <a href='/logout'>Logout</a>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
