import csv

from util import getFile

class Frequency:
    def __init__(self, name, freq, mode, bandwidth) -> None:
        self.name = name
        self.freq = freq
        self.mode = mode
        self.bandwidth = bandwidth


    def out(self):
        return f"{self.name} - {self.freq} - {self.mode} - BW:{self.bandwidth}"

    def __str__(self) -> str:
        return self.out()

    def __repr__(self) -> str:
        return self.out()

    def calculateBandwidth(self):
        if self.bandwidth == "":
            return "N/A"
        elif self.bandwidth == "25":
            return "FM"
        elif self.bandwidth == "12.5":
            return "NFM"
        elif self.bandwidth == "20":
            return "FM"
        elif self.bandwidth == "11.25":
            return "NFM"
        else:
            print(f"Provided Bandwidth '{self.bandwidth}' value for channel '{self.name}' is not defined")
            return None

    def getChrip(self):
        mode = self.calculateBandwidth()
        if mode is None:
            channel = None
        if mode == "N/A":
            channel = [-1, self.name, self.freq, "off", "5.0", "", "88.5", "88.5", "023", "NN", "023", "Tone->Tone", mode, "2.5", "", "5.0W"]
        else:
            channel = [-1, self.name, self.freq, "", "5.0", "", "88.5", "88.5", "023", "NN", "023", "Tone->Tone", mode, "2.5", "", "5.0W"]

        return channel

def createFreqencies(lines):
    freqencies = []
    for line in lines:
        name = line[0]
        freq = line[1]
        mode = line[2]
        bandwidth = line[4]
        freqencies.append(Frequency(name, freq, mode, bandwidth))
    return freqencies

def getChirps(frequencies):
    chirps = []
    for i, f in enumerate(frequencies):
        chirp = f.getChrip()
        if chirp is not None:
            chirp[0] = str(i)
            chirps.append(chirp)
    return chirps

def exportChirps(chirps, outfile):
    headers = ["Location","Name","Frequency","Duplex","Offset","Tone","rToneFreq","cToneFreq","DtcsCode","DtcsPolarity","RxDtcsCode","CrossMode","Mode","TStep","Skip","Power"]
    outf = open(outfile, "w+")
    writer = csv.writer(outf)
    writer.writerow(headers)
    writer.writerows(chirps)



def processFreqencies(freq_file):
    output = getFile(freq_file)
    freqencies = createFreqencies(output[1])
    chirps = getChirps(freqencies)
    exportChirps(chirps, "out_freq.csv")
