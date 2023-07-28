# config.py

import os

# Configurações do banco de dados
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'fluxo_de_caixa_python'

# Caminho completo para o banco de dados
DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
