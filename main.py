import csv
import sys

class Repeater:
    def __init__(self, callsign, rx_freq, tx_freq, mode, squelch) -> None:
        self.callsign = callsign
        self.rx_freq = rx_freq
        self.tx_freq = tx_freq
        self.mode = mode
        self.squelch = squelch

    def out(self):
        return f"{self.callsign} - RX: {self.rx_freq}, TX: {self.tx_freq}"

    def __str__(self) -> str:
        return self.out()
    def __repr__(self) -> str:
        return self.out()

    def getChirp(self):
        if self.mode == "FM" and self.squelch and self.squelch.replace(".", "").isdigit():
            rx_channel = [-1, self.rx_freq, -1, "TSQL", "88.5", self.squelch, "023", "023", "NN", "Tone->Tone", "", "", "FM", "2.5", "5.0W", f"{self.callsign} - RX"]
            tx_channel = [-1, self.tx_freq, -1, "TSQL", "88.5", self.squelch, "023", "023", "NN", "Tone->Tone", "", "", "FM", "2.5", "5.0W", f"{self.callsign} - TX"]
            return [rx_channel, tx_channel]
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
        repeaters.append(Repeater(callsign, rx_freq, tx_freq, mode, squelch))
    return repeaters

def getChirps(repeaters):
    chirps = []
    counter = 1
    for r in repeaters:
        if r.getChirp() is not None:
            (rx_chirp, tx_chirp) = r.getChirp()
            rx_chirp[0] = str(counter-1)
            tx_chirp[0] = str(counter)
            rx_chirp[2] = "CH{:03d}".format(counter)
            tx_chirp[2] = "CH{:03d}".format(counter+1)
            chirps.extend([rx_chirp, tx_chirp])
            counter += 2
    return chirps

def exportChirps(chirps, outfile):
    headers = ["Location", "Frequency", "Name", "Tone", "rToneFreq", "cToneFreq", "DtcsCode", "RxDtcsCode", "DtcsPolarity", "CrossMode", "Duplex", "Offset", "Mode", "TStep", "Power", "Comment"]
    f = open(outfile, "w+")
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(chirps)


if __name__ == "__main__":
    output = getFile(sys.argv[1])
    repeaters = createRepeaters(output[1])
    chirps = getChirps(repeaters)
    exportChirps(chirps, "out.csv")
