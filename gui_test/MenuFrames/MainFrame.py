import tkinter as tk


class MainFrame:
    def __init__(self, main_win):
        self.window_ref = main_win

        self.buttonsFrame = tk.Frame()
        self.buttonsFrame.pack()
        self.buttonsFrame.place(x=600, y=150)
        self.buttonsFrame.config(bg="white")

        self.editorButton = tk.Button(self.buttonsFrame, text="Editar imagen", fg="black", command=self.editor_req)
        self.editorButton.config(font=('Algerian', 20))
        self.editorButton.pack(pady=20, ipadx=10, ipady=5)

        self.howToButton = tk.Button(self.buttonsFrame, text="Ayuda", fg="black", command=self.help_req)
        self.howToButton.config(font=('Algerian', 20))
        self.howToButton.pack(pady=20, ipadx=10, ipady=5)

        self.aboutButton = tk.Button(self.buttonsFrame, text="Créditos", fg="black", command=self.about_req)
        self.aboutButton.config(font=('Algerian', 20))
        self.aboutButton.pack(pady=20, ipadx=10, ipady=5)

        self.closeButton = tk.Button(self.buttonsFrame, text="Salir", fg="black", command=self.win_close)
        self.closeButton.config(font=('Algerian', 20))
        self.closeButton.pack(pady=20, ipadx=10, ipady=5)

    def editor_req(self):
        self.window_ref.view_update("editor_window_req")
        self.delete_frame()

    def help_req(self):
        self.window_ref.view_update("help_window_req")
        self.delete_frame()

    def about_req(self):
        self.window_ref.view_update("about_window_req")
        self.delete_frame()

    def win_close(self):
        self.window_ref.exit()

    def delete_frame(self):
        self.buttonsFrame.destroy()

