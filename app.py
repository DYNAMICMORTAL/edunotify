from flask import Flask, render_template, request, redirect, session, url_for
import boto3
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "super-secret-key"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('EduNotify-Notices')


@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        email = request.form['email']

        if user_id == 'professor' and email == 'professor@Apsit':
            session['user'] = 'admin'
            return redirect('/admin')
        elif email == f"{user_id}@Apsit":
            session['user'] = user_id  # student ID
            session['email'] = email
            return redirect('/student')
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/admin')
def admin_dashboard():
    if session.get('user') != 'admin':
        return redirect('/login')

    response = table.scan()
    notices = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)
    return render_template('admin.html', notices=notices)


@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    if not session.get('user') or session.get('user') == 'admin':
        return redirect('/login')

    if request.method == 'POST':
        dept = request.form['department']
        year = request.form['year']
        response = table.scan()
        filtered = [n for n in response['Items'] if n['department'] == dept and n['year'] == year]
        notices = sorted(filtered, key=lambda x: x['timestamp'], reverse=True)
        return render_template('student.html', notices=notices, selected=True, dept=dept, year=year)

    return render_template('student.html', notices=[], selected=False)


@app.route('/post', methods=['POST'])
def post_notice():
    if session.get('user') != 'admin':
        return redirect('/login')

    notice = {
        'id': str(uuid.uuid4()),
        'title': request.form['title'],
        'description': request.form['description'],
        'department': request.form['department'],
        'year': request.form['year'],
        'timestamp': datetime.now().isoformat()
    }
    table.put_item(Item=notice)
    return redirect('/admin')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
