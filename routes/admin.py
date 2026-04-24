from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models.artikel import User, Artikel, Kategori
from extensions import db
from werkzeug.security import check_password_hash
import cloudinary.uploader

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        print(f"Username input: {username}")
        print(f"User found: {user}")
        print(f"Password input: {password}")
        if user:
            print(f"Password di DB: {user.password}")

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Username atau password salah!')

    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin.route('/dashboard')
@login_required
def dashboard():
    artikels = Artikel.query.order_by(Artikel.tanggal.desc()).all()
    kategoris = Kategori.query.all()
    return render_template('admin/dashboard.html', artikels=artikels, kategoris=kategoris)

@admin.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    kategoris = Kategori.query.all()
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        kategori_id = request.form.get('kategori_id') or None
        gambar_url = None

        if 'gambar' in request.files:
            file = request.files['gambar']
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(file)
                gambar_url = upload_result['secure_url']

        artikel = Artikel(judul=judul, isi=isi, gambar=gambar_url, kategori_id=kategori_id)
        db.session.add(artikel)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/tambah.html', kategoris=kategoris)

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    artikel = Artikel.query.get_or_404(id)
    kategoris = Kategori.query.all()

    if request.method == 'POST':
        artikel.judul = request.form['judul']
        artikel.isi = request.form['isi']
        artikel.kategori_id = request.form.get('kategori_id') or None

        if 'gambar' in request.files:
            file = request.files['gambar']
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(file)
                artikel.gambar = upload_result['secure_url']

        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit.html', artikel=artikel, kategoris=kategoris)

@admin.route('/hapus/<int:id>')
@login_required
def hapus(id):
    artikel = Artikel.query.get_or_404(id)
    db.session.delete(artikel)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

# CRUD Kategori
@admin.route('/kategori')
@login_required
def kategori():
    kategoris = Kategori.query.all()
    return render_template('admin/kategori.html', kategoris=kategoris)

@admin.route('/kategori/tambah', methods=['POST'])
@login_required
def tambah_kategori():
    nama = request.form['nama']
    kategori = Kategori(nama=nama)
    db.session.add(kategori)
    db.session.commit()
    return redirect(url_for('admin.kategori'))

@admin.route('/kategori/hapus/<int:id>')
@login_required
def hapus_kategori(id):
    kategori = Kategori.query.get_or_404(id)
    db.session.delete(kategori)
    db.session.commit()
    return redirect(url_for('admin.kategori'))