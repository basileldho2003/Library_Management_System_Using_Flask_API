from flask import Flask, request, jsonify
import sqlite3, sys

app = Flask(__name__)

def db_connector():
    try:
        sqlconn = sqlite3.connect("library.sqlite")
        sqlcur = sqlconn.cursor()
        sqlcur.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                isbn TEXT
            )
        """
        )
        sqlcur.execute(
            """
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                membership_date TEXT DEFAULT CURRENT_DATE
            )
        """
        )
        sqlconn.commit()
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}", file=sys.stderr)
    finally:
        sqlconn.close()

db_connector()

@app.route("/")
def index():
    return jsonify({"message": "Welcome to ABC library."}), 200

# Display/insert books.
@app.route("/books", methods=["GET", "POST"])
def books():
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    if request.method == "GET":
        try:
            scur.execute("SELECT * FROM books")
            books = [
                dict(
                    id=bkrow[0],
                    title=bkrow[1],
                    author=bkrow[2],
                    year=bkrow[3],
                    isbn=bkrow[4],
                )
                for bkrow in scur.fetchall()
            ]
            return jsonify(books), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            sconn.close()
    if request.method == "POST":
        try:
            new_title = request.args.get("title")
            new_author = request.args.get("author")
            new_year = request.args.get("year") or None
            new_isbn = request.args.get("isbn") or None
            if new_title and new_author or new_year or new_isbn:
                insquery = "INSERT INTO books (title, author, year, isbn) \
                             VALUES(?, ?, ?, ?)"
                scur.execute(insquery, (new_title, new_author, new_year, new_isbn))
                sconn.commit()
                return (
                    jsonify(
                        {"messsage": f"Record of book {new_title} added successfully."}
                    ),
                    201,
                )
            else:
                return (
                    jsonify({"error": "Title and author fields are required!"}),
                    500,
                )
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            sconn.close()


# Display book by ID.
@app.route("/books/<int:id>", methods=["GET"])
def book_id(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM books WHERE id={id}")
        book = [
            dict(
                id=bkrow[0],
                title=bkrow[1],
                author=bkrow[2],
                year=bkrow[3],
                isbn=bkrow[4],
            )
            for bkrow in scur.fetchall()
        ]
        if book:
            return jsonify(book), 200
        else:
            return jsonify({"error": f"Book {id} not found!"}), 500
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()


# Update book by ID.
@app.route("/books/<int:id>", methods=["PUT"])
def book_id_update(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM books WHERE id={id}")
        ex_rec = scur.fetchall()
        if not ex_rec:
            return jsonify({"error": f"Book {id} not found!"}), 500
        book = [
            dict(
                id=bkrow[0],
                title=bkrow[1],
                author=bkrow[2],
                year=bkrow[3],
                isbn=bkrow[4],
            )
            for bkrow in ex_rec
        ]
        new_title = request.args.get("title") or book[0]["title"]
        new_author = request.args.get("author") or book[0]["author"]
        new_year = request.args.get("year") or book[0]["year"]
        new_isbn = request.args.get("isbn") or book[0]["isbn"]
        upquery = "UPDATE books \
            SET title=?, author=?, year=?, isbn=? \
            WHERE id=?"
        scur.execute(upquery, (new_title, new_author, new_year, new_isbn, id))
        sconn.commit()
        return (
            jsonify(
                {
                    "message": f"Book ID {id} updated successfully!"
                }
            ),
            200,
        )
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()


# Delete book by ID.
@app.route("/books/<int:id>", methods=["DELETE"])
def book_id_delete(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM books WHERE id={id}")
        ex_rec = scur.fetchall()
        if not ex_rec:
            return jsonify({"error": f"Book {id} not found!"}), 500
        scur.execute(f"DELETE FROM books WHERE id={id}")
        sconn.commit()
        return jsonify({"error": f"Book {id} deleted successfully!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()

# Display/insert members.
@app.route("/members", methods=["GET", "POST"])
def members():
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    if request.method == "GET":
        try:
            scur.execute("SELECT * FROM members")
            members = [
                dict(
                    id=memrow[0],
                    name=memrow[1],
                    email=memrow[2],
                    membership_date=memrow[3],
                )
                for memrow in scur.fetchall()
            ]
            return jsonify(members), 200
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
    if request.method == "POST":
        try:
            new_name = request.args.get("name")
            new_email = request.args.get("email") or None
            if new_name and new_email:
                insquery = "INSERT INTO members (name, email) \
                             VALUES(?, ?)"
                scur.execute(insquery, (new_name, new_email))
                sconn.commit()
                return (
                    jsonify(
                        {"messsage": f"Record of name {new_name} added successfully."}
                    ),
                    201,
                )
            else:
                return (
                    jsonify({"error": "Name and email fields are required!"}),
                    500,
                )
        except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            sconn.close()


# Display member by ID.
@app.route("/members/<int:id>", methods=["GET", "POST"])
def member_id(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM members WHERE id={id}")
        member = [
            dict(
                id=memrow[0],
                name=memrow[1],
                email=memrow[2],
                membership_date=memrow[3],
            )
            for memrow in scur.fetchall()
        ]
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": f"Member {id} not found!"}), 500
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()


# Update member by ID.
@app.route("/members/<int:id>", methods=["GET", "POST", "PUT"])
def member_id_update(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM members WHERE id={id}")
        ex_rec = scur.fetchall()
        if not ex_rec:
            return jsonify({"error": f"Member {id} not found!"}), 500
        member = [
            dict(
                id=memrow[0],
                name=memrow[1],
                email=memrow[2],
                membership_date=memrow[3],
            )
            for memrow in ex_rec
        ]
        new_name = request.args.get("name") or member[0]["name"]
        new_email = request.args.get("email") or member[0]["email"]
        upquery = "UPDATE members \
            SET name=?, email=? \
            WHERE id=?"
        scur.execute(upquery, (new_name, new_email, id))
        sconn.commit()
        return (
            jsonify(
                {
                    "message": f"Member ID {id} updated successfully!"
                }
            ),
            200,
        )
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()


# Delete member by ID.
@app.route("/members/<int:id>", methods=["GET", "POST", "DELETE"])
def member_id_delete(id):
    sconn = sqlite3.connect("library.sqlite")
    scur = sconn.cursor()
    try:
        scur.execute(f"SELECT * FROM members WHERE id={id}")
        ex_rec = scur.fetchall()
        if not ex_rec:
            return jsonify({"error": f"Member {id} not found!"}), 500
        scur.execute(f"DELETE FROM members WHERE id={id}")
        sconn.commit()
        return jsonify({"error": f"Member {id} deleted successfully!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        sconn.close()


if __name__ == "__main__":
    app.run()
