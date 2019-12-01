import tkinter as tk


class ProcessFrame:
    def __init__(self, main_win):
        self.window_ref = main_win

        self.processFrame = tk.Frame()
        self.processFrame.config(bg="white", width=960, height=600)
        self.processFrame.pack()

        self.titleLabel = tk.Label(self.processFrame, text="PROCESADO DE IMAGEN", bg="white", fg="black")
        self.titleLabel.config(font=('Algerian', 20))
        self.titleLabel.grid(ipadx=10, ipady=10, row=0, columnspan=3)

        self.OKButton = tk.Button(self.processFrame, text="OK", fg="black", command=self.back_req)
        self.OKButton.config(font=('Algerian', 20))
        self.OKButton.grid(ipadx=10, ipady=5, row=1, sticky='W')

    def back_req(self):
        self.window_ref.view_update("editor_cancel_req")

    def delete_frame(self):
        self.processFrame.destroy()