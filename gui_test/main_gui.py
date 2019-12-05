import tkinter as tk

from MenuFrames.MainFrame import MainFrame
from MenuFrames.AboutFrame import AboutFrame
from MenuFrames.HelpFrame import HelpFrame
from MenuFrames.EditorFrame import EditorFrame
from MenuFrames.ProcessFrame import ProcessFrame


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Testing GUI")
        self.window.geometry('960x600')
        self.window.config(bg="white")
        self.window.resizable(0, 0)

        self.imgOriginal = None
        self.bkgImage = None
        self.bkgLabel = None
        self.title = None
        self.load_title_bkg()

        self.actualFrame = MainFrame(self)

    def run(self):
        self.window.mainloop()

    def load_title_bkg(self):
        self.bkgImage = tk.PhotoImage(file="GUI_Images/MainImage.png")
        self.bkgLabel = tk.Label(image=self.bkgImage)
        self.bkgLabel.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        self.title = tk.Label(self.window, text="RETOQUE FOTOGRÁFICO", bg="white", fg="black")
        self.title.pack(padx=5, pady=5, ipadx=5, ipady=5, fill=tk.X)
        self.title.config(font=('Algerian', 26))

    def clear_title_bkg(self):
        self.bkgLabel.destroy()
        self.title.destroy()

    def view_update(self, new_req):
        if new_req == "about_window_req":
            self.actualFrame = AboutFrame(self)
        elif new_req == "main_window_req":
            self.actualFrame = MainFrame(self)
        elif new_req == "help_window_req":
            self.actualFrame = HelpFrame(self)
        elif new_req == "editor_window_req":
            self.actualFrame = EditorFrame(self)
        elif new_req == "editor_cancel_req":
            self.actualFrame.delete_frame()
            self.load_title_bkg()
            self.actualFrame = MainFrame(self)
        elif new_req == "editor_process_req":
            self.actualFrame.delete_frame()
            self.actualFrame = ProcessFrame(self)

    def exit(self):
        self.actualFrame.delete_frame()
        self.window.destroy()


if __name__ == '__main__':
    main_gui = MainWindow()
    main_gui.run()

