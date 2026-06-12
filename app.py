<<<<<<< HEAD
from flask import Flask, redirect, url_for, render_template, request, session, send_from_directory
from functools import wraps
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here' 
=======
"""
HealthSync — Akıllı Hastane Yönetim Sistemi
v2.4.1 — Production Build
"""
from flask import Flask, redirect, url_for, render_template, request, session, jsonify, send_from_directory
from functools import wraps
import os
from werkzeug.utils import secure_filename
from lxml import etree  # XXE için gerekli güvensiz XML kütüphanesi

app = Flask(__name__)
app.secret_key = 'hs_9k2m_2026'
>>>>>>> a00a62a (all lab completly updated)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'php'}
SIMPLE_USERNAME = 'magnus'
SIMPLE_PASSWORD = 'superman'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

<<<<<<< HEAD
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

=======

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


>>>>>>> a00a62a (all lab completly updated)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('upload_login'))
        return f(*args, **kwargs)
    return decorated_function

<<<<<<< HEAD
=======

>>>>>>> a00a62a (all lab completly updated)
@app.route('/')
def index():
    return render_template("index.html")

<<<<<<< HEAD
=======

>>>>>>> a00a62a (all lab completly updated)
@app.route('/robots.txt')
def robots():
    return """User-agent: *
Disallow: /api/
Disallow: /uploads/
<<<<<<< HEAD
""", 200, {'Content-Type': 'text/plain'}

=======
Disallow: /config/
# HealthSync internal sitemap — DO NOT MODIFY
# Last reviewed: 2026-05-14 — M. Vinter
""", 200, {'Content-Type': 'text/plain'}


@app.route('/api/')
def api_index():
    """API dokümantasyon sayfası — keşif için breadcrumb."""
    return jsonify({
        "service": "HealthSync REST API v1.0",
        "status": "operational",
        "endpoints": {
            "/api/appointment/check": "POST — Randevu durumu sorgulama (XML)",
            "/api/health": "GET — Servis sağlık kontrolü",
        },
        "note": "Tüm API çağrıları için Content-Type: application/xml gereklidir."
    })


# --- XXE ZAAFİYETİNİN BULUNDUĞU ENDPOINT ---
@app.route('/api/appointment/check', methods=['POST'])
def check_appointment():
    try:
        # Dış varlıkların (External Entities) çözümlenmesine izin veriyoruz (XXE)
        parser = etree.XMLParser(resolve_entities=True, load_dtd=True, no_network=False)
        root = etree.fromstring(request.data, parser=parser)
        id_element = root.find('id')

        if id_element is not None and id_element.text:
            return jsonify({
                "found": False,
                "message": f"Randevu ID '{id_element.text}' sistemde bulunamadı."
            }), 200
        return jsonify({"found": False, "message": "Geçersiz XML yapısı."}), 400
    except Exception as e:
        return jsonify({"found": False, "message": f"Sistem Hatası: {str(e)}"}), 500


@app.route('/config/')
def config_page():
    """Sahte config paneli — sadece breadcrumb amaçlı."""
    return jsonify({
        "error": "Access Denied",
        "message": "Configuration panel is restricted to internal network (172.20.0.0/24).",
        "hint": "Contact your system administrator: magnus@healthsync.local",
        "reference": "CONFIG-2026-05-14"
    }), 403


>>>>>>> a00a62a (all lab completly updated)
@app.route('/uploads/login', methods=['GET', 'POST'])
def upload_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
<<<<<<< HEAD
        
=======

>>>>>>> a00a62a (all lab completly updated)
        if username == SIMPLE_USERNAME and password == SIMPLE_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_dashboard'))
        else:
            return render_template('upload_login.html', error='Geçersiz kullanıcı adı veya şifre'), 401
<<<<<<< HEAD
    
    return render_template('upload_login.html')

=======

    return render_template('upload_login.html')


>>>>>>> a00a62a (all lab completly updated)
@app.route('/uploads')
@login_required
def upload_dashboard():
    files = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    files = [f for f in files if not f.startswith('.')]
    return render_template('upload_dashboard.html', files=files)

<<<<<<< HEAD
=======

>>>>>>> a00a62a (all lab completly updated)
@app.route('/uploads/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return {'error': 'Dosya seçilmedi'}, 400
<<<<<<< HEAD
    
    file = request.files['file']
    
    if file.filename == '':
        return {'error': 'Dosya seçilmedi'}, 400
    
=======

    file = request.files['file']

    if file.filename == '':
        return {'error': 'Dosya seçilmedi'}, 400

>>>>>>> a00a62a (all lab completly updated)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return {'success': f'{filename} başarıyla yüklendi'}, 200
<<<<<<< HEAD
    
    return {'error': 'İzin verilmeyen dosya türü'}, 400

=======

    return {'error': 'İzin verilmeyen dosya türü'}, 400


>>>>>>> a00a62a (all lab completly updated)
@app.route('/uploads/logout')
def upload_logout():
    session.pop('logged_in', None)
    return redirect(url_for('upload_login'))

<<<<<<< HEAD
@app.route('/health')
def health():
    return {'status': 'ok'}
=======

# Yüklenen dosyalara erişim — webshell çalıştırmak için gerekli
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'healthsync-webapp', 'version': '2.4.1'}

>>>>>>> a00a62a (all lab completly updated)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
