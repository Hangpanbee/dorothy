from flask import Flask, render_template, request, jsonify
from voice import resultCheck
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html', myfunction=resultCheck)


'''
@app.route('/captureaudio')
def captureaudio():
    return resultCheck()
'''

if __name__ == '__main__':
    app.run(debug=True)
