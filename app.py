from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
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

        # Show flash message and redirect to login
        flash('You are now registered and can log in!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor and get username if it exists
        cursor = db.connection.cursor()
        result = cursor.execute('SELECT * FROM users WHERE username =%s', [username])

        if (result > 0):
            # If there is a match, get stored hash
            data = cursor.fetchone()
            # DictCursor configured above, treat like dict not tuple
            password = data['password']

            # See if the password entered by user matches the one in DB
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
        else:
            app.logger.info('NO USER')

    return render_template('login.html')


if __name__ == '__main__':
    app.run()
