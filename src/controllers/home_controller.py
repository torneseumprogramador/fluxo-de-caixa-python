# controllers/home_controller.py

from flask import redirect, render_template, request, url_for
from sqlalchemy import or_

from app import app, db
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
