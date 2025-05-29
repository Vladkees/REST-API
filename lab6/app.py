from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
from resources import BookListResource, BookResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update({
    'APISPEC_SPEC': 'apispec.ext.marshmallow.APISpec',
    'APISPEC_TITLE': 'Library API',
    'APISPEC_VERSION': 'v1',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui'
})

db = SQLAlchemy(app)
api = Api(app)

# Реєстрація RESTful ресурсів
api.add_resource(BookListResource, '/books')
api.add_resource(BookResource, '/books/<int:book_id>')

# Генерація Swagger документації
docs = FlaskApiSpec(app)
docs.register(BookListResource)
docs.register(BookResource)

if __name__ == '__main__':
    from models import Book
    with app.app_context():
        db.create_all()
    app.run(debug=True)
