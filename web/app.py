from flask import Flask, render_template, redirect, request, url_for
from ChatBot import ChatBot

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        msg_list = ChatBot.load_last()
        return render_template('test.html', msg_list=msg_list)
    else:
        if request.form['btn'] == 'upload':
            ChatBot.add_message('Загрузить из базы')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list)
        elif request.form['btn'] == 'load':
            ChatBot.add_message('Загрузить в базу')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list)
        else:
            ChatBot.add_message('Добавить в базу')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list)


if __name__ == '__main__':
    ChatBot = ChatBot()
    app.run(port=8080, host='127.0.0.1', debug=True)
