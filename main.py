import sys

from repeater import processRepeaters
from freq import processFreqencies

def main():
    processRepeaters(sys.argv[1])
    processFreqencies(sys.argv[2])



if __name__ == "__main__":
    main()
