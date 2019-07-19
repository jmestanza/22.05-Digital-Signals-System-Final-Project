from xml.dom import minidom
import xml.etree.ElementTree as ET


configFile = "config.xml"


def get(config, tag):
    return float(config.attributes[tag].value)


def loadConfig(configDataWritable):
    print("loading")

    mydoc = minidom.parse("Globals/config.xml")
    config = mydoc.childNodes[0]

    configDataWritable.fs = get(config, "SampleFreq")
    configDataWritable.FAAfreq = get(config, "FAAFreq")
    configDataWritable.SHsample = get(config, "SampleTime")
    configDataWritable.SHhold = get(config, "HoldTime")
    configDataWritable.SRate = get(config, "SampleFreq")
    configDataWritable.Transitorio = get(config, "Transitorio")

    # rebundancia
    configDataWritable.LLfreq = configDataWritable.FAAfreq
    configDataWritable.LLoff = configDataWritable.SHsample
    configDataWritable.LLon = configDataWritable.SHhold


def writeConfig(configDataReadable):
    data = ET.Element('config')

    data.set("FAAFreq", str(configDataReadable.FAAfreq))
    data.set("SampleFreq", str(configDataReadable.fs))
    data.set("HoldTime", str(configDataReadable.SHhold))
    data.set("SampleTime", str(configDataReadable.SHsample))
    data.set("Transitorio", str(configDataReadable.Transitorio))

    myData = ET.tostring(data)
    myFile = open("Globals/config.xml", "wb")
    myFile.write(myData)


