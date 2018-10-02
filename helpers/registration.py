from wtforms import Form, StringField, TextAreaField, PasswordField, validators


# RegistrationForm sets up form with validation
class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    website = StringField('Website', [
                          validators.Optional(), validators.Length(min=6, max=50)], description='(Optional)')
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords Do Not Match')
    ])
    confirm = PasswordField('Confirm Password')
