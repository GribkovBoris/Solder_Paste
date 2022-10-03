# ***********************************************************************
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from Gui_Automizer import MyThread
import Gui_Kivy


class ContainerTest(BoxLayout):

    def __init__(self, kek, **kwargs):
        super(ContainerTest, self).__init__(**kwargs)
        self.kek = kek

    def printMe(self):
        print(self.ids.mylabel.text)
        print(self.kek)


class TutorialApp(App):
    def build(self):
        self.load_kv('.kv')
        return ContainerTest(11)


# ***********************************************************************
# Запуск проекта
if __name__ == "__main__":
    threadExit = MyThread("exit")
    threadExit.start()
    # Gui_Kivy.init_window(1400, 700)
    Gui_Kivy.init_window(1000, 500)
    if True:
        # app = Gui_Kivy.DisplayApp()
        # app.run()
        Gui_Kivy.DisplayApp().run()
    else:
        app = TutorialApp()
        app.run()
# ***********************************************************************
