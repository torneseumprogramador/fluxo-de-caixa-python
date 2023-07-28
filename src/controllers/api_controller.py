# controllers/home_controller.py

from flask import jsonify, redirect, render_template, request, url_for
from flask_cors import CORS
from sqlalchemy import or_

from app import app, db
from models.caixa import Caixa

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/caixas')
def api_index():
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

    # Monta o dicionário com os dados
    data = {
        'receitas': receitas,
        'despesas': despesas,
        'valor_total': valor_total,
        'extrato': [
            {
                'id': caixa.id,
                'tipo': caixa.tipo,
                'valor': caixa.valor,
                'status': caixa.status
            } for caixa in caixas
        ]
    }

    # Retorna os dados em formato JSON
    return jsonify(data)

@app.route('/api/caixas', methods=['POST'])
def api_cadastrar():
    data = request.json  # Obtém os dados enviados no corpo da requisição

    tipo = data.get('tipo')
    valor = data.get('valor')
    status = data.get('status')

    if not tipo or valor is None or status is None:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        valor = float(valor)
        status = int(status)
    except ValueError:
        return jsonify({'error': 'Valor e status devem ser números'}), 400

    novo_caixa = Caixa(tipo=tipo, valor=valor, status=status)
    db.session.add(novo_caixa)
    db.session.commit()

    return jsonify({
        'id': novo_caixa.id,
        'tipo': novo_caixa.tipo,
        'valor': novo_caixa.valor,
        'status': novo_caixa.status
    })

@app.route('/api/caixas/<int:id>', methods=['DELETE'])
def api_excluir(id):
    caixa = Caixa.query.get(id)
    if caixa:
        db.session.delete(caixa)
        db.session.commit()
        return jsonify({}), 204
    else:
        # Retorna uma mensagem de erro caso o ID não seja encontrado
        return jsonify({'error': 'Registro não encontrado'}), 404
