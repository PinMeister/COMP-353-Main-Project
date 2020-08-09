from flask import Flask, flash, render_template,session, abort, url_for, redirect, request, session
from flask_bootstrap import Bootstrap
from db_connection import *

app = Flask(__name__)
bootstrap = Bootstrap()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete_application', methods=['GET', 'POST'])
def del_application():
    if request.method == 'POST':
        application_id = request.form['application_id']
        remove_job_application(application_id)
        return applied_jobs()


@app.route('/applied_jobs')
def applied_jobs():
    email = session['email']
    return render_template('applied-jobs-results.html', list_of_job_applications=get_job_applications(email))


@app.route('/employer_postings')
def employer_postings():
    email = session['email']
    return render_template('employer-postings.html', list_of_job_postings=get_job_postings(email))


@app.route('/modify_posting/<posting_id>', methods=['GET', 'POST'])
def modify_posting(posting_id):
    if request.method == 'POST':
        job_title = request.form['job_title']
        description = request.form['description']
        category = request.form['category']
        modify_job_posting(posting_id, job_title, description, category)
        return redirect('/employer_postings')
    else:
        return render_template('modify_posting.html')


@app.route('/delete_posting/<posting_id>', methods=['GET', 'POST'])
def delete_posting(posting_id):
    if request.method == 'POST':
        remove_job_posting(posting_id)
        return redirect('/employer_postings')


@app.route('/view_applications/<posting_id>', methods=['GET', 'POST'])
def view_applications(posting_id):
    return render_template('view-applications.html', list_of_applications=get_applications_by_posting(posting_id))


@app.route('/user-profile')
def user_profile():
    return render_template('user-profile.html')


@app.route('/modify_user_profile', methods=['GET', 'POST'])
def change_user_profile():
    return render_template('user-profile.html')


@app.route('/delete_user_account', methods=['POST', 'GET'])
def delete_user_account():
    email = session['email']
    delete_account(email)
    return redirect(url_for('index'))


@app.route('/modify_password', methods=['POST', 'GET'])
def change_user_password():
    email = session['email']
    password = request.form['new_password']
    print(password)
    if password != "":
        change_password(email, password)
    return render_template('user-profile.html')


@app.route('/modify_name', methods=['POST', 'GET'])
def change_user_name():
    email = session['email']
    new_name = request.form['new_name']
    if new_name != "":
        change_name(email, new_name)
    return render_template('user-profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    # form fields
    if request.method == 'POST':

        email = request.form['username']
        password = request.form['password']
        account = get_login(email,password)

        if account:
            session['logged_In'] = True
            session['userID'] = account[0]
            session['email'] = account[1]
            session['user_type'] = account[5]
            session['is_admin'] = account[6]
            flash('logged in successfully')
            return redirect(url_for('index'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    error = None
    # form fields
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = get_forgotten(email, name)
        flash('password is: ' + str(password[0]))
    else:
        error = 'Invalid Credentials. Please try again.'
    return render_template('forgot.html', error=error)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('registration.html', error=error)


@app.route('/users')
def users():
    return render_template('users.html', list_of_users=get_all_users())


@app.route('/logout')
def logout():
    session.pop('userID', None)
    session.pop('email', None)
    session.pop('logged_In', None)
    flash('You are logged out.')
    session['logged_In'] = False
    return redirect('/')


@app.route('/postings', methods=['GET', 'POST'])
def postings():
    title = ""
    category = ""
    if request.method == 'POST':
        title = request.form['title_search']
        category = request.form['category_search']
    return render_template('postings.html', list_of_postings=search_postings(title, category))


@app.route('/add_job_application', methods=['GET', 'POST'])
def add_job_application():
    if request.method == 'POST':
        posting_id = request.form['posting_id']
        email = request.form['email']
        add_application_job(posting_id, email)
        return redirect('/applied_jobs')
    else:
        return render_template('add_job_application.html')


@app.route('/add_job_posting', methods=['GET', 'POST'])
def add_job_posting():
    if request.method == 'POST':
        email = session['email']
        job_title = request.form['job_title']
        description = request.form['description']
        category = request.form['category']
        add_posting_job(email, job_title, description, category)
        return redirect('/employer_postings')
    else:
        return render_template('add_job_posting.html')


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)

