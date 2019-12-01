import tkinter as tk
from tkinter import filedialog
import ntpath as parser
from MenuFrames.SubFrames.ImageFrame import ImageFrame


class EditorFrame:
    def __init__(self, main_win):
        self.window_ref = main_win
        self.window_ref.clear_title_bkg()

        self.img_load_path = ""
        self.img_loaded = False

        self.editorFrame = tk.Frame()
        self.editorFrame.config(bg="white", width=960, height=600)
        self.editorFrame.pack()

        self.titleLabel = tk.Label(self.editorFrame, text="EDITOR", bg="white", fg="black")
        self.titleLabel.config(font=('Algerian', 20))
        #self.titleLabel.pack(side=tk.TOP, ipadx=10, ipady=10)
        self.titleLabel.grid(ipadx=10, ipady=10, row=0, columnspan=3)

        self.step1Label = tk.Label(self.editorFrame, text="1) Seleccione la imagen a procesar: ",
                                   bg="white", fg="black")
        self.step1Label.config(font=('Algerian', 14))
        #self.step1Label.pack(side=tk.LEFT, ipadx=10, ipady=10)
        self.step1Label.grid(row=1, column=0)

        self.chooseImgButton = tk.Button(self.editorFrame, text="...", fg="black", command=self.choose_img)
        #self.chooseImgButton.pack(side=tk.LEFT, padx=5, pady=20, ipadx=10)
        self.chooseImgButton.config(font=('Algerian', 14))
        self.chooseImgButton.grid(padx=5, pady=10, ipadx=10, row=1, column=1)

        self.fileLabel = tk.Label(self.editorFrame, text="No seleccionado", bg="white", fg="black")
        self.fileLabel.config(font=('Algerian', 14))
        #self.fileLabel.pack(side=tk.LEFT, ipadx=10, ipady=10)
        self.fileLabel.grid(ipadx=10, ipady=10, row=1, column=2)

        self.step2Label = tk.Label(self.editorFrame, text="2) Seleccionar el objeto a remover: ",
                                   bg="white", fg="black")
        self.step2Label.config(font=('Algerian', 14))
        #self.step2Label.pack(side=tk.BOTTOM, ipadx=10, ipady=10)
        self.step2Label.grid(row=2, column=0)

        self.imgFrame = ImageFrame(self.editorFrame, 3)

        self.backButton = tk.Button(self.editorFrame, text="Volver", fg="black", command=self.back_req)
        self.backButton.config(font=('Algerian', 20))
        #self.backButton.pack(pady=20, ipadx=10, ipady=5)
        self.backButton.grid(pady=20, ipadx=10, ipady=5, row=4, column=0, sticky='W')

        self.processButton = tk.Button(self.editorFrame, text="Procesar", fg="black", command=self.process_req)
        self.processButton.config(font=('Algerian', 20))
        self.processButton.grid(pady=20, ipadx=10, ipady=5, row=4, column=2, sticky='W')


    def choose_img(self):
        #Es un string con el directorio de la imagen
        self.img_load_path = tk.filedialog.askopenfilename(initialdir="/", title="Select file",
                                                           filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

        if self.img_load_path:
            self.imgFrame.save_img_original(self.img_load_path)
            self.fileLabel.config(text=parser.basename(self.img_load_path))
            self.img_loaded = True
            self.imgFrame.show_img()
        else:
            if not self.img_loaded:
                self.fileLabel.config(text="No seleccionado")

    def back_req(self):
        self.window_ref.view_update("editor_cancel_req")

    def process_req(self):
        self.imgFrame.create_mask()
        self.window_ref.view_update("editor_process_req")

    def delete_frame(self):
        self.editorFrame.destroy()
