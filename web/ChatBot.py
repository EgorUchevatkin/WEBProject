from Sender import Sender


class ChatBot:
    def __init__(self):
        self.command_list = ['Загрузить из базы', 'Загрузить в базу', 'Добавить в базу']
        self.hello_msg = ['Привет', 'Доброго времени суток', 'Здравствуйте']
        self.sender = Sender()

    def on_message(self, msg):
        if msg not in self.command_list:
            self.send_message('Я вас не понимаю')
        else:
            if msg == self.command_list[0]:
                name, surname = self.sender.get_request_to_user()
                self.load_base(name, surname)
            elif msg == self.command_list[1]:
                name, surname, item = self.sender.get_request_to_user(targets=['name', 'surname', 'item'])
                self.update_base(name, surname, item)
            else:
                name, surname, item = self.sender.get_request_to_user(targets=['name', 'surname', 'item'])
                self.add_base(name, surname, item)

    def send_message(self, text):
        self.sender.put_messages(text)

    def update_base(self, name, surname, item):
        pass

    def load_base(self, name, surname):
        # TODO: Загрузить базу данных
        pass

    def add_base(self, name, surname, item):
        pass
