import sys
import csv

from util import getFile

class Repeater:
    def __init__(self, callsign, rx_freq, tx_freq, mode, squelch, location) -> None:
        self.callsign = callsign
        self.rx_freq = rx_freq
        self.tx_freq = tx_freq
        self.mode = mode
        self.squelch = squelch
        self.location = location

    def out(self):
        return f"{self.callsign} - RX: {self.rx_freq}, TX: {self.tx_freq}"

    def __str__(self) -> str:
        return self.out()
    def __repr__(self) -> str:
        return self.out()

    def getChirp(self):
        if (self.mode == "FM" or self.mode == "GMRS") and \
                                        ("md" in self.location.lower() or "dc" in self.location.lower()) and \
                                         self.squelch and \
                                         self.squelch.replace(".", "").isdigit() and \
                                         ((float(self.rx_freq) > 100 and float(self.rx_freq) < 200) or (float(self.rx_freq) > 400 and float(self.rx_freq) < 500)):
            offset = float(self.rx_freq) - float(self.tx_freq)
            offset = round(offset, 2)
            duplex = ''
            if offset > 0:
                duplex = '+'
            else:
                duplex = '-'

            rx_channel = [-1, self.rx_freq, self.callsign, "TSQL", "88.5", self.squelch, "023", "023", "NN", "Tone->Tone", duplex, f"{offset}", "FM", "2.5", "5.0W", f"{self.callsign} - RX"]
            # tx_channel = [-1, self.tx_freq, -1, "TSQL", "88.5", self.squelch, "023", "023", "NN", "Tone->Tone", "", "", "FM", "2.5", "5.0W", f"{self.callsign} - TX"]
            return [rx_channel]
        else:
            return None

def getFile(filename):
    f = open(filename)
    reader = csv.reader(f)
    headers = next(reader)
    lines = []
    for line in reader:
        lines.append(line)
    return headers, lines

def createRepeaters(lines):
    repeaters = []
    for line in lines:
        callsign = line[0]
        rx_freq = line[1]
        tx_freq = line[2]
        mode = line[3]
        squelch = line[4]
        location = line[6]
        repeaters.append(Repeater(callsign, rx_freq, tx_freq, mode, squelch, location))
    return repeaters

def getChirps(repeaters):
    chirps = []
    counter = 1
    for r in repeaters:
        if r.getChirp() is not None:
            rx_chirp = r.getChirp()[0]
            rx_chirp[0] = str(counter-1)
            chirps.append(rx_chirp)
            counter += 1
    return chirps

def exportChirps(chirps, outfile):
    headers = ["Location", "Frequency", "Name", "Tone", "rToneFreq", "cToneFreq", "DtcsCode", "RxDtcsCode", "DtcsPolarity", "CrossMode", "Duplex", "Offset", "Mode", "TStep", "Power", "Comment"]
    f = open(outfile, "w+")
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(chirps)

def processRepeaters(repeater_file):
    output = getFile(repeater_file)
    repeaters = createRepeaters(output[1])
    chirps = getChirps(repeaters)
    exportChirps(chirps, "out_rep.csv")
