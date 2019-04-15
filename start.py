#-*- coding:utf-8 -*-
# Автор: Олег Иванович Ляш

# Импорт модулей
import arcade
import os
import tkinter as tk

# Включение и отключение вывода отладочных сообщений
DEBUG = True

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
        self.SCREEN_WIDTH = root.winfo_screenwidth()
        self.SCREEN_HEIGHT = root.winfo_screenheight()
        del root

        # Параметры масштабирования (надо бы при запуске определять размеры экрана и масштабировать все картинки)
        self.SPRITE_SCALING = 0.1
        self.VIEWPORT_MARGIN = 40

        # Открываем окно
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.title, fullscreen=fs)

        # Устанавливаем рабочий каталог, где по умолчанию будут находится файлы
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Получаем размеры окна и устанавливаем окно просмотра равным этому окну приложения
        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

    def setup(self):
        """ Установка основных параметров """
        self.setPaths() # Общие пути к ресурсам
        self.setUserVars() # Переменные описывающие пользователя
        self.setFonts() # Шрифты
        self.setColors() # Цвета
        self.setMenu() # Главное меню
        self.mouseX = 0 # Стартовые координаты мыши (Х)
        self.mouseY = 0 # Стартовые координаты мыши (У)
        self.isMouseDown = False # Признак того что нажимают основную кнопку мыши
        self.loadAvatars() # Грузим аватарки пользователя
        self.setAbout()  # Устанавливам параметры "О программе"

    def setPaths(self):
        """ Задаем пути к ресурсам """
        self.imgPath = "images/" # к картинкам
        self.logoPath = self.imgPath + "logo/" # к логотипам
        self.avatarPath = self.imgPath+"avatars/" # аватаркам пользовтаеля
        self.cardPath = self.imgPath+"cards/" # карточкам с эмоциями
        self.soundPath = "sounds/" # звукам
        self.fontPath = "fonts/" # шрифтам
        self.savePath = "save" # сохранениям результатов

    def setUserVars(self):
        """ Переменные описывающие состояние пользователя """
        self.userAvatar = 1 # Номер аватара, который выбрал пользователь
        self.userGoodAnswers = 0 # Количество правильных ответов
        self.userBadAnswers = 0 # КОличество не правильных ответов

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
        self.aboutLogo2 = arcade.Sprite(self.logoPath + "LabVS_logo_white.png",0.5)
        self.aboutLogo3 = arcade.Sprite(self.logoPath + "cmmpk_MO.png", 0.5)

    def setFonts(self):
        """ Шрифты """
        # шрифты отсюда https://fonts.google.com/?selection.family=Russo+One&subset=cyrillic&sort=popularity
        self.font_title=self.fontPath+"RussoOne-Regular.ttf"
        self.font = self.fontPath+"Roboto-Black.ttf"

    def setColors(self):
        """ Задаем основные цвета """
        # Цвет фона
        self.bgcolor = arcade.color.BLACK
        # Цвет текста заголовка
        self.titlecolor = arcade.color.WHITE
        # Цвет текста подзаголовка
        self.subtitlecolor = arcade.color.LIGHT_GRAY
        # Цвет текста пункта меню
        self.menucolor = arcade.color.LIGHT_GRAY
        # Цвет текста выбранного пункта меню
        self.menucolorselected = arcade.color.YELLOW
        # Задаем фоновый цвет
        arcade.set_background_color(self.bgcolor)

    def setMenu(self):
        # Переменная состояния приложения
        # Если = 0, то выводится начальный экран
        self.state = 0
        # Словарь для хранения пунктов меню
        self.Menu = {}
        # Первый из отображаемых элементов меню
        self.MenuFirst = 1
        # Последний из отображаемых пунктов меню
        self.MenuLast = 5
        # Собственно сами пункты меню
        self.Menu[0] = "Стартовое меню"
        self.Menu[1] = "Выбор набора карточек"
        self.Menu[2] = "Выбор аватара"
        self.Menu[3] = "Начать"
        self.Menu[4] = "О программе"
        self.Menu[5] = "Выход"
        self.Menu[99] = "Пауза"

    def loadAvatars(self):
        """ Загрузка ававтаров """
        files = os.listdir(self.avatarPath)

        self.imgAvatars = arcade.SpriteList()

        for i in files:
            self.imgAvatar = arcade.Sprite(self.avatarPath+i, 1)
            self.imgAvatar.width = 100
            self.imgAvatar.height = 100
            self.imgAvatar.center_x = 0
            self.imgAvatar.center_y = 0
            self.imgAvatars.append(self.imgAvatar)

    def on_draw(self):
        """ Рендерем экран """
        arcade.start_render()
        if self.state == 0:
            # Рисуем менюшку стартовую менюшку
            self.drawState0()
        elif self.state == 1:
            # Рисуем менюшку стартовую менюшку
            self.drawState1()
        elif self.state == 2:
            # Рисуем менюшку стартовую менюшку
            self.drawState2()
        elif self.state == 3:
            # Рисуем менюшку стартовую менюшку
            self.drawState3()
        elif self.state == 4:
            # Рисуем менюшку стартовую менюшку
            self.drawState4()
        elif self.state == 5:
            # Выход
            try:
                quit()
            except:
                pass

        if DEBUG:
            arcade.draw_line(0,self.mouseY,self.SCREEN_WIDTH,self.mouseY,arcade.color.RED)
            arcade.draw_line(self.mouseX, 0, self.mouseX, self.SCREEN_HEIGHT, arcade.color.RED)
            print(self.MenuItemSelected)

    def drawState0(self):
        # Рисуем название программы (заголовок)
        text = self.title
        color = self.titlecolor
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 6
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)
        # Рисуем Описание программы (подзаголовок)
        text = self.subtitle
        color = self.subtitlecolor
        text_size = 30
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 4
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)
        #
        self.drawMenu()
        self.imgAvatars.sprite_list[self.userAvatar].center_x = self.imgAvatars.sprite_list[self.userAvatar].width
        self.imgAvatars.sprite_list[self.userAvatar].center_y = self.SCREEN_HEIGHT - self.imgAvatars.sprite_list[self.userAvatar].height
        self.imgAvatars.sprite_list[self.userAvatar].draw()

    def drawState1(self):
        # Выбор набора карточек
        text = "Выбор набора карточек"
        color = self.titlecolor
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 6
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

    def drawState2(self):
        # Выбор аватара
        text = "Выбор аватара"
        color = self.titlecolor
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 6
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

        #self.imgAvatars.draw()
        # Вывод конкретного спрайта
        w=self.imgAvatars.sprite_list[1].width
        h=self.imgAvatars.sprite_list[1].height
        counter = 4
        s = 20
        x = self.SCREEN_WIDTH // 2 - (counter * w) //2
        y = self.SCREEN_HEIGHT // 2
        for i in range(0,len(self.imgAvatars.sprite_list)-1):
            self.imgAvatars.sprite_list[i].center_x = x
            x += w + s
            self.imgAvatars.sprite_list[i].center_y = y
            counter -=1
            if counter <=0:
                counter = 4
                x = self.SCREEN_WIDTH // 2 - (counter * w) // 2
                y += h + s

            self.imgAvatars.sprite_list[i].draw()
            # Определяем попадание курсора на аватар
            bottom =self.mouseY > self.imgAvatars.sprite_list[i].center_y - self.imgAvatars.sprite_list[i].height // 2
            top = self.mouseY < self.imgAvatars.sprite_list[i].center_y + self.imgAvatars.sprite_list[i].height // 2

            left = self.mouseX > self.imgAvatars.sprite_list[i].center_x - self.imgAvatars.sprite_list[i].width // 2
            right = self.mouseX < self.imgAvatars.sprite_list[i].center_x + self.imgAvatars.sprite_list[i].width // 2

            if (bottom and top) and (left and right):
                arcade.draw_rectangle_outline(self.imgAvatars.sprite_list[i].center_x,self.imgAvatars.sprite_list[i].center_y,self.imgAvatars.sprite_list[i].width,self.imgAvatars.sprite_list[i].height,color=arcade.color.RED)
                if self.isMouseDown:
                    self.userAvatar = i

        # self.imgAvatars.sprite_list[self.userAvatar].center_x = 500
        # self.imgAvatars.sprite_list[self.userAvatar].center_y = 500
        # self.imgAvatars.sprite_list[self.userAvatar].draw()

    def drawState3(self):
        # Начать
        text = "Собственно процесс диагностики"
        color = self.titlecolor
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 6
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

    def drawState4(self):
        # О программе
        x = self.SCREEN_WIDTH // 2
        lineHeight = 40
        # ------------------------
        text = "О программе"
        color = self.titlecolor
        text_size = 44
        y = self.SCREEN_HEIGHT  - 2*lineHeight
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

        text =  self.aboutDescription1
        color = self.subtitlecolor
        text_size = 20
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - 3*lineHeight
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font)

        text =  self.aboutDescription2
        color = self.subtitlecolor
        text_size = 20
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - 4*lineHeight
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font)

        # ------------------------
        text = "Заказчик"
        color = self.titlecolor
        text_size = 20
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 3
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font)

        text = self.aboutClient1
        color = self.subtitlecolor
        text_size = 20
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 3 - 40
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font)

        text = self.aboutClient2
        color = self.subtitlecolor
        text_size = 20
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 3 - 80
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font)

        #------------------------
        text = "Разработчики: "
        color = self.titlecolor
        text_size = 20
        y = self.SCREEN_HEIGHT - self.SCREEN_HEIGHT // 2
        arcade.draw_text(text, x, y, color, text_size, anchor_x="center", anchor_y="center", font_name=self.font)

        text = self.aboutDeveloper1
        color = self.subtitlecolor
        text_size = 20
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT - self.SCREEN_HEIGHT // 2 - 40
        arcade.draw_text(text, x, y, color, text_size, anchor_x="center", anchor_y="center", font_name=self.font)

        text = self.aboutDeveloper2
        color = self.subtitlecolor
        text_size = 20
        y = self.SCREEN_HEIGHT - self.SCREEN_HEIGHT // 2 - 80
        arcade.draw_text(text, x, y, color, text_size, anchor_x="center", anchor_y="center", font_name=self.font)

        self.aboutLogo1.center_x = (self.SCREEN_WIDTH // 2) // 2
        self.aboutLogo1.center_y = 10 + self.aboutLogo2.height
        self.aboutLogo1.draw()

        self.aboutLogo2.center_x = (self.SCREEN_WIDTH // 2) + (self.SCREEN_WIDTH // 2) // 2
        self.aboutLogo2.center_y = 10 + self.aboutLogo2.height
        self.aboutLogo2.draw()

        self.aboutLogo3.center_x = self.SCREEN_WIDTH // 2
        self.aboutLogo3.center_y = 10 + self.aboutLogo2.height
        self.aboutLogo3.draw()

    def drawState5(self):
        # Выход из программы
        text = "Выход"
        color = arcade.color.WHITE
        text_size = 44
        x = self.SCREEN_WIDTH // 2
        y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 6
        arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

    def drawMenu(self):
        """ Рисуем менюшку """
        mx = self.mouseX
        my = self.mouseY
        width = 500
        height=15
        self.MenuItemSelected = -1

        for i in range(0,self.MenuLast):
            text = self.Menu[self.MenuFirst+i]
            text_size = 30
            x = self.SCREEN_WIDTH // 2
            y = self.SCREEN_HEIGHT  - self.SCREEN_HEIGHT // 3 - 20 - i*40
            if my>y-height and my<y+height and mx>x-width//2 and mx<x+width//2:
                color = self.menucolorselected
                self.MenuItemSelected = self.MenuFirst+i
            else:
                color = self.menucolor
            arcade.draw_text(text,x, y,color, text_size, anchor_x="center", anchor_y = "center",font_name = self.font_title)

    def on_key_press(self, key, modifiers):
        """ Обработка нажатий на кнопки """
        if key == arcade.key.F:
            # Переключение между полноэкранным режимом и обычным
            self.set_fullscreen(not self.fullscreen)
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        if key == arcade.key.S:
            # Еще один способ переключеие между полноэкранным режимом и обычным. Разница будет заметна, если разрешение экрана будет меньше чем текущее
            self.set_fullscreen(not self.fullscreen)
            self.set_viewport(0, self.SCREEN_WIDTH, 0, self.SCREEN_HEIGHT)

        # Обрабатываем клавишу ESCAPE
        if key == arcade.key.ESCAPE:
            if self.state == 0 or self.state==5:
                self.close()
                quit()
            elif self.state > 0 and self.state < 5:
                self.state=0

    def on_mouse_motion(self, x, y, dx, dy):
        """ Перемещение мышки """
        # Запоминаем текущие координаты мыши и ее смещение
        self.mouseX = x
        self.mouseY = y
        self.mouseDX = dx
        self.mouseDY = dy



    def on_mouse_press(self, x, y, button, modifiers):
        """ Когда кнопка мыши нажата """
        print(f"You clicked button number: {button}")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.bgGUIColor  = arcade.color.GREEN
            self.isMouseDown = True

    def on_mouse_release(self, x, y, button, modifiers):
        """ Когда кнопка мыши отпущена """
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.MenuItemSelected == 5:
                self.close()
                quit()

            if self.MenuItemSelected>0 and self.MenuItemSelected <=5:
                print("Перключаемся в состояние %s"%(self.MenuItemSelected))
                self.state = self.MenuItemSelected

            self.isMouseDown = False

    def update(self, delta_time):
        """ Перемещение объектов и др. логика """
        pass

def main():
    """ Main method """
    app = TApp(False)
    app.setup()
    arcade.run()

if __name__ == "__main__":
    main()