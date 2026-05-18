import os
import json
import io
from datetime import datetime
from functools import wraps
from urllib.parse import urlparse
from flask import (Flask, render_template, request, redirect, url_for, session, flash, send_file, abort)
import mysql.connector
from xhtml2pdf import pisa

# ======================================================
# FLASK CONFIG
# ======================================================

app = Flask(__name__)
app.secret_key = 'ganti_secret_key_ini'

# ======================================================
# DATABASE CONFIG
# ======================================================

DB_CONFIG = {
    'host': os.getenv('MYSQLHOST'),
    'port': int(os.getenv('MYSQLPORT', 3306)),
    'user': os.getenv('MYSQLUSER'),
    'password': os.getenv('MYSQLPASSWORD'),
    'database': os.getenv('MYSQLDATABASE')
}


# ======================================================
# JENIS SURAT
# ======================================================

JENIS_SURAT = {
    'sptjm': 'SPTJM',
    'laporan_kegiatan': 'Laporan Kegiatan',
    'nota_dinas': 'Nota Dinas',
    'surat_pernyataan': 'Surat Pernyataan',
    'daftar_pengeluaran_rill': 'Daftar Pengeluaran Rill'
}

# ======================================================
# DATABASE CONNECTION
# ======================================================

def db():
    return mysql.connector.connect(**DB_CONFIG)

# ======================================================
# LOGIN REQUIRED
# ======================================================

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'user_id' not in session:
            return redirect(url_for('login'))

        return f(*args, **kwargs)

    return wrapper

# ======================================================
# CURRENT USER
# ======================================================

def current_user():

    if 'user_id' not in session:
        return None

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute(
        'SELECT * FROM users WHERE id=%s',
        (session['user_id'],)
    )

    user = cur.fetchone()

    cur.close()
    con.close()

    return user

# ======================================================
# DEFAULT DATA
# ======================================================

def default_data(jenis):

    base = {

        # UMUM
        'nama': '',
        'nip': '',

        # FIX INI WAJIB
        'pangkat_gol': '',

        'jabatan': '',
        'unit_organisasi': '',

        # NOTA DINAS
        'nomor_surat': '',
        'tanggal': '',
        'kepada': '',
        'hal': '',
        'lampiran': '',
        'kegiatan': '',
        'nomor_tugas': '',
        'tanggal_tugas': '',
        'nominal': '',

        # ISI
        'isi_pernyataan': '',

        # TTD
        'ttd_tempat': 'Pangkalan Brandan',
        'ttd_tanggal': '',
        'ttd_nama': '',
        'ttd_nip': '',

        # MENGETAHUI
        'menyetujui_nama': '',
        'menyetujui_nip': '',
        
        # KHUSUS DAFTAR PENGELUARAN RILL
        'mengetahui_nama': '',
        'mengetahui_nip': '',

        # KETERANGAN
        'keterangan': ''
    }

    # ==================================================
    # SPTJM
    # ==================================================

    if jenis == 'sptjm':

        base.update({

            'kegiatan': '',
            'biaya_perjalanan': '',
            'biaya_perjalanan_terbilang': '',
            'rute': 'Pangkalan Brandan - Medan',
            'spd_nomor': '',

            'rincian': [

                {
                    'uraian': 'Uang Harian',
                    'jumlah': '',
                    'keterangan': ''
                },

                {
                    'uraian': 'Transport',
                    'jumlah': '',
                    'keterangan': ''
                }

            ],

            'telah_dibayarkan': '',
            'telah_dibayarkan_terbilang': '',

            'bendahara_nama': 'Inal Pratama Tarigan',
            'bendahara_nip': '199702172017121002',

            'penerima_nama': '',

             # FIX BARU
             'penerima_tanggal': '',

            'ditetapkan': '0',
            'dibayarkan_semula': '0',
            'sisa': '0',

            'ppk_nama': 'Munawir Sajalai',
            'ppk_nip': '198712252020121001'

        })

    # ==================================================
    # LAPORAN KEGIATAN
    # ==================================================

    elif jenis == 'laporan_kegiatan':

         base.update({

        # ==========================================
        # DATA DIPA
        # ==========================================

        'nomor_dipa': '',
        'tanggal_dipa': '',

        # ==========================================
        # TEMPAT
        # ==========================================

        'tempat': '',

        # ==========================================
        # ISI LAPORAN
        # ==========================================

        'uraian_kegiatan': '',
        'hasil_tindak_lanjut': '',

        # ==========================================
        # PETUGAS
        # ==========================================

        'petugas': [],

        # ==========================================
        # PELAKSANA SPD
        # ==========================================

        'pelaksana_nama': '',
        'pelaksana_nip': '',

        # ==========================================
        # FIX TTD BARU KIRI KANAN
        # ==========================================

        'ttd_kiri_nama': '',
        'ttd_kiri_jabatan': '',

        'ttd_kanan_nama': '',
        'ttd_kanan_jabatan': ''

    })

    # ==================================================
    # NOTA DINAS
    # ==================================================

    elif jenis == 'nota_dinas':

        base.update({

            'unit_organisasi': '',
            'isi_pernyataan': '',

            # FIX YANG HILANG
            'kepada': '',
            'hal': '',
            'lampiran': '',
            'kegiatan': '',
            'nomor_tugas': '',
            'tanggal_tugas': '',
            'nominal': '',

            'menyetujui_nama': '',
            'menyetujui_nip': ''

        })

    # ==================================================
    # SURAT PERNYATAAN
    # ==================================================

    elif jenis == 'surat_pernyataan':

        base.update({

            'unit_organisasi': '',
            'isi_pernyataan': '',

            'menyetujui_nama': '',
            'menyetujui_nip': ''

        })

    # ==================================================
    # DAFTAR PENGELUARAN RILL
    # ==================================================

    elif jenis == 'daftar_pengeluaran_rill':

        base.update({

        'pengeluaran': [

            {
                'uraian': 'Uang Harian',
                'jumlah': ''
            }

        ],

        # PPK / MENGETAHUI
        'mengetahui_nama': '',
        'mengetahui_nip': '',

        # BACKUP FIELD LAMA
        'ppk_nama': '',
        'ppk_nip': ''

    })
    return base
# ======================================================
# PARSE FORM
# ======================================================

def parse_form(jenis):

    data = default_data(jenis)

    # ==================================================
    # AMBIL INPUT NORMAL
    # ==================================================

    for k in data.keys():

        # SKIP ARRAY
        if k in [
            'rincian',
            'petugas',
            'pengeluaran'
        ]:
            continue

        # ==============================================
        # FIX KHUSUS RICH TEXT EDITOR
        # ==============================================

        if k == 'isi_pernyataan':

            isi_html = request.form.get(
                'isi_pernyataan',
                ''
            )

            # FIX QUILL KOSONG
            if isi_html == '<p><br></p>':
                isi_html = ''

            data['isi_pernyataan'] = isi_html

        else:

            data[k] = request.form.get(
                k,
                data[k]
            )

    # ==================================================
    # SPTJM
    # ==================================================

    if jenis == 'sptjm':

        uraian = request.form.getlist(
            'rincian_uraian[]'
        )

        jumlah = request.form.getlist(
            'rincian_jumlah[]'
        )

        ket = request.form.getlist(
            'rincian_keterangan[]'
        )

        data['rincian'] = [

            {
                'uraian': u,
                'jumlah': j,
                'keterangan': k
            }

            for u, j, k in zip(
                uraian,
                jumlah,
                ket
            )

            if u or j or k

        ]

    # ==================================================
    # LAPORAN KEGIATAN
    # ==================================================

    elif jenis == 'laporan_kegiatan':

        nama = request.form.getlist(
            'petugas_nama[]'
        )

        nip = request.form.getlist(
            'petugas_nip[]'
        )

        pangkat = request.form.getlist(
            'petugas_pangkat_gol[]'
        )

        jabatan = request.form.getlist(
            'petugas_jabatan[]'
        )

        data['petugas'] = [

            {
                'nama': a,
                'nip': b,
                'pangkat_gol': c,
                'jabatan': d
            }

            for a, b, c, d in zip(
                nama,
                nip,
                pangkat,
                jabatan
            )

            if a or b or c or d

        ]

    # ==================================================
    # DAFTAR PENGELUARAN RILL
    # ==================================================

    elif jenis == 'daftar_pengeluaran_rill':

        uraian = request.form.getlist(
            'pengeluaran_uraian[]'
        )

        jumlah = request.form.getlist(
            'pengeluaran_jumlah[]'
        )

        data['pengeluaran'] = [

            {
                'uraian': u,
                'jumlah': j
            }

            for u, j in zip(
                uraian,
                jumlah
            )

            if u or j

        ]

    return data

# ======================================================
# GET SURAT
# ======================================================

def get_surat_or_404(id):

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute(
        'SELECT * FROM surat WHERE id=%s',
        (id,)
    )

    row = cur.fetchone()

    cur.close()
    con.close()

    if not row:
        abort(404)

    # ==================================================
    # FIX JSON ERROR
    # ==================================================

    try:

        row['data_dict'] = json.loads(row['data'])

    except:

        row['data_dict'] = {}

    return row

# ======================================================
# LOGIN
# ======================================================

@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        con = db()
        cur = con.cursor(dictionary=True)

        cur.execute(
            'SELECT * FROM users WHERE username=%s AND password=%s',
            (username, password)
        )

        user = cur.fetchone()

        cur.close()
        con.close()

        if user:

            session['user_id'] = user['id']
            session['nama_lengkap'] = user['nama_lengkap']

            return redirect(url_for('dashboard'))

        flash('Username atau password salah')

    return render_template('login.html')

# ======================================================
# LOGOUT
# ======================================================

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

# ======================================================
# DASHBOARD
# ======================================================

@app.route('/dashboard')
@login_required
def dashboard():

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute('SELECT COUNT(*) total FROM surat')
    total = cur.fetchone()['total']

    cur.execute(
        "SELECT COUNT(*) total FROM surat WHERE status='Selesai'"
    )

    selesai = cur.fetchone()['total']

    cur.execute(
        "SELECT COUNT(*) total FROM surat WHERE status='Draft'"
    )

    draft = cur.fetchone()['total']

    cur.execute(
        'SELECT * FROM surat ORDER BY id DESC LIMIT 6'
    )

    latest = cur.fetchall()

    cur.close()
    con.close()

    return render_template(

        'dashboard.html',

        user=current_user(),

        total=total,
        selesai=selesai,
        draft=draft,

        latest=latest,

        jenis_surat=JENIS_SURAT

    )

# ======================================================
# NEW SURAT
# ======================================================

@app.route('/surat/<jenis>/new', methods=['GET', 'POST'])
@login_required
def surat_new(jenis):

    if jenis not in JENIS_SURAT:
        abort(404)

    # ==================================================
    # SAVE DATA
    # ==================================================

    if request.method == 'POST':

        data = parse_form(jenis)

        judul = request.form.get(
            'judul'
        ) or JENIS_SURAT[jenis]

        status = request.form.get(
            'status',
            'Selesai'
        )

        con = db()
        cur = con.cursor()

        cur.execute('''

            INSERT INTO surat
            (

                jenis,
                judul,
                nomor_surat,
                tanggal,
                data,
                status,
                user_id

            )

            VALUES
            (%s,%s,%s,%s,%s,%s,%s)

        ''', (

            jenis,
            judul,

            data.get('nomor_surat', ''),
            data.get('tanggal', ''),

            json.dumps(
                data,
                ensure_ascii=False
            ),

            status,

            session['user_id']

        ))

        con.commit()

        new_id = cur.lastrowid

        cur.close()
        con.close()

        flash('Surat berhasil dibuat')

        return redirect(
            url_for(
                'surat_preview',
                id=new_id
            )
        )

    # ==================================================
    # FORM
    # ==================================================

    return render_template(

        'form_' + jenis + '.html',

        mode='new',

        jenis=jenis,

        title=JENIS_SURAT[jenis],

        data=default_data(jenis),

        surat=None,

        user=current_user()

    )

# ======================================================
# EDIT SURAT
# ======================================================

@app.route('/surat/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def surat_edit(id):

    surat = get_surat_or_404(id)

    jenis = surat['jenis']

    # ==================================================
    # UPDATE
    # ==================================================

    if request.method == 'POST':

        data = parse_form(jenis)

        judul = request.form.get(
            'judul'
        ) or JENIS_SURAT[jenis]

        status = request.form.get(
            'status',
            'Selesai'
        )

        con = db()
        cur = con.cursor()

        cur.execute('''

            UPDATE surat

            SET

                judul=%s,
                nomor_surat=%s,
                tanggal=%s,
                data=%s,
                status=%s

            WHERE id=%s

        ''', (

            judul,

            data.get('nomor_surat', ''),
            data.get('tanggal', ''),

            json.dumps(
                data,
                ensure_ascii=False
            ),

            status,

            id

        ))

        con.commit()

        cur.close()
        con.close()

        flash('Surat berhasil diperbarui')

        return redirect(
            url_for(
                'surat_preview',
                id=id
            )
        )

    # ==================================================
    # FORM EDIT
    # ==================================================

    return render_template(

        'form_' + jenis + '.html',

        mode='edit',

        jenis=jenis,

        title=JENIS_SURAT[jenis],

        data=surat['data_dict'],

        surat=surat,

        user=current_user()

    )

# ======================================================
# PREVIEW
# ======================================================

@app.route('/surat/<int:id>')
@login_required
def surat_preview(id):

    surat = get_surat_or_404(id)

    return render_template(

        'preview_' + surat['jenis'] + '.html',

        surat=surat,

        data=surat['data_dict'],

        user=current_user()

    )
    
    
# ======================================================
# PDF HELPER
# ======================================================

def clean_filename(text):
    text = str(text or 'dokumen')
    aman = ''

    for ch in text:
        if ch.isalnum() or ch in ['-', '_']:
            aman += ch
        elif ch == ' ':
            aman += '_'

    return aman.strip('_') or 'dokumen'


def normalize_jenis(jenis):
    return str(jenis or '').strip().lower()


def find_logo_static_path():
    candidates = [
        'logo.png',
        'logo.jpg',
        'logo.jpeg',

        'img/logo.png',
        'img/logo.jpg',
        'img/logo.jpeg',

        'images/logo.png',
        'images/logo.jpg',
        'images/logo.jpeg',

        'assets/logo.png',
        'assets/logo.jpg',
        'assets/logo.jpeg'
    ]

    for item in candidates:
        full_path = os.path.join(app.root_path, 'static', item)

        if os.path.isfile(full_path):
            return '/static/' + item.replace('\\', '/')

    return ''


def link_callback(uri, rel):
    from urllib.parse import urlparse

    parsed = urlparse(uri)
    path = parsed.path

    if path.startswith('/static/'):
        full_path = os.path.join(
            app.root_path,
            path.lstrip('/')
        )

        if os.path.isfile(full_path):
            return full_path

    if uri.startswith('static/'):
        full_path = os.path.join(
            app.root_path,
            uri
        )

        if os.path.isfile(full_path):
            return full_path

    return uri

# ======================================================
# PDF
# ======================================================

@app.route('/surat/<int:id>/pdf')
@login_required
def surat_pdf(id):

    surat = get_surat_or_404(id)
    data = surat['data_dict']

    jenis = normalize_jenis(surat.get('jenis'))

    # PENTING:
    # Ini dibuat fleksibel karena kadang database/server menyimpan typo:
    # daftar_pengeluaran_rill / daftar_pengeluaran_riil / daftar_pengeluaran_ril
    if jenis in [
        'daftar_pengeluaran_rill',
        'daftar_pengeluaran_riil',
        'daftar_pengeluaran_ril'
    ]:
        template_pdf = 'pdf_daftar_pengeluaran_rill.html'
        pdf_title = 'Daftar Pengeluaran Riil'
        pdf_filename_prefix = 'daftar_pengeluaran_riil'
    else:
        # Untuk jenis lain sementara masih pakai preview.
        # Nanti sebaiknya dibuat template PDF khusus juga.
        template_pdf = 'preview_' + jenis + '.html'
        pdf_title = 'Document Generator'
        pdf_filename_prefix = jenis or 'dokumen'

    logo_src = find_logo_static_path()

    print('================ PDF DEBUG ================')
    print('SURAT ID       :', id)
    print('JENIS DATABASE :', surat.get('jenis'))
    print('JENIS NORMAL   :', jenis)
    print('TEMPLATE PDF   :', template_pdf)
    print('LOGO SRC       :', logo_src)
    print('===========================================')

    html = render_template(
        template_pdf,
        surat=surat,
        data=data,
        pdf=True,
        logo_src=logo_src,
        pdf_title=pdf_title,
        user=current_user()
    )

    pdf = io.BytesIO()

    result = pisa.CreatePDF(
        src=io.StringIO(html),
        dest=pdf,
        encoding='utf-8',
        link_callback=link_callback
    )

    if result.err:
        print('PDF ERROR:', result.err)
        abort(500, 'PDF gagal dibuat. Periksa template PDF.')

    pdf.seek(0)

    nama_file = clean_filename(
        data.get('nama') or surat.get('judul') or pdf_filename_prefix
    )

    download = request.args.get('download') == '1'

    response = send_file(
        pdf,
        as_attachment=download,
        download_name=f"{pdf_filename_prefix}_{nama_file}.pdf",
        mimetype='application/pdf'
    )

    # Supaya browser/Railway tidak nampilin PDF cache lama
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

# ======================================================
# DELETE
# ======================================================

@app.route('/surat/<int:id>/delete', methods=['POST'])
@login_required
def surat_delete(id):

    con = db()
    cur = con.cursor()

    cur.execute(
        'DELETE FROM surat WHERE id=%s',
        (id,)
    )

    con.commit()

    cur.close()
    con.close()

    flash('Surat berhasil dihapus')

    return redirect(url_for('arsip'))

# ======================================================
# ARSIP DENGAN PAGINATION
# ======================================================

@app.route('/arsip')
@login_required
def arsip():

    q = request.args.get('q', '').strip()
    jenis = request.args.get('jenis', '').strip()
    status = request.args.get('status', '').strip()

    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1

    try:
        per_page = int(request.args.get('per_page', 10))
    except:
        per_page = 10

    if page < 1:
        page = 1

    # Batasi agar tidak terlalu berat
    if per_page < 5:
        per_page = 5

    if per_page > 50:
        per_page = 50

    where = ' WHERE 1=1 '
    params = []

    if q:
        where += '''
            AND
            (
                judul LIKE %s
                OR nomor_surat LIKE %s
                OR tanggal LIKE %s
            )
        '''

        params += [
            f'%{q}%',
            f'%{q}%',
            f'%{q}%'
        ]

    if jenis:
        where += ' AND jenis=%s '
        params.append(jenis)

    if status:
        where += ' AND status=%s '
        params.append(status)

    con = db()
    cur = con.cursor(dictionary=True)

    # Hitung total semua data sesuai filter
    count_sql = 'SELECT COUNT(*) AS total FROM surat ' + where

    cur.execute(count_sql, params)

    total_data = cur.fetchone()['total']

    total_pages = (total_data + per_page - 1) // per_page

    if total_pages < 1:
        total_pages = 1

    if page > total_pages:
        page = total_pages

    offset = (page - 1) * per_page

    # Ambil data sesuai halaman
    data_sql = '''
        SELECT *
        FROM surat
    ''' + where + '''
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    '''

    cur.execute(
        data_sql,
        params + [per_page, offset]
    )

    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template(

        'arsip.html',

        rows=rows,

        jenis_surat=JENIS_SURAT,

        user=current_user(),

        q=q,
        jenis=jenis,
        status=status,

        page=page,
        per_page=per_page,
        total_data=total_data,
        total_pages=total_pages,
        start_no=offset + 1

    )
# ======================================================
# PENGATURAN
# ======================================================

@app.route('/pengaturan', methods=['GET', 'POST'])
@login_required
def pengaturan():

    user = current_user()

    if request.method == 'POST':

        nama = request.form['nama_lengkap']
        username = request.form['username']
        password = request.form['password']

        con = db()
        cur = con.cursor()

        cur.execute(

            '''
            UPDATE users

            SET

                nama_lengkap=%s,
                username=%s,
                password=%s

            WHERE id=%s
            ''',

            (
                nama,
                username,
                password,
                user['id']
            )

        )

        con.commit()

        cur.close()
        con.close()

        session['nama_lengkap'] = nama

        flash('Akun berhasil diperbarui')

        return redirect(url_for('pengaturan'))

    return render_template(

        'pengaturan.html',

        user=user

    )
    
  # ======================================================
# CATATAN NO SURAT
# ======================================================

def get_catatan_no_surat(q=''):

    con = db()
    cur = con.cursor(dictionary=True)

    sql = 'SELECT * FROM catatan_no_surat WHERE 1=1'
    params = []

    if q:
        sql += '''
            AND
            (
                no_surat LIKE %s
                OR keterangan LIKE %s
            )
        '''

        params += [
            f'%{q}%',
            f'%{q}%'
        ]

    sql += ' ORDER BY id DESC'

    cur.execute(sql, params)

    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


@app.route('/no-surat', methods=['GET', 'POST'])
@login_required
def no_surat():

    if request.method == 'POST':

        no_surat_value = request.form.get('no_surat', '').strip()
        keterangan = request.form.get('keterangan', '').strip()

        if not no_surat_value:
            flash('No surat wajib diisi')
            return redirect(url_for('no_surat'))

        con = db()
        cur = con.cursor()

        cur.execute(
            '''
            INSERT INTO catatan_no_surat
            (
                no_surat,
                keterangan
            )
            VALUES
            (%s, %s)
            ''',
            (
                no_surat_value,
                keterangan
            )
        )

        con.commit()

        cur.close()
        con.close()

        flash('Catatan no surat berhasil ditambahkan')

        return redirect(url_for('no_surat'))

    q = request.args.get('q', '').strip()

    rows = get_catatan_no_surat(q)

    return render_template(
        'no_surat.html',
        rows=rows,
        q=q,
        edit_row=None,
        user=current_user()
    )


@app.route('/no-surat/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def no_surat_edit(id):

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute(
        'SELECT * FROM catatan_no_surat WHERE id=%s',
        (id,)
    )

    edit_row = cur.fetchone()

    if not edit_row:
        cur.close()
        con.close()
        abort(404)

    if request.method == 'POST':

        no_surat_value = request.form.get('no_surat', '').strip()
        keterangan = request.form.get('keterangan', '').strip()

        if not no_surat_value:
            flash('No surat wajib diisi')
            cur.close()
            con.close()
            return redirect(url_for('no_surat_edit', id=id))

        cur.execute(
            '''
            UPDATE catatan_no_surat
            SET
                no_surat=%s,
                keterangan=%s
            WHERE id=%s
            ''',
            (
                no_surat_value,
                keterangan,
                id
            )
        )

        con.commit()

        cur.close()
        con.close()

        flash('Catatan no surat berhasil diperbarui')

        return redirect(url_for('no_surat'))

    cur.close()
    con.close()

    q = request.args.get('q', '').strip()
    rows = get_catatan_no_surat(q)

    return render_template(
        'no_surat.html',
        rows=rows,
        q=q,
        edit_row=edit_row,
        user=current_user()
    )


@app.route('/no-surat/<int:id>/delete', methods=['POST'])
@login_required
def no_surat_delete(id):

    con = db()
    cur = con.cursor()

    cur.execute(
        'DELETE FROM catatan_no_surat WHERE id=%s',
        (id,)
    )

    con.commit()

    cur.close()
    con.close()

    flash('Catatan no surat berhasil dihapus')

    return redirect(url_for('no_surat'))


@app.route('/no-surat/pdf')
@login_required
def no_surat_pdf():

    q = request.args.get('q', '').strip()

    rows = get_catatan_no_surat(q)

    html = render_template(
        'pdf_no_surat.html',
        rows=rows,
        q=q,
        tanggal_cetak=datetime.now().strftime('%d-%m-%Y %H:%M'),
        user=current_user()
    )

    pdf = io.BytesIO()

    result = pisa.CreatePDF(
        src=io.StringIO(html),
        dest=pdf,
        encoding='utf-8',
        link_callback=link_callback
    )

    if result.err:
        abort(500, 'PDF catatan no surat gagal dibuat.')

    pdf.seek(0)

    return send_file(
        pdf,
        as_attachment=True,
        download_name='daftar_catatan_no_surat.pdf',
        mimetype='application/pdf'
    )

# ======================================================
# FILTER RUPIAH
# ======================================================

@app.template_filter('rupiah')
def rupiah(v):

    s = str(v or '0') \
        .replace('.', '') \
        .replace(',', '') \
        .strip()

    try:

        n = int(s)

    except:

        return v

    return 'Rp. ' + f'{n:,}'.replace(',', '.')

# ======================================================
# RUN APP
# ======================================================

if __name__ == '__main__':

    app.run(debug=True)
