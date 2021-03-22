from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, OneLineRightIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.snackbar import Snackbar


# Создание трёх экранов, наследуемых от базового
class StartScreen(Screen):
    pass


class AddTaskScreen(Screen):
    pass


class UpdateTaskScreen(Screen):
    pass


# Добавление менеджера и трёх кастомных экранов
sm = ScreenManager()
sm.add_widget(StartScreen(name='StartScreen'))
sm.add_widget(AddTaskScreen(name='AddTaskScreen'))
sm.add_widget(UpdateTaskScreen(name='UpdateTaskScreen'))


# Создание элемента списка с иконкой справа
class ListItemWithCheckbox(OneLineRightIconListItem):
    '''Custom list item.'''


# Создание чекбокса для правой части
class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__()
        # Создание списка выполненных заданий для отслеживания
        self.done_list = []

    def build(self):
        # Активация разметки
        self.style = Builder.load_file('style.kv')
        return self.style

    def change_screen(self, screen):
        # Функция перехода на экран screen
        self.root.current = screen

    def addTask(self):
        # Функция добавления задания в список
        # Считывание данных из экрана добавления
        task_text = self.style.get_screen('AddTaskScreen').ids.task_text.text
        # Если данные введены
        if task_text.split():
            # Добавление записи
            self.style.get_screen('StartScreen').ids.my_list.add_widget(
                ListItemWithCheckbox(text=task_text)
            )
            # Переход на стартовый экран
            self.change_screen('StartScreen')
            # Очистка данных на экране ввода
            self.style.get_screen('AddTaskScreen').ids.task_text.text = ""
        # Если нет
        else:
            # Показываем уведомление о пустом поле ввода
            Snackbar(text='Task is Empty').show()

    def updateTaskStart(self, item):
        # Функция перехода на экран обновления и передача в него элемента
        self.updating_item = item
        self.style.get_screen('UpdateTaskScreen').ids.update_task_text.text = self.updating_item.text
        self.style.get_screen('UpdateTaskScreen').manager.current = 'UpdateTaskScreen'

    def updateTaskFinish(self):
        # Функция обновления задания в списке
        # Считывание данных из экрана
        task_updated = self.style.get_screen('UpdateTaskScreen').ids.update_task_text.text
        # Если данные введены
        if task_updated.split():
            self.updating_item.text = task_updated
            # Переход на стартовый экран
            self.change_screen('StartScreen')
        # Если нет
        else:
            # Показываем уведомление о пустом поле ввода
            Snackbar(text='Task is Empty').show()

    def on_checkbox_active(self, checkbox, value, f_but):
        # Функция при нажатии на чекбокс
        # Запись в список выполненых при нажатой галочке и удаление при снятия галочки
        if value:
            self.done_list.append(f_but)
        else:
            self.done_list.remove(f_but)

    def delete_done_list(self):
        # Функция удаления выполненых заданий
        for task in self.done_list:
            self.style.get_screen('StartScreen').ids.my_list.remove_widget(task)
        # Очистка списка выполненых после удаления
        for task in self.done_list:
            self.done_list.remove(task)


MyApp().run()
