from flask import Flask, render_template, request, redirect, session
import boto3
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secret-key"

# AWS setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('EduNotify-Notices')
s3 = boto3.client('s3', region_name='us-east-1')
S3_BUCKET = 'edunotify-attachments'

# 🔐 Login route
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['userid']
        email = request.form['email']

        if user_id == 'professor' and email == 'professor@Apsit':
            session['user'] = 'admin'
            return redirect('/dashboard')
        elif email == f"{user_id}@Apsit":
            session['user'] = user_id
            session['email'] = email
            return redirect('/view-notices')
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# 👨‍🏫 Admin Dashboard Overview
@app.route('/dashboard')
def dashboard():
    if session.get('user') != 'admin':
        return redirect('/login')
    return render_template('dashboard.html')


# 📢 Post a new notice
@app.route('/post-notice', methods=['GET', 'POST'])
def post_notice():
    if session.get('user') != 'admin':
        return redirect('/login')

    if request.method == 'POST':
        file_url = ""
        file = request.files.get('attachment')
        if file and file.filename:
            filename = secure_filename(file.filename)
            s3.upload_fileobj(file, S3_BUCKET, filename)
            file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

        notice = {
            'id': str(uuid.uuid4()),
            'title': request.form['title'],
            'description': request.form['description'],
            'department': request.form['department'],
            'year': request.form['year'],
            'priority': request.form.get('priority', 'normal'),
            'timestamp': datetime.now().isoformat(),
            'file_url': file_url
        }

        table.put_item(Item=notice)
        return redirect('/dashboard')

    return render_template('post_notice.html')


# 📃 View Notices (Student filtered or Admin full view)
@app.route('/view-notices', methods=['GET', 'POST'])
def view_notices():
    if not session.get('user'):
        return redirect('/login')

    notices = []
    if request.method == 'POST':
        dept = request.form['department']
        year = request.form['year']
        response = table.scan()
        filtered = [n for n in response['Items'] if n['department'] == dept and n['year'] == year]
        notices = sorted(filtered, key=lambda x: x['timestamp'], reverse=True)
    else:
        if session.get('user') == 'admin':
            response = table.scan()
            notices = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)

    return render_template('view_notices.html', notices=notices)


# 🎓 Student Management (Admin only)
@app.route('/students')
def manage_students():
    if session.get('user') != 'admin':
        return redirect('/login')
    return render_template('student_management.html')


if __name__ == '__main__':
    app.run(debug=True)
