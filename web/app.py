from flask import Flask, render_template, redirect, request, url_for
from ChatBot import ChatBot

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        msg_list = ChatBot.load_last()
        return render_template('test.html', msg_list=msg_list, check=1)
    else:
        if request.form['btn'] == 'new-competition':
            ChatBot.add_message('Создать новое соревнование')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list, check=2)
        elif request.form['btn'] == 'new-group':
            ChatBot.add_message('Создать новую группу')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list, check=2)
        elif request.form['btn'] == 'new-result':
            ChatBot.add_message('Добавить новый результат')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list, check=2)
        elif request.form['btn'] == 'new-student':
            ChatBot.add_message('Добавить нового ученика')
            msg_list = ChatBot.load_last()
            return render_template('test.html', msg_list=msg_list, check=2)
        else:
            return render_template(ChatBot.get_html_page())


if __name__ == '__main__':
    ChatBot = ChatBot()
    app.run(port=8080, host='127.0.0.1', debug=True)
