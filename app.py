import os

from flask import Flask
from extensions import db, login_manager
from config import Config
import cloudinary

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    cloudinary.config(
        cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
        api_key=app.config['CLOUDINARY_API_KEY'],
        api_secret=app.config['CLOUDINARY_API_SECRET']
    )

    with app.app_context():
        from models.artikel import User, Artikel
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        from models.artikel import User
        return User.query.get(int(user_id))

    from routes.publik import publik
    from routes.admin import admin
    app.register_blueprint(publik)
    app.register_blueprint(admin, url_prefix='/admin')

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)