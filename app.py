from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f"Item(name='{self.name}', description='{self.description}')"


# Метод создания новой записи
@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    new_item = Item(name=data['name'], description=data.get('description', ''))
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully'}), 201


# Метод получения данных по ID
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'name': item.name, 'description': item.description})


# Метод получения всех данных в формате CSV
@app.route('/items', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    csv_data = ','.join([f"{item.id},{item.name},{item.description}\n" for item in items])
    return csv_data, 200, {'Content-Type': 'text/csv'}


# Метод обновления записи
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.json
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})


# Метод удаления записи
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})


# Создание таблицы в базе данных
@app.before_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
