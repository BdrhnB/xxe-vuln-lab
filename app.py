"""
HealthSync — Smart Hospital Management System
v2.4.1 — Production Build
"""
from flask import Flask, redirect, url_for, render_template, request, session, jsonify, send_from_directory
from functools import wraps
import os
from werkzeug.utils import secure_filename
from lxml import etree

app = Flask(__name__)
app.secret_key = 'hs_9k2m_2026'

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
Disallow: /config/
# HealthSync internal sitemap — DO NOT MODIFY
# Last reviewed: 2026-05-14 — M. Vinter
""", 200, {'Content-Type': 'text/plain'}


@app.route('/api/')
def api_index():
    return jsonify({
        "service": "HealthSync REST API v1.0",
        "status": "operational",
        "endpoints": {
            "/api/appointment/check": "POST — Appointment status lookup (XML)",
            "/api/health": "GET — Service health check",
        },
        "note": "All API calls require Content-Type: application/xml."
    })


# --- XXE VULNERABILITY ENDPOINT ---
@app.route('/api/appointment/check', methods=['POST'])
def check_appointment():
    try:
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
        root = etree.fromstring(request.data, parser=parser)
        id_element = root.find('id')

        if id_element is not None and id_element.text:
            return jsonify({
                "found": False,
                "message": f"Appointment ID '{id_element.text}' not found in the system."
            }), 200
        return jsonify({"found": False, "message": "Invalid XML structure."}), 400
    except Exception as e:
        return jsonify({"found": False, "message": f"System Error: {str(e)}"}), 500


@app.route('/config/')
def config_page():
    return jsonify({
        "error": "Access Denied",
        "message": "Configuration loaded from /etc/healthsync/app.conf — restricted to internal network (172.20.0.0/24).",
        "hint": "Contact your system administrator: magnus@healthsync.local",
        "reference": "CONFIG-2026-05-14"
    }), 403


@app.route('/uploads/login', methods=['GET', 'POST'])
def upload_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == SIMPLE_USERNAME and password == SIMPLE_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_dashboard'))
        else:
            return render_template('upload_login.html', error='Invalid username or password'), 401

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
        return {'error': 'No file selected'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': 'No file selected'}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return {'success': f'{filename} uploaded successfully'}, 200

    return {'error': 'File type not allowed'}, 400


@app.route('/uploads/logout')
def upload_logout():
    session.pop('logged_in', None)
    return redirect(url_for('upload_login'))


# Serve uploaded files — needed for webshell execution
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'healthsync-webapp', 'version': '2.4.1'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
