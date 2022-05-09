from flask import Flask, render_template, jsonify, make_response, session, request, redirect, url_for
from database import DataBase

app = Flask(__name__)
app.secret_key = 'MINHA_CHAVE_CRIPTOGRADAFA'

database = DataBase()


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/login_admin')
def login():
    return render_template('login_admin.html')


@app.route('/login_admin/check', methods=['POST'])
def check_login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        session['password'] = request.form['password']
        if session['user'] == 'admin' and session['password'] == 'admin':
            return redirect(url_for('admin'))
        else:
            return make_response(jsonify({'Erro:': 'Senha errada!'}), 404)


@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')


@app.route('/address')
def address():
    return render_template('address.html')


@app.route('/buy')
def buy():
    lista = database.find_db()
    return render_template('buy.html', lista=lista)


@app.route('/buy/bought', methods=['POST'])
def bought():
    if request.method == 'POST':
        session['item'] = request.form['item']
        session['quantidade'] = request.form['quantidade']
        check = database.bought_db(session['item'], session['quantidade'])
        if not check:
            return make_response(jsonify({'Erro:': 'Item nao disponivel!!!'}), 404)
        return redirect(url_for('savepoint4'))

    else:
        return make_response(jsonify({'Erro:': 'Nenhum dado encontrado!'}), 404)


@app.route('/add_bought')
def savepoint4():
    item_bd = session['item']
    qtd_bd = session['quantidade']
    lista = database.price(session['item'])

    return render_template('bought_page.html', item_id=item_bd, qtd_bd=qtd_bd, preco=lista)


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/admin/listagem')
def listing():
    lista = database.list_db()
    try:
        if not lista:
            return make_response(jsonify({'Erro:': 'Nenhum dado encontrado!'}), 404)
            # return jsonify({'Listagem de Items': lista})
        else:
            return jsonify({'Listagem de Items': lista})
    except TypeError:
        return make_response(jsonify({'Erro:': 'Nenhum dado encontrado!'}), 404)


@app.route('/admin/add', methods=['POST'])
def add():
    if request.method == 'POST':

        session['item'] = request.form['item'].title()
        session['quantidade'] = request.form['quantidade']
        session['preco'] = request.form['preco']
        result = database.save_db(session['item'], session['quantidade'], session['preco'])
        if not result:
            return make_response(jsonify({'Erro:': 'Esse item ja existe na lista!'}), 404)
        return redirect(url_for('savepoint'))
    else:
        return make_response(jsonify({'Erro:': 'Nenhum dado encontrado!'}), 404)


@app.route('/admin/update', methods=['POST'])
def update():
    if request.method == 'POST':
        session['item'] = request.form['item'].title()
        session['quantidade'] = request.form['quantidade']
        session['preco'] = request.form['preco']
        result = database.update_db(session['item'], session['quantidade'], session['preco'])
        if not result:
            return make_response(jsonify({'Erro:': 'Esse item nao existe na lista!'}), 404)
        return redirect(url_for('savepoint3'))


@app.route('/add_update')
def savepoint3():
    item_bd = session['item']
    qtd_bd = session['quantidade']
    prc_bd = session['preco']
    return render_template('update_page.html', item_bd=item_bd, qtd_bd=qtd_bd, prc_bd=prc_bd)


@app.route('/addsave')
def savepoint():
    item_bd = session['item']
    return render_template('add_page.html', item_bd=item_bd)


@app.route('/admin/del', methods=['POST'])
def delete():
    if request.method == 'POST':
        session['id'] = request.form['id']
        check = database.delete_db(session['id'])
        if not check:
            return make_response(jsonify({'Erro:': 'ID nao existe!!!'}), 404)
        return redirect(url_for('savepoint2'))

    else:
        return make_response(jsonify({'Erro:': 'Nenhum dado encontrado!'}), 404)


@app.route('/add_delete')
def savepoint2():
    delete_id = session['id']
    return render_template('delete_page.html', delete_id=delete_id)


#  improve login system
#  blueprint


app.run(debug=True)
