from flask import Flask, render_template, request, redirect, session
import boto3
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super-secret-key"

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('EduNotify-Notices')
s3 = boto3.client('s3', region_name='us-east-1')
S3_BUCKET = 'edunotify-attachments'

dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='AKIA5CT2FOY3CPXMWS6M',
    aws_secret_access_key='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'
)
table = dynamodb.Table('EduNotify-Notices')

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id='AKIA5CT2FOY3CPXMWS6M',
    aws_secret_access_key='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'
)

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if session.get('user') != 'admin':
        return redirect('/login')
    return render_template('dashboard.html')

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

@app.route('/view-notices', methods=['GET', 'POST'])
def view_notices():
    if not session.get('user'):
        return redirect('/login')

    notices = []
    default_message = "Please use the filters above to view notices relevant to your department and year."
    try:
        if request.method == 'POST':
            dept = request.form.get('department', '')
            year = request.form.get('year', '')

            # Fetch all notices from DynamoDB
            response = table.scan()
            all_notices = response.get('Items', [])

            # Filter notices based on department and year
            notices = [
                n for n in all_notices
                if (not dept or n.get('department') == dept) and (not year or n.get('year') == str(year))
            ]
            default_message = "No notices found for the selected filters." if not notices else ""
        elif session.get('user') != 'admin':
            # Default behavior for students: show no notices until filters are applied
            notices = []
        else:
            # Fetch all notices for admin view
            response = table.scan()
            notices = response.get('Items', [])
            default_message = "No notices available." if not notices else ""

        # Sort notices by timestamp (descending)
        notices = sorted(notices, key=lambda x: x.get('timestamp', ''), reverse=True)
    except Exception as e:
        return render_template('view_notices.html', error=str(e))

    return render_template('view_notices.html', notices=notices, default_message=default_message)

@app.route('/students')
def manage_students():
    if session.get('user') != 'admin':
        return redirect('/login')
    return render_template('student_management.html')

if __name__ == '__main__':
    app.run(debug=True)