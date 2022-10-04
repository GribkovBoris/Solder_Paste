# ***********************************************************************
from Gui_Automizer import MyThread
import Gui_Kivy

# ***********************************************************************
# Запуск проекта
if __name__ == "__main__":
    threadExit = MyThread("exit")
    threadExit.start()
    Gui_Kivy.init_window(1360, 680)
    # Gui_Kivy.init_window(1400, 700)
    # Gui_Kivy.init_window(1000, 500)
    # app = Gui_Kivy.DisplayApp()
    # app.run()
    Gui_Kivy.DisplayApp().run()
# ***********************************************************************
