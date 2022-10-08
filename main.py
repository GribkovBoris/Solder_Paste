# ***********************************************************************
from Gui_Automizer import MyThread
import Gui_Kivy
# ***********************************************************************

# Запуск проекта
if __name__ == "__main__":
    threadExit = MyThread("exit")
    threadExit.start()
    Gui_Kivy.init_window(1360, 680)
    Gui_Kivy.DisplayApp().run()

# ***********************************************************************
