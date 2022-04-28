class ChatBot:
    def __init__(self):
        self.command_list = ['Загрузить из базы', 'Загрузить в базу', 'Добавить в базу']
        self.hello_msg = ['Привет', 'Доброго времени суток', 'Здравствуйте']
        self.max_showed_msg = 5
        self.msg_list = ['Чтобы начать беседу, нажмите на одну из кнопок', '', '', '', '']

    def add_message(self, text):
        self.__msg2list(text)
        if text == self.command_list[0]:
            self.__msg2list('Загрузка из базы прошла успешно')
        elif text == self.command_list[1]:
            self.__msg2list('Загрузка в базу прошла успешно')
        else:
            self.__msg2list('Информация добавлена в базу')

    def __msg2list(self, text):
        if self.msg_list[0] == 'Чтобы начать беседу, нажмите на одну из кнопок':
            self.msg_list[0] = ''
            self.msg_list[0] = text
        else:
            if '' in self.msg_list:
                self.msg_list[self.msg_list.index('')] = text
            else:
                self.msg_list[0] = self.msg_list[1]
                self.msg_list[1] = self.msg_list[2]
                self.msg_list[2] = self.msg_list[3]
                self.msg_list[3] = self.msg_list[4]
                self.msg_list[4] = text


    def __update_base(self, name, surname, item):
        pass

    def __load_base(self, name, surname):
        # TODO: Загрузить базу данных
        pass

    def __add_base(self, name, surname, item):
        pass

    def load_last(self):
        return self.msg_list
