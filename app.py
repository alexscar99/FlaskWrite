from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
import time
from helpers import data, keys, registration


app = Flask(__name__)
app.secret_key = keys.Generate_Secret_Key()

# Config MySQL then initialize
app.config['MYSQL_HOST'] = keys.DB_Host()
app.config['MYSQL_USER'] = keys.DB_User()
app.config['MYSQL_PASSWORD'] = keys.DB_Password()
app.config['MYSQL_DB'] = keys.DB_Name()
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

db = MySQL(app)


# Set routes and define functions to render the template for that route
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about_us():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=data.Articles())

@app.route('/article/<string:id>/')
def show_article(id):
    return render_template('article.html', id=id)


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = registration.RegistrationForm(request.form)

    # Check that form is submitted and validated
    if request.method == 'POST' and form.validate():
        # Create variables to store inputs from register form
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cursor = db.connection.cursor()

        # Execute SQL query, commit to DB, then close connection
        cursor.execute('INSERT INTO users(name, email, username, password) \
        VALUES(%s, %s, %s, %s)', (name, email, username, password))
        db.connection.commit()
        cursor.close()

        # Show flash message and redirect to index (will change to login) on submission
        flash('You are now registered and can log in!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
