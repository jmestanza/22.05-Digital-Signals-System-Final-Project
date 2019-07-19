from util_python import read_csv
from util_python import Senial, read_spice
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# from mpldatacursor import datacursor
# import pandas as pd

MAG, \
PHA, \
DB,\
BOTH = range(4)


def csvToSignal(data, fieldY, fieldX="x_axis"):
    try:
        while len(data[fieldX]) > len(data[fieldY]):
            data[fieldX].pop()
    except KeyError:
        pass
    senial = Senial.Senial(data[fieldX], data[fieldY])

    return senial


class CombinedPlot:
    def __init__(self):
        self.plotCount = []
        self.title = ""
        self.xAxisTitle = ""
        self.yAxisTitle = ""
        self.y2AxisTitle = ""

        self.func = None
        self.logarithmic = False
        self.spiceData = dict()
        self.fig = None

    def setTitle(self, title):
        self.title = title
        return self

    def setXTitle(self, title):
        self.xAxisTitle = title
        return self

    def setYTitle2(self, title):
        self.y2AxisTitle = title
        return self

    def setYTitle(self, title):
        self.yAxisTitle = title
        return self

    def addSignalPlot(self, signal, color, name):
        self.plotCount.append({
            "signal": signal,
            "color": color,
            "name": name
        })
        return self

    def getSpiceData(self, filename):
        if not( filename is self.spiceData):
            self.spiceData[filename] = read_spice.read_file_spice(filename)
        return self.spiceData[filename]

    def addSpiceBodePlot(self, filename, name, color, mode, color2 = None, name2 = None):
        spiceData = self.getSpiceData(filename)
        suma = 0

        for i in range(len(spiceData["pha"])):
            if i > 0 and spiceData["pha"][i]+suma > 100 and spiceData["pha"][i-1] < -100:
                suma += -360
            spiceData["pha"][i] += suma

        if mode == MAG:
            xdata = spiceData["f"]
            ydata = spiceData["abs"]
        elif mode == PHA:
            xdata = spiceData["f"]
            ydata = spiceData["pha"]
        elif mode == BOTH:
            xdata = spiceData["f"]
            ydata2 = spiceData["abs"]
            ydata = spiceData["pha"]
        else:
            raise Exception("Invalid mode ", mode, " selected")

        signal = Senial.Senial(xdata, ydata)
        if mode != BOTH:
            self.plotCount.append(
                {
                    "signal": signal,
                    "color": color,
                    "name": name
                }
            )
        else:
            signal2 = Senial.Senial(xdata, ydata2)
            self.plotCount.append(
                {
                    "signal": signal,
                    "signal2": signal2,
                    "color": color2,
                    "name": name2,
                    "color2": color,
                    "name2": name
                }
            )
        return self

    def addExcelPlot(self, filename, fieldX, fieldY, color, name):
        info = pd.read_excel(filename)

        self.plotCount.append({
            "signal": Senial.Senial(info[fieldX], info[fieldY]),
            "color": color,
            "name": name
        })
        return self

    def addCSVPlot(self, filename, field, name, color):
        data = read_csv.read_csv_bode(filename)
        signal = csvToSignal(data, field)
        #signal.mode = "csv"

        self.plotCount.append({
            "signal": signal,
            "color": color,
            "name": name
        })

        return self

    def addCSVQuotient(self, filename, name, color, fieldX, fieldA, fieldB, mode = DB):
        # get k such that kFieldA=fieldB
        data = read_csv.read_csv_bode(filename)
        signal1 = csvToSignal(data, fieldA, fieldX)
        signal2 = csvToSignal(data, fieldB, fieldX)
        if mode == DB:
            yvarFinal = [signal2.values[i] - signal1.values[i] for i in range(len(signal1.values))]
        else:
            yvarFinal = [signal2.values[i] / signal1.values[i] for i in range(len(signal1.values))]

        self.plotCount.append(
            {
                "signal": Senial.Senial(signal1.xvar, yvarFinal),
                "color": color,
                "name": name
            }
        )
        return self

    def placeLimits(self):
        if len(self.plotCount) >= 2:
            case1 = self.plotCount[-1]
            case2 = self.plotCount[-2]

            if case1.mode == "teorica":
                teorica = case1
                practica = case2
            else:
                teorica = case2
                practica = case1
            if teorica.xvarEnd:
                practica.setShowStartXvar(teorica.xvarStart)
                practica.setShowEndXvar(teorica.xvarEnd)
        return self

    def plotAndSave(self, filename):
        patches = []
        fig, ax1 = plt.subplots()

        if self.func:
            func, args = self.func
            args["ax"] = ax1
            func(args)

        if self.y2AxisTitle != "":
            ax2 = ax1.twinx()

        for plot in self.plotCount:
            if plot["signal"].mode == "teorica":
                xvalues, yvalues = plot["signal"].getSamplesChangeXvar()
            elif plot["signal"].mode == "csv":
                xvalues, yvalues = plot["signal"].getSamplesBetweenLimits()
            else:
                xvalues, yvalues = plot["signal"].xvar, plot["signal"].values
            if not self.logarithmic:
                ax1.plot(
                    xvalues,
                    yvalues,
                    plot["color"]
                )
            else:
                ax1.semilogx(
                    xvalues,
                    yvalues,
                    plot["color"]
                )
            if "signal2" in plot:
                ax2.semilogx(
                    plot["signal2"].xvar,
                    plot["signal2"].values,
                    plot["color2"]
                )
                patches.append(
                    mpatches.Patch(color=plot["color2"], label=plot["name2"])
                )
            patches.append(
                mpatches.Patch(color=plot["color"], label=plot["name"])
            )
        plt.legend(handles=patches)

        plt.title(self.title)

        ax1.minorticks_on()
        ax1.grid(which='major', linestyle='-', linewidth=0.3, color='black')
        ax1.grid(axis="both", which='minor', linestyle=':', linewidth=0.1, color='black')
        ax1.tick_params(axis='both', which='minor', bottom=False)

        #plt.tick_params(axis='x', which='minor', bottom=False)

        ax1.set_xlabel(self.xAxisTitle)
        ax1.set_ylabel(self.yAxisTitle)

        if self.y2AxisTitle != "":
            ax2.set_ylabel(self.y2AxisTitle)

        fig.savefig(filename, dpi=300)

        return self

    def plot(self):
        patches = []
        fig, ax1 = plt.subplots()

        if self.func:
            func, args = self.func
            args["ax"] = ax1
            func(args)

        if self.y2AxisTitle != "":
            ax2 = ax1.twinx()

        for plot in self.plotCount:
            if plot["signal"].mode == "teorica":
                xvalues, yvalues = plot["signal"].getSamplesChangeXvar()
            elif plot["signal"].mode == "csv":
                xvalues, yvalues = plot["signal"].getSamplesBetweenLimits()
            else:
                xvalues, yvalues = plot["signal"].xvar, plot["signal"].values
            if not self.logarithmic:
                ax1.plot(
                    xvalues,
                    yvalues,
                    plot["color"]
                )
            else:
                ax1.semilogx(
                    xvalues,
                    yvalues,
                    plot["color"]
                )
            if "signal2" in plot:
                ax2.semilogx(
                    plot["signal2"].xvar,
                    plot["signal2"].values,
                    plot["color2"]
                )
                patches.append(
                    mpatches.Patch(color=plot["color2"], label=plot["name2"])
                )
            patches.append(
                mpatches.Patch(color=plot["color"], label=plot["name"])
            )
        plt.legend(handles=patches)

        plt.title(self.title)

        ax1.minorticks_on()
        ax1.grid(which='major', linestyle='-', linewidth=0.3, color='black')
        ax1.grid(axis="both", which='minor', linestyle=':', linewidth=0.1, color='black')
        ax1.tick_params(axis='both', which='minor', bottom=False)

        #plt.tick_params(axis='x', which='minor', bottom=False)

        ax1.set_xlabel(self.xAxisTitle)


        if self.y2AxisTitle != "":
            ax2.set_ylabel(self.y2AxisTitle)

        ax1.set_ylabel(self.yAxisTitle)

        self.fig = fig

        self.ax1 = ax1
        if self.y2AxisTitle:
            self.ax2 = ax2

        #fig.savefig(filename, dpi=300)

        return self

    def save(self, filename):
        self.fig.savefig(filename, dpi=300)

    def extraPlot(self, func, args):
        self.func = func, args

        return self

    def setLogarithmic(self):
        self.logarithmic = True

        return self

    def addDataTip(self, titleX, titleY, unitX, unitY):
        #print("adding")
        #self.plot()

        datacursor(
            display='multiple',
            tolerance=30,
            formatter=(titleX+": {x:.3e}  "+unitX+" \n"+titleY+":{y:.1f} "+unitY).format,
            draggable=True
        )

        return self

    def show(self):
        plt.show()
        return self

    def addDataTipBodePha(self):
        self.addDataTip(
            ax=self.ax1,
            titleX= "Freq",
            titleY= "Fase",
            unitX= "Hz",
            unitY = "Grados"
        )
        return self

    def addDataTipBodeMag(self):
        self.addDataTip(
            ax=self.ax2,
            titleX="Freq",
            titleY="Amp",
            unitX="Hz",
            unitY="Db"
        )
        return self
