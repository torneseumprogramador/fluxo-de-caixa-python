from app import db


class Caixa(db.Model):
    __tablename__ = 'caixas'  # Define o nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, nullable=False)
