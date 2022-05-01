class ChatBot:
    def __init__(self):
        from random import randint

        self.command_list = ['Создать новое соревнование', 'Создать новую группу',
                             'Добавить новый результат', 'Добавить нового ученика']
        self.hello_msg = ['Привет', 'Доброго времени суток', 'Здравствуйте']
        self.max_showed_msg = 5
        self.msg_list = [self.hello_msg[randint(0, 2)], '', '', '', '']
        self.current_command = None

    def add_message(self, text):
        self.__msg2list(text)
        if text == self.command_list[0]:
            self.__msg2list('Создание нового соревнования, пожалуйста, подождите')
            self.current_command = self.command_list[0]
        elif text == self.command_list[1]:
            self.__msg2list('Создание новой группы, пожалуйста, подождите')
            self.current_command = self.command_list[1]
        elif text == self.command_list[2]:
            self.__msg2list('Подготовка к добавлению результата, пожалуйста, подождите')
            self.current_command = self.command_list[2]
        else:
            self.__msg2list('Подготовка к добавлению нового ученика, пожалуйста, подождите')
            self.current_command = self.command_list[3]
        self.__msg2list('Все готово к вашей операции, нажмите на кнопку ниже')

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

    def load_last(self):
        return self.msg_list

    def get_html_page(self):
        command2html = {
            self.command_list[0]: 'new_competition.html',
            self.command_list[1]: 'new_group.html',
            self.command_list[2]: 'new_resultt.html',
            self.command_list[3]: 'new_student.html'
        }

        return command2html[self.current_command]
