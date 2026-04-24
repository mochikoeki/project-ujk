from flask import Blueprint, render_template
from models.artikel import Artikel
from extensions import db

publik = Blueprint('publik', __name__)

@publik.route('/')
def index():
    # Ambil 3 artikel terbaru untuk halaman home
    terbaru = Artikel.query.order_by(Artikel.tanggal.desc()).limit(3).all()
    return render_template('index.html', artikels=terbaru)

@publik.route('/about')
def about():
    return render_template('about.html')

@publik.route('/artikel')
def artikel():
    data = Artikel.query.order_by(Artikel.tanggal.desc()).all()
    return render_template('artikel.html', artikels=data)

@publik.route('/artikel/<int:id>')
def detail(id):
    data = Artikel.query.get_or_404(id)
    return render_template('detail.html', artikel=data)