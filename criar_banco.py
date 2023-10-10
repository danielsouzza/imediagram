from app_imediagram import database, app

from app_imediagram.models import Usuario, Foto

with app.app_context():
    database.create_all()