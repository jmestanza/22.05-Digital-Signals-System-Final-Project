import tkinter as tk
from tkinter import ttk
import threading
from MenuFrames.SubFrames.ProgressFrame import ProgressFrame
from Algoritmo.algorithm import Algorithm


class ProcessFrame:
    def __init__(self, main_win):
        self.window_ref = main_win

        self.processFrame = tk.Frame()
        self.processFrame.config(bg="white", width=960, height=600)
        self.processFrame.pack()

        self.titleLabel = tk.Label(self.processFrame, text="PROCESAMIENTO DE IMAGEN", bg="white", fg="black")
        self.titleLabel.config(font=('Algerian', 20))
        self.titleLabel.grid(ipadx=10, ipady=10, row=0, columnspan=3)

        self.inpaintProgress = ProgressFrame(self.processFrame, 1)
        self.img_address = "OutJobs/testimage.jpeg"
        self.inpaintProgress.update_image(self.img_address)

        self.processProgress = ttk.Progressbar(self.processFrame, length=300, mode="indeterminate")
        self.processProgress.grid(pady=20, row=2, column=1)
        self.processProgress.start(10)

        self.OKButton = tk.Button(self.processFrame, text="Detener", fg="black", command=self.back_req)
        self.OKButton.config(font=('Algerian', 20))
        self.OKButton.grid(ipadx=10, ipady=5, row=3, columnspan=3)

        self.algorithm = Algorithm(self.update_statics)

        self.taskTest = threading.Thread(target=self.task1)
        self.taskTest.start()

        self.taskFinish = 0
        self.avoid = 0

    def update_statics(self):
        self.img_address = self.algorithm.get_address()
        self.inpaintProgress.update_image(self.img_address)

    def back_req(self):
        if self.taskFinish == 0:
            self.avoid = 1
            self.algorithm.stop_processing()

        self.window_ref.view_update("editor_cancel_req")

    def task1(self):
        self.algorithm.run_algorithm()

        if self.avoid == 0:
            self.taskFinish = 1
            self.OKButton.config(text="Termino")

    def delete_frame(self):
        self.processFrame.destroy()
