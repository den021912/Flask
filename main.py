from flask import Flask, render_template, request
import hashlib
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, LoginManager, logout_user
from models import db, Game, Buyer

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()

admin = Admin(app)
admin.add_view(ModelView(Buyer, db.session))
admin.add_view(ModelView(Game, db.session))


@login_manager.user_loader
def load_user(id):
    return Buyer.query.get(int(id))


@app.route('/')
def main_page():
    games = Game.query.order_by(Game.created_at.desc()).all()
    return render_template('main_page.html', games =games)


@app.route('/games')
def games_page():
    games = Game.query.order_by(Game.created_at.desc()).all()
    return render_template('games_page.html', games= games)


@app.route('/games/<int:id>/')
def new_page(id):
    games = Game.query.filter_by(id=id).first()
    return render_template('new_page.html', games= games)


@app.route('/registration/', methods=['GET', 'POST'])
def registration_page(Buyer=None):
    users_list = set()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        age = request.form['age']
        users_all = Buyer.query.all()
        for Buyer in users_all:
            users_list.add(Buyer.username)
        if username in users_list:
            error = 'Такой пользователь уже существует'
            return render_template('registration_page.html', error = error)
        elif repeat_password != password:
            error = 'Пароли не совпадают'
            return render_template('registration_page.html', error = error)
        elif int(age) < 18:
            error = 'Вы должны быть старше 18'
            return render_template('registration_page.html', error = error)
        else:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            buyer = Buyer(username = username, password = hashed_password, age = age)
            db.session.add(buyer)
            db.session.commit()
            return render_template('registration_page.html',
                                   error='вы зарегистрированы')
    else:
        return render_template('registration_page.html')

@app.route('/login/', methods=['GET', 'POST'])
def login_view():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        buyer = Buyer.query.filter_by(username = username).first()
        if buyer.password == hashed_password:
            login_user(buyer)
            return render_template('login_view.html', buyer = username)
        else:
            error = 'Неправильное имя пользователя или пароль'
            return render_template('login_view.html', error = error)
    else:
        return render_template('login_view.html')


@app.route('/logout/')
def logout():
    logout_user()
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)