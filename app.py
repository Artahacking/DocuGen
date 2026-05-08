import os
import json
import io

from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
    abort
)

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

            'bendahara_nama': 'Imal Pratama Tarigan',
            'bendahara_nip': '199702172017121002',

            'penerima_nama': '',

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

            'nomor_dipa': '',
            'tanggal_dipa': '',
            'tempat': '',
            'uraian_kegiatan': '',
            'hasil_tindak_lanjut': '',

            'petugas': [],

            'pelaksana_nama': '',
            'pelaksana_nip': ''

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
    # AMBIL SEMUA INPUT BIASA
    # ==================================================

    for k in data.keys():

        if k not in ['rincian', 'petugas', 'pengeluaran']:

            data[k] = request.form.get(k, data[k])

    # ==================================================
    # FIX ISI NOTA DINAS
    # ==================================================

    data['isi_pernyataan'] = request.form.get(
        'isi_pernyataan',
        ''
    )

    # ==================================================
    # SPTJM
    # ==================================================

    if jenis == 'sptjm':

        uraian = request.form.getlist('rincian_uraian[]')
        jumlah = request.form.getlist('rincian_jumlah[]')
        ket = request.form.getlist('rincian_keterangan[]')

        data['rincian'] = [

            {
                'uraian': u,
                'jumlah': j,
                'keterangan': k
            }

            for u, j, k in zip(uraian, jumlah, ket)

            if u or j or k

        ]

    # ==================================================
    # LAPORAN KEGIATAN
    # ==================================================

    if jenis == 'laporan_kegiatan':

        nama = request.form.getlist('petugas_nama[]')
        nip = request.form.getlist('petugas_nip[]')
        pangkat = request.form.getlist('petugas_pangkat_gol[]')
        jabatan = request.form.getlist('petugas_jabatan[]')

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

    if jenis == 'daftar_pengeluaran_rill':

        uraian = request.form.getlist('pengeluaran_uraian[]')
        jumlah = request.form.getlist('pengeluaran_jumlah[]')

        data['pengeluaran'] = [

            {
                'uraian': u,
                'jumlah': j
            }

            for u, j in zip(uraian, jumlah)

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
# PDF
# ======================================================

@app.route('/surat/<int:id>/pdf')
@login_required
def surat_pdf(id):

    surat = get_surat_or_404(id)

    html = render_template(

        'preview_' + surat['jenis'] + '.html',

        surat=surat,

        data=surat['data_dict'],

        pdf=True,

        user=current_user()

    )

    pdf = io.BytesIO()

    pisa.CreatePDF(

        io.StringIO(html),

        dest=pdf,

        encoding='utf-8'

    )

    pdf.seek(0)

    return send_file(

        pdf,

        as_attachment=True,

        download_name=f"{surat['jenis']}_{id}.pdf",

        mimetype='application/pdf'

    )

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
# ARSIP
# ======================================================

@app.route('/arsip')
@login_required
def arsip():

    q = request.args.get('q', '')
    jenis = request.args.get('jenis', '')
    status = request.args.get('status', '')

    sql = 'SELECT * FROM surat WHERE 1=1'

    params = []

    if q:

        sql += '''
            AND
            (
                judul LIKE %s
                OR nomor_surat LIKE %s
            )
        '''

        params += [
            f'%{q}%',
            f'%{q}%'
        ]

    if jenis:

        sql += ' AND jenis=%s'

        params.append(jenis)

    if status:

        sql += ' AND status=%s'

        params.append(status)

    sql += ' ORDER BY id DESC'

    con = db()
    cur = con.cursor(dictionary=True)

    cur.execute(sql, params)

    rows = cur.fetchall()

    cur.close()
    con.close()

    return render_template(

        'arsip.html',

        rows=rows,

        jenis_surat=JENIS_SURAT,

        user=current_user()

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
