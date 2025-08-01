from flask import Flask, render_template, request, redirect
import sqlite3

# Step 1: Create Flask app
app = Flask(__name__)

# Step 2: Initialize Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Create Questions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')

    # Create Responses Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            question_id INTEGER,
            selected_option TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Call init_db() when app starts
init_db()

# Step 3: Routes

# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Admin Page - Add Questions
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        answer = request.form['answer']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO questions (question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (question, option1, option2, option3, option4, answer))
        conn.commit()
        conn.close()

        return redirect('/admin')

    return render_template('admin.html')


# Quiz Page - User Takes Quiz
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM questions')
    questions = c.fetchall()
    conn.close()

    if request.method == 'POST':
        username = request.form['username']
        score = 0

        for q in questions:
            selected = request.form.get(f'question_{q[0]}')
            correct_answer = q[6]
            if selected == correct_answer:
                score += 1

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO responses (username, question_id, selected_option) VALUES (?, ?, ?)',
                      (username, q[0], selected))
            conn.commit()
            conn.close()

        return render_template('score.html', username=username, score=score, total=len(questions))

    return render_template('quiz.html', questions=questions)


# Step 4: Run App
if __name__ == '__main__':
    app.run(debug=True)
