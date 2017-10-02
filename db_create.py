from app import app, db
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db.create_all()