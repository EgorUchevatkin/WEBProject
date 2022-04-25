class Sender:
    def __init__(self):
        self.messages = []

    def load_messages(self, numbers=0):
        if self.messages and len(self.messages) > numbers:
            if numbers == 0:
                return self.messages
            else:
                return self.messages[len(self.messages) - numbers - 1:]
        else:
            return 'Неправильный аргумент'

    def put_messages(self, msg_text, target='msg'):
        """
        Это будет функция, которая будет вызываться при нажатии кнопки пользователем, то есть функция,
        отвечающая за ответ пользователя
        :return:
        """
        # TODO: Добавить сообщение во фрейм(обновить фрейм)
        self.messages.append(msg_text)

    def get_request_to_user(self, targets=['name', 'surname']):
        request = None

        return request
