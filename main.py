import tkinter as tk
from models import DataManager
from ui import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    data_manager = DataManager()
    app = MainWindow(root, data_manager)
    root.mainloop()
