from flask import Flask, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__, static_folder='static')

app.config.from_pyfile('config.py')  # Carrega as configurações do arquivo config.py
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.caixa import Caixa


@app.route('/')
def index():
    tipo = request.args.get('tipo', '')  # Obtém o valor do parâmetro 'tipo' da URL

    # Consulta os dados do banco de dados com base no tipo, se houver algum filtro
    if tipo:
        caixas = Caixa.query.filter(or_(Caixa.tipo.ilike(f'%{tipo}%'))).all()
    else:
        caixas = Caixa.query.all()

    # Calcula as somas de receitas e despesas
    receitas = sum(caixa.valor for caixa in caixas if caixa.status == 1)
    despesas = sum(caixa.valor for caixa in caixas if caixa.status == 0)

    # Calcula o valor total (receitas - despesas)
    valor_total = receitas - despesas

    # Envia as informações para o template
    return render_template('index.html', receitas=receitas, despesas=despesas, valor_total=valor_total, extrato=caixas, termo_busca=tipo)

@app.route('/adicionar')
def adicionar():
    return render_template('adicionar.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    tipo = request.form['tipo']
    valor = float(request.form['valor'])
    status = int(request.form['status'])

    novo_caixa = Caixa(tipo=tipo, valor=valor, status=status)
    db.session.add(novo_caixa)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    caixa = Caixa.query.get(id)
    if caixa:
        db.session.delete(caixa)
        db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
