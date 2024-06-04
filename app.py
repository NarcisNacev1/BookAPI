import sqlite3
from flask import Flask, request, jsonify, redirect
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Book API"
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return redirect("/swagger/#/")

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        return jsonify(books)

    if request.method == 'POST':
        new_book = request.get_json()
        new_author = new_book.get('author')
        new_language = new_book.get('language')
        new_title = new_book.get('title')
        sql = """INSERT INTO book (author, language, title) VALUES (?, ?, ?)"""
        cursor.execute(sql, (new_author, new_language, new_title))
        conn.commit()
        return jsonify(new_book), 201

@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None

    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = dict(id=r[0], author=r[1], language=r[2], title=r[3])
        if book is not None:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404

    if request.method == 'PUT':
        updated_book = request.get_json()
        author = updated_book.get('author')
        language = updated_book.get('language')
        title = updated_book.get('title')
        sql = """UPDATE book SET author=?, language=?, title=? WHERE id=?"""
        cursor.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)

    if request.method == 'DELETE':
        sql = """DELETE FROM book WHERE id=?"""
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": f"Book with id: {id} deleted successfully"}), 200

if __name__ == '__main__':
    app.run()
