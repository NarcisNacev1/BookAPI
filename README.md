## BookAPI

This project is a simplified version of the course API as it currently lacked a UI. However, I have now added a UI and made several other improvements. It was cool to revisit and build it from scratch.

### Updates

- **Added a UI:** I have completed the UI for the BookAPI. The UI allows users to interact with the API through a user-friendly interface, making it easier to perform CRUD operations on the books database.
- **Updated API with Update Section:** I added a `PUT` endpoint to the API, allowing users to update existing book entries in the database. This was a crucial addition to complete the CRUD functionality.

### What I Learned

- **First time using GitBash:** It took me some time to learn all the commands, but now I can upload to GitHub directly from the terminal without using the web interface. GitBash seems pretty useful, and I definitely plan to learn more as I work on additional projects in the future.

- **Using SQLiteStudio:** I used SQLiteStudio as the database tool for this project, and it went smoothly. It’s much cleaner than pgAdmin4. I uploaded the file generated in PyCharm, and it worked perfectly—no need to tweak anything. I initially planned to upload the project to Heroku for hosting, which is why there's an extra file named Procfile with some text I'll delete later. However, I found out that Heroku requires payment, so I kept the setup as is. All the CRUD commands work fine for now, and tomorrow I'll check if the UI affects anything.

- **Handling Git Branches:** I also used `git push --force` because I couldn't figure out how to merge the branches I had (main and master). I wanted all the code to be in the main branch but kept getting an error. I need to learn how to do this without potentially deleting someone else's work since I've read that `git push --force` can cause that.

Overall, this project has been a great learning experience, and I'm looking forward to enhancing it further.

### Code Snippets

#### Redirect to Swagger UI
```python
@app.route('/')
def index():
    return redirect("/swagger/#/")
```

#### Updated Single Book Endpoint
```python
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
```

### Next Steps

- Finalize and polish the UI.
- Test the application thoroughly to ensure all features work as expected.
- Learn more about merging branches in Git without using `git push --force`.

Overall, this project has been a fantastic journey, and I'm excited about the new skills I've gained and look forward to applying them to future projects.
