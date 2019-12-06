import tkinter as tk


class HelpFrame:
    def __init__(self, main_win):
        self.window_ref = main_win

        self.helpFrame = tk.Frame()
        self.helpFrame.pack()
        self.helpFrame.place(x=500, y=150)
        self.helpFrame.config(bg="white")

        self.titleLabel = tk.Label(self.helpFrame, text="Modo de uso", bg="white", fg="black")
        self.titleLabel.config(font=('Algerian', 20))
        self.titleLabel.pack(ipadx=10, ipady=10)

        self.helpText = tk.Text(self.helpFrame, height=10, width=45, font=('Algerian', 12))
        self.helpText.pack()
        self.helpText.insert(tk.END, "En el editor, elegir una imagen tipo JPEG. \n"
                                     "Para marcar el area a tratar: \n Definir los puntos en sentido horario o antiho-rario. \n "
                                     "Presionar enter para cerrarla. \n Se puede definir mas de una region. \n")
        self.helpText.config(state="disabled")

        self.backButton = tk.Button(self.helpFrame, text="Volver", fg="black", command=self.back_req)
        self.backButton.pack(pady=20, ipadx=10, ipady=5)
        self.backButton.config(font=('Algerian', 20))

    def back_req(self):
        self.window_ref.view_update("main_window_req")
        self.delete_frame()

    def delete_frame(self):
        self.helpFrame.destroy()