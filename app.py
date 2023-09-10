from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
from backend.db import db


app = Flask(__name__)

# ini adalah syarat untuk menggunakan session
# flash adalah bagian dari session
app.secret_key = '1n14dalahS3cretK3y'

from backend.auth import authapp

app.register_blueprint(authapp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'POST':
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'no_hp' : request.form['no_hp'],
            'email' : request.form['email'],
            'jurusan' : request.form['jurusan'],
        }

        # db.collection('mahasiswa').add(data)
        db.collection('mahasiswa').document().set(data)
        # tambah Flash/Pesan
        flash('Berhasil Menambah Data Mahasiswa', 'success')
        return redirect(url_for('mahasiswa'))
    
    # ini cara untuk mengambil semyua data di collection firestore
    docs = db.collection('mahasiswa').stream()
    print(type(docs))
    mhs = []
    for doc in docs:
        # ini adalah untuk konversi data snapshoot dari firestore ke dictonary
        m = doc.to_dict()
        # cara memasukkan ID
        m['id'] = doc.id
        # ini adalah cara memasukkan ke dalam list
        mhs.append(m)

    print(type(mhs))
    # return jsonify(mhs)

    # print('Ini adalah halaman mahasiswa di fungsi mahasiswa')
    return render_template('mahasiswa/mahasiswa.html', mhs=mhs)

@app.route('/mahasiswa/hapus/<uid>')
def hapus_mahasiswa(uid):
    
    # menghapus dokumen di dalam collection mahasiswa
    db.collection('mahasiswa').document(uid).delete()
    # kembali ke halaman mahasiswa setelah hapus
    flash('Berhasil Hapus Mahasiswa', 'danger')
    return redirect(url_for('mahasiswa'))

@app.route('/mahasiswa/lihat/<uid>')
def lihat_mahasiswa(uid):
    data = db.collection('mahasiswa').document(uid).get().to_dict()
    return render_template('mahasiswa/lihat.html', data=data)
    # return jsonify(data)

# EDIT
@app.route('/mahasiswa/edit/<uid>', methods=['GET', 'POST'])
def edit_mahasiswa(uid):
    # mengirimkan post
    if request.method == 'POST':
        data = {
            'nama_lengkap' : request.form['nama_lengkap'],
            'no_hp' : request.form['no_hp'],
            'email' : request.form['email'],
            'jurusan' : request.form['jurusan'],
        }

        # db.collection('mahasiswa').add(data)
        db.collection('mahasiswa').document(uid).set(data, merge=True)
        # tambah Flash/Pesan
        flash('Berhasil Edit Data Mahasiswa', 'success')
        return redirect(url_for('mahasiswa'))
    # dapatkan data mahasiswa yang mau di edit berdasarkan uid
    mahasiswa = db.collection('mahasiswa').document(uid).get().to_dict()
    # mengirimkan data mahasiswa dari database ke halaman html
    return render_template('mahasiswa/edit.html', mahasiswa=mahasiswa)


if __name__ == '__main__':
    app.run(debug=True)