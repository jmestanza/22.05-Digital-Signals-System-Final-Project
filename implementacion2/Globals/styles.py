from Globals import config
import tkinter.ttk as ttk


class Data:
    data = None
    def __init__(self):
        pass

    def load(self):

        s = ttk.Style()
        mygreen = "#9EB8E9"
        myred = "#D7DFD5"

        # Configuración del theme para el notebook, el treeview, y la progressbar
        s.theme_create("yummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 1, 0, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [30, 5], "background": myred, "font": config.SMALL_FONT,
                              "focuscolor": mygreen},
                "map": {"background": [("selected", mygreen)]}},
            "Treeview.Heading": {
                "configure": {"font": config.SMALL_FONT, "background": "SkyBlue2", "padding": [5, 5], },
                "map": {"background": [("selected", myred)]}
            },
            "Treeview": {
                "configure": {"font": config.SMALL_FONT, "padding": [5, 5]},
                "map": {"background": [("selected", "cyan4")]}
            },
            "red.Horizontal.TProgressbar": {
                "configure": {"foreground": "bisque2", "background": "forestGreen", "thickness": 50}
            }
        })
        s.configure('CardTrack', background='red')

        s.theme_use("yummy")




def getData():
    if not Data.data:
        Data.data = Data()
    return Data.data
