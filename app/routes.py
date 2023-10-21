'''
Hackathon 2023 Team 8
Team Members: Callie Campbell-Perdomo, Sam Candaleria, Saul Gonzalez, Saul's friend, Vincent Dufour
Description: Student-made website for students containing student-crowdsourced info & reviews
'''

from app import app, db, load_user
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')


###########################################################################################################
# Start of sign in/ sign-up/ sign out 


# sign-in functionality
@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    form = SignInForm()
    if form.validate_on_submit():
        id = form.id.data
        passwd = form.passwd.data
        hashed_passwd = passwd.encode('utf-8')

        user = load_user(id)

        if user:
            if bcrypt.checkpw(hashed_passwd, user.passwd):
                login_user(user)
            else:
                return '<p>Incorrect Password!</p>'

            if user.id == "admin":
                return redirect(url_for('front_page_admin'))
            else:
                return redirect(url_for('front_page'))
        else:
            return '<p>Username not recognized!</p>'
    else:
        return render_template('users_signin.html', title=app.config['USER SIGNIN'], form=form)


# sign-up functionality
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    form = SignUpForm()
    if form.validate_on_submit():
        passwd = form.passwd.data
        passwd_confirm = form.passwd_confirm.data
        if passwd == passwd_confirm:
            hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        else:
            return '<p>Passwords do not match!</p>'
        
        new_user = User(
            id = form.id.data,
            name = form.name.data,
            about = form.about.data,
            passwd = hashed
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return render_template('users_signup.html', title=app.config['USER SIGNUP'], form=form)


# sign-out functionality
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    logout_user()
    return redirect(url_for('index'))


# End of sign in/ sign-up/ sign out 
###########################################################################################################


###########################################################################################################
# Start of user-facing routes





# End of user-facing routes 
###########################################################################################################


###########################################################################################################
# Start of admin-facing routes


@app.route('/users')
@login_required     
def list_users(): 
    users = User.query.all()
    return render_template('resellers_list.html', users=users, user=current_user)
    

# End of admin-facing routes 
###########################################################################################################
