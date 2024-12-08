"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Articles, Tags, ArticlesTags
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    users = [user.serialize() for user in users]
    return jsonify(users), 200



@app.route('/articles', methods=['GET'])
def get_tags():
    data = Articles.query.all()
    data = [el.serialize() for el in data]
    return jsonify(data), 200


@app.route('/articles/<int:id>', methods=['GET'])
def get_one_article(id):
    try:
        data = Articles.query.get(id)
        if data is None:
            raise Exception('no hay articulo!')
        return jsonify(data.serialize())
    except Exception as e:
        return jsonify({"error": str(e)})
    

# @app.route('/articles/<art_title>', methods=['GET'])
# def get_one_article_by_title(art_title):
#     try:
#         data = Articles.query.filter_by(title=art_title)
        
#         if data is None:
#             raise Exception('error!')
#         return jsonify(data.serialize())
#     except Exception as e:
#         return jsonify({"error": str(e)})    
    

@app.route('/articles', methods=['POST'])
def add_article():
    try:
        data = request.json
        if 'content' not in data or 'title' not in data or 'user_id' not in data:
            raise Exception('faltan datos!')
        article = Articles(
            title = data['title'],
            content = data['content'],                       # <--- puede ser data.get('content'),
            user_id = data['user_id']
        )
        db.session.add(article)
        db.session.commit()
        return jsonify(article.serialize()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})




@app.route('/articles/<int:id>', methods=['PUT'])
def update_article(id):
    try:
        data = request.json
        article = Articles.query.get(id)
        if article is None:
            raise Exception('no hay articulo!')
        
        article.title = data.get('title', article.title),
        article.content = data.get('content', article.content),                       # <--- puede ser data.get('content'),
        article.user_id = data.get('user_id', article.user_id)

        db.session.commit()
        return jsonify(article.serialize()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})



@app.route('/articles/<int:id>', methods=['DELETE'])
def delete_article(id):
    try:
        data = Articles.query.get(id)
        if data is None:
            raise Exception('No hay articulo!')
        db.session.delete(data)
        db.session.commit()
        return jsonify({'msg': 'eliminado'})
    except Exception as e:
        return jsonify({"error": str(e)})
    



@app.route('/tags', methods=['GET'])
def get_articles():
    data = Tags.query.all()
    data = [el.serialize() for el in data]
    return jsonify(data), 200


@app.route('/articlestags', methods=['GET'])
def get_articles_tags():
    data = ArticlesTags.query.all()
    data = [el.serialize() for el in data]
    return jsonify(data), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
