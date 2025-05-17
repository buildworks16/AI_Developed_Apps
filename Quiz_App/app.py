from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

# Simple user database (in a real app, use a proper database)
users = {
    'admin': {'password': 'admin123', 'security_answer': 'blue'}
}

# Quiz questions
questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['London', 'Paris', 'Berlin', 'Madrid'],
        'answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'Which language is Flask written in?',
        'options': ['Java', 'Python', 'C++', 'JavaScript'],
        'answer': 'Python'
    },
    {
        'question': 'What is the largest mammal?',
        'options': ['Elephant', 'Blue Whale', 'Giraffe', 'Hippopotamus'],
        'answer': 'Blue Whale'
    }
]


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('quiz'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('quiz'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        security_answer = request.form['security_answer']

        if username in users:
            return render_template('register.html', error='Username already exists')

        users[username] = {
            'password': password,
            'security_answer': security_answer
        }
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        score = 0
        for i, question in enumerate(questions):
            user_answer = request.form.get(f'q{i}')
            if user_answer == question['answer']:
                score += 1

        return render_template('result.html', score=score, total=len(questions))

    return render_template('quiz.html', questions=questions)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
