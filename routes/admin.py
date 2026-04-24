from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.artikel import User, Artikel
from app import db
from extensions import db

admin = Blueprint('admin', __name__)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
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
    return render_template('admin/dashboard.html', artikels=artikels)

@admin.route('/tambah', methods=['GET', 'POST'])
@login_required
def tambah():
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        artikel = Artikel(judul=judul, isi=isi)
        db.session.add(artikel)
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/tambah.html')

@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    artikel = Artikel.query.get_or_404(id)

    if request.method == 'POST':
        artikel.judul = request.form['judul']
        artikel.isi = request.form['isi']
        db.session.commit()
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit.html', artikel=artikel)

@admin.route('/hapus/<int:id>')
@login_required
def hapus(id):
    artikel = Artikel.query.get_or_404(id)
    db.session.delete(artikel)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))