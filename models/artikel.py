from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    artikels = db.relationship('Artikel', backref='kategori', lazy=True)

class Artikel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(200), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    gambar = db.Column(db.String(500), nullable=True)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'), nullable=True)