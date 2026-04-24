from flask import Blueprint, render_template
from models.artikel import Artikel
from extensions import db

publik = Blueprint('publik', __name__)

@publik.route('/')
def index():
    return render_template('index.html')

@publik.route('/artikel')
def artikel():
    data = Artikel.query.order_by(Artikel.tanggal.desc()).all()
    return render_template('artikel.html', artikels=data)

@publik.route('/artikel/<int:id>')
def detail(id):
    data = Artikel.query.get_or_404(id)
    return render_template('detail.html', artikel=data)