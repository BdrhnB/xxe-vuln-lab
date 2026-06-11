from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here' 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'php'}
SIMPLE_USERNAME = 'magnus'
SIMPLE_PASSWORD = 'superman'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('upload_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/robots.txt')
def robots():
    return """User-agent: *
Disallow: /api/
Disallow: /uploads/
""", 200, {'Content-Type': 'text/plain'}

@app.route('/uploads/login', methods=['GET', 'POST'])
def upload_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == SIMPLE_USERNAME and password == SIMPLE_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_dashboard'))
        else:
            return render_template('upload_login.html', error='Geçersiz kullanıcı adı veya şifre'), 401
    
    return render_template('upload_login.html')

@app.route('/uploads')
@login_required
def upload_dashboard():
    files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    files = [f for f in files if not f.startswith('.')]
    return render_template('upload_dashboard.html', files=files)

@app.route('/uploads/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return {'error': 'Dosya seçilmedi'}, 400
    
    file = request.files['file']
    
    if file.filename == '':
        return {'error': 'Dosya seçilmedi'}, 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return {'success': f'{filename} başarıyla yüklendi'}, 200
    
    return {'error': 'İzin verilmeyen dosya türü'}, 400

@app.route('/uploads/logout')
def upload_logout():
    session.pop('logged_in', None)
    return redirect(url_for('upload_login'))

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
