import os
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader, Template
import pdb
app = Flask(__name__)
app.secret_key = 'peering'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Luar2200'
# app.config['MYSQL_DB'] = 'peering'
mysql = MySQL(app)

class Peering:
    def __init__(self, asn, local, company, ipv4, ipv6):
        self.asn = asn
        self.local = local
        self.company = company
        self.ipv4 = ipv4
        self.ipv6 = ipv6

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario('jacqueline', 'jacqueline Ribeiro', 'senha')
usuario2 = Usuario('gabriel', 'gabriel', 'senha')
usuario3 = Usuario('maycon', 'rickson', 'senha')
usuario4 = Usuario('rickson', 'rickson', 'senha')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

peering1 = Peering('10', 'RJ', 'net', '172.0.0.0', '2001::1233')
peering2 = Peering('10', 'SP', 'claro', '172.0.2.0', '2001::1234')
lista = [peering1, peering2]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Peering', peerings=lista)

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='NOVO PEERING')

@app.route('/criar', methods=['GET', 'POST'])
def criar():

    details = request.form
    asn = details['asn']
    local = details['local']
    company = details['company']
    ipv4 = details['ipv4']
    ipv6 = details['ipv6']

    peering = Peering(asn, local, company, ipv4, ipv6)
    lista.append(peering)
    
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader("templates"))
    
    if local == 'Rio de Janeiro':
      template = env.get_template("RJ.j2")
      output_from_parsed_template = template.render(asn=asn, company=company, ipv4=ipv4, ipv6=ipv6)
    elif local == 'São Paulo':
      template = env.get_template("SP.j2")
      output_from_parsed_template = template.render(asn=asn, company=company, ipv4=ipv4, ipv6=ipv6)
    else:
      template = env.get_template("CE.j2")
      output_from_parsed_template = template.render(asn=asn, company=company, ipv4=ipv4, ipv6=ipv6)

    print (output_from_parsed_template)
    content = str.encode(output_from_parsed_template)
    with open("sw.html", "wb") as fh:
      fh.write(content)
      fh.close()

    return render_template('lista.html', titulo='Peering', peerings=lista)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('login'))
