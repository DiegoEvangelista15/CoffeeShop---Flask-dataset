import dataset


class DataBase:
    def list_db(self):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            coffee = db['cafe'].all()
            if db['cafe'].count() > 0:

                cflist = [dict(id=data['id'], name=data['name'], quantity=data['quantity'], price=data['price']) for
                          data in coffee]
                return cflist
            else:
                return False

    def save_db(self, nome, qtd, prc):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].all()
            check = [f'{n["name"]}' for n in lista]
            if nome in check:
                return False
            else:
                return db['cafe'].insert(dict(name=nome, quantity=qtd, price=prc))

    def find_db(self):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].all()
            # check = [f'{n["name"]}' for n in lista]
            return lista

    def bought_db(self, nome, qtd):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].find_one(name=nome)
            qtd = float(qtd)
            lista['quantity'] = float(lista['quantity'])
            lista['quantity'] -= qtd
            if lista['quantity'] <= 0:
                return False
            else:
                return db['cafe'].update(lista, ['id'])

    def price(self, nome):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].find_one(name=nome)
            preco = lista['price']
            return preco


    def update_db(self, nome, qtd, prc):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].find_one(name=nome)
            if not lista:
                return False
            lista['quantity'] = qtd
            lista['price'] = prc
            return db['cafe'].update(lista, ['id'])

    def delete_db(self, id):
        with dataset.connect('sqlite:///cafeteria.db') as db:
            lista = db['cafe'].all()
            check = [f'{n["id"]}' for n in lista]
            if id not in check:
                return False
            else:
                return db['cafe'].delete(id=id)
