from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader, Template
import pdb
app = Flask(__name__)
app.secret_key = 'peering'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Luar2200'
app.config['MYSQL_DB'] = 'peering'
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
usuario2 = Usuario('gabriel', 'rickson', 'seha')
usuario3 = Usuario('maycon', 'rickson', 'seha')
usuario4 = Usuario('rickson', 'frickson', 'seha')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

peering1 = Peering('10', 'RJ', 'net', '172.0.0.0', '2001::1233')
peering2 = Peering('10', 'SP', 'claro', '172.0.2.0', '2001::1234')
lista = [peering1, peering2]

@app.route('/')
def index():
    return render_template('lista.html', titulo='Peering', peerings=lista)

# @app.route("/")
# def template_test():
#     return render_template('template.html', my_string="Wheeeee!", my_list=[0,1,2,3,4,5])


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Peering')

@app.route('/criar', methods=['POST',])
def criar():
    details = request.form
    ASN = details['ASN']
    local = details['local']
    company = details['company']
    IPV4 = details['IPV4']
    IPV6 = details['IPV6']

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    if lugar == 'Rio de janeiro':
        template = env.get_template('RJ.j2')
    elif lugar == 'São Paulo':
        template = env.get_template('SP.j2')
    elif lugar == 'Ceara':
        template = env.get_template('CE.j2')

    print(templates.render(ASN='ASN', local='local', company='company', ipv4='IPV4', ipv6='IPV6'))
    pdb.set_trace()

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
    return redirect(url_for('index'))






