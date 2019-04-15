# -*- coding:utf-8 -*-
# Автор: Олег Иванович Ляш

# Импорт модулей
import arcade
import os
import tkinter as tk

# Включение и отключение вывода отладочных сообщений
DEBUG = True

SCALE = 1

class TImageButton:
    def __init__(self,center_x, center_y, img1="images/GUI/close1.png", img2="images/GUI/close2.png"):
        self.center_x = center_x
        self.center_y = center_y
        self.img1 = arcade.Sprite(img1, 1)
        self.img1.width = self.img1.width * SCALE
        self.img1.height = self.img1.height * SCALE

        self.img2 = arcade.Sprite(img2, 1)
        self.img2.width = self.img2.width * SCALE
        self.img2.height = self.img2.height * SCALE

        self.width=self.img1.width
        self.height = self.img1.height
        self.img1.center_x = center_x
        self.img1.center_y = center_y
        self.img2.center_x = center_x
        self.img2.center_y = center_y

    def draw(self):
        self.img2.draw()


class TButton:
    """ img-based button """
    def __init__(self, center_x, center_y ):
        self.img = arcade.Sprite("images/GUI/close1.png", 1)
        self.center_x = center_x
        self.center_y = center_y
        self.img.center_x = center_x
        self.img.center_y = center_y
        self.pressed = False
        self.width = 20
        self.height = 20

    def draw(self):
        """ Draw the button """
        # arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width,
        #                              self.height, self.face_color)
        if not self.pressed:
            arcade.draw_circle_filled(self.center_x, self.center_y, self.width, arcade.color.RED)
        else:
            arcade.draw_circle_filled(self.center_x, self.center_y, self.width, arcade.color.GREEN)
        # self.img.draw()

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


def check_mouse_press_for_buttons(x, y, button_list):
    """ Given an x, y, see if we need to register any button clicks. """
    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()


def check_mouse_release_for_buttons(x, y, button_list):
    """ If a mouse button has been released, see if we need to process
        any release events. """
    for button in button_list:
        if button.pressed:
            button.on_release()


class StartTextButton(TButton):
    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y)
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()


# Основной класс окна, в котором все рисуется
class TApp(arcade.Window):
    """ Основной класс приложения """

    def __init__(self, fs=False):
        """ Конструктор """
        # Заголовок окна
        self.title = "EmoDetect"
        self.subtitle = "Диагностика эмоционального развития"

        # Создаем окно tkinter, получаем реальные размеры экрана и удаляем это окно
        root = tk.Tk()
        self.SCREEN_WIDTH = 1024  # root.winfo_screenwidth()
        self.SCREEN_HEIGHT = 768  # root.winfo_screenheight()
        self.SCALE = 1
        del root
        # Открываем окно
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.title, fullscreen=fs)

        # Устанавливаем рабочий каталог, где по умолчанию будут находится файлы
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Получаем размеры окна и устанавливаем окно просмотра равным этому окну приложения
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        self.setAll()

    def setAll(self):
        self.setPaths()
        self.setUserVars()
        self.setAbout()
        self.setFonts()
        self.setColors()

        # Create our on-screen GUI buttons
        self.button_list = []

        play_button = StartTextButton(100, 570, self.close_program)
        self.button_list.append(play_button)

        self.qqq = TImageButton(200,300)

    def close_program(self):
        pass
        # self.quit = True
        # self.close()
        # quit()

    def setPaths(self):
        """ Задаем пути к ресурсам """
        self.imgPath = "images/"  # к картинкам
        self.logoPath = self.imgPath + "logo/"  # к логотипам
        self.avatarPath = self.imgPath + "avatars/"  # аватаркам пользовтаеля
        self.cardPath = self.imgPath + "cards/"  # карточкам с эмоциями
        self.soundPath = "sounds/"  # звукам
        self.fontPath = "fonts/"  # шрифтам
        self.savePath = "save"  # сохранениям результатов

    def setUserVars(self):
        """ Переменные описывающие состояние пользователя """
        self.userAvatar = 1  # Номер аватара, который выбрал пользователь
        self.userGoodAnswers = 0  # Количество правильных ответов
        self.userBadAnswers = 0  # КОличество не правильных ответов

    def setAbout(self):
        """ Данные для пункта 'О программе' """
        self.aboutDescription1 = "описание программы 1"
        self.aboutDescription2 = "описание программы 2"
        self.aboutDescription3 = "описание программы 3"
        self.aboutClient1 = "о заказчике 1"
        self.aboutClient2 = "о заказчике 2"
        self.aboutClient3 = "о заказчике 3"
        self.aboutDeveloper1 = "Сумина Дарья"
        self.aboutDeveloper2 = "Олег Иванович Ляш"
        self.aboutDeveloper3 = "Еще кто-н"
        self.aboutLogo1 = arcade.Sprite(self.logoPath + "magu-masu_logo 06_white.png", 1)
        self.aboutLogo2 = arcade.Sprite(self.logoPath + "LabVS_logo_white.png", 0.5)
        self.aboutLogo3 = arcade.Sprite(self.logoPath + "cmmpk_MO.png", 0.5)

    def setFonts(self):
        """ Шрифты """
        # шрифты отсюда https://fonts.google.com/?selection.family=Russo+One&subset=cyrillic&sort=popularity
        self.font_title = self.fontPath + "RussoOne-Regular.ttf"
        self.font = self.fontPath + "Roboto-Black.ttf"

    def setColors(self):
        """ Задаем основные цвета """
        # Цвет фона
        self.bgcolor = arcade.color.WHITE
        # Цвет текста заголовка
        self.titlecolor = arcade.color.BLACK
        # Цвет текста подзаголовка
        self.subtitlecolor = arcade.color.GRAY
        # Цвет текста пункта меню
        self.menucolor = arcade.color.GRAY
        # Цвет текста выбранного пункта меню
        self.menucolorselected = arcade.color.YELLOW
        # Задаем фоновый цвет
        arcade.set_background_color(self.bgcolor)

    def on_key_press(self, key, modifiers):
        """ Обработка нажатий на кнопки """
        # Обрабатываем клавишу ESCAPE
        if key == arcade.key.ESCAPE:
            self.close()
            quit()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Перемещение мышки """
        # Запоминаем текущие координаты мыши и ее смещение
        if DEBUG:
            print("Подвигали мышкой (%s,%s)" % (x, y))

    def on_mouse_press(self, x, y, button, modifiers):
        """ Когда кнопка мыши нажата """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if DEBUG:
                print("Нажата левая кнопка мыши")

        check_mouse_press_for_buttons(x, y, self.button_list)

    def on_mouse_release(self, x, y, button, modifiers):
        """ Когда кнопка мыши отпущена """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if DEBUG:
                print("Отпущена левая кнопка мыши")
        check_mouse_release_for_buttons(x, y, self.button_list)

    def update(self, delta_time):
        """ Перемещение объектов и др. логика """
        pass

    def on_draw(self):
        """ Рендерем экран """
        arcade.start_render()

        # Рисуем название программы (заголовок)
        text = self.title
        color = self.titlecolor
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT - 100
        arcade.draw_text(text, x, y, color, text_size, anchor_x="center", anchor_y="center", font_name=self.font_title)

        for button in self.button_list:
            button.draw()

        self.qqq.draw()


def main():
    """ Основная функция программы """
    app = TApp(False)
    app.setAll()
    arcade.run()


if __name__ == "__main__":
    main()
