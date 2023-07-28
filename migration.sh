#!/bin/bash

read -p "Digite o que vc deseja para migração, exemplo: 'criando tabela de usuario': " user_input

cd src
flask db migrate -m "$user_input"
flask db upgrade
