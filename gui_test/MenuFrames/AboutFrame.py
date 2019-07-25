import tkinter as tk


class AboutFrame:
    def __init__(self, main_win):
        self.window_ref = main_win

        self.aboutFrame = tk.Frame()
        self.aboutFrame.pack()
        self.aboutFrame.place(x=580, y=150)
        self.aboutFrame.config(bg="white")

        self.titleLabel = tk.Label(self.aboutFrame, text="GRUPO 1", bg="white", fg="black")
        self.titleLabel.config(font=('Algerian', 20))
        self.titleLabel.pack(ipadx=10, ipady=10)

        self.int0Label = tk.Label(self.aboutFrame, text="MÁSPERO, Martina - 57120", bg="white", fg="black")
        self.int0Label.config(font=('Algerian', 16))
        self.int0Label.pack(ipadx=5, ipady=5)

        self.int1Label = tk.Label(self.aboutFrame, text="MESTANZA, Joaquín - 58288", bg="white", fg="black")
        self.int1Label.config(font=('Algerian', 16))
        self.int1Label.pack(ipadx=5, ipady=5)

        self.int2Label = tk.Label(self.aboutFrame, text="NOWIK, Ariel - 58309", bg="white", fg="black")
        self.int2Label.config(font=('Algerian', 16))
        self.int2Label.pack(ipadx=5, ipady=5)

        self.int3Label = tk.Label(self.aboutFrame, text="PARRA, Rocío - 57669", bg="white", fg="black")
        self.int3Label.config(font=('Algerian', 16))
        self.int3Label.pack(ipadx=5, ipady=5)

        self.int4Label = tk.Label(self.aboutFrame, text="REGUEIRA, Marcelo - 58300", bg="white", fg="black")
        self.int4Label.config(font=('Algerian', 16))
        self.int4Label.pack(ipadx=5, ipady=5)

        self.backButton = tk.Button(self.aboutFrame, text="Volver", fg="black", command=self.back_req)
        self.backButton.pack(pady=20, ipadx=10, ipady=5)
        self.backButton.config(font=('Algerian', 20))

    def back_req(self):
        self.window_ref.view_update("main_window_req")
        self.delete_frame()

    def delete_frame(self):
        self.aboutFrame.destroy()
