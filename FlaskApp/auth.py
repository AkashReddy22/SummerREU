from database import Database
from flask import Blueprint, Flask, flash, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

login_manager = LoginManager()
login_blueprint = Blueprint('Authentication',__name__, url_prefix="", template_folder='templates')
db = Database()

class LoginForm(FlaskForm):
    UserName = StringField('UserName', validators=[DataRequired()])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_with_id(user_id)

def add_login_routes(app: Flask):
    login_manager.init_app(app)
    app.register_blueprint(login_blueprint)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_with_id(form.UserName.data)
        if user is None:
            return 'Invalid Username or Password', 403
        if user and not user.check_password(form.Password.data):
            return 'Invalid Username or Password', 403
        login_user(user)
        flash('Logged in successfully.')
        next_url = request.args.get('next')
        return redirect(next_url or url_for('home'))
    return render_template('login.html', form=form)


@login_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('Authentication.login'))