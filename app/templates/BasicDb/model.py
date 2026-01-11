from app import db 

class Model(db.Model):
    __tablename__ = "Models"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)