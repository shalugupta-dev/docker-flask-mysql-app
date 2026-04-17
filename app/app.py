from flask import Flask, request, jsonify
import mysql.connector
import time

# ✅ Flask app define karo (IMPORTANT)
app = Flask(__name__)

# ✅ DB connection retry logic
def connect_db():
    while True:
        try:
            conn = mysql.connector.connect(
                host="mysql",
                user="root",
                password="root",
                database="blogdb"
            )
            print("✅ Connected to MySQL")
            return conn
        except Exception:
            print("⏳ Waiting for MySQL...")
            time.sleep(5)

conn = connect_db()
cursor = conn.cursor()

# ✅ Table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255)
)
""")

# ✅ Routes
@app.route('/post', methods=['POST'])
def create_post():
    data = request.json
    cursor.execute("INSERT INTO posts (title) VALUES (%s)", (data["title"],))
    conn.commit()
    return "Post saved"

@app.route('/posts', methods=['GET'])
def get_posts():
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()

    posts = []
    for row in rows:
        posts.append({"id": row[0], "title": row[1]})

    return jsonify(posts)

# ✅ Server run (MOST IMPORTANT)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)