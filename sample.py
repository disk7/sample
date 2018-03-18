# ===========================
#  Package Using Declaration
# ===========================
from pathlib import Path
import csv
import re

# =============================
#  Grobal Variables Definition
# =============================
#(None)

# ===================
#  Functions
# ===================
def getConfig(fname):
    # Open Configuration File #
    fp = open(fname, "r", encoding="ms932", errors="", newline="" )
    file = csv.reader(fp, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    # Store Contents #
    cfg = []
    for line in file:
        cfg.append(line)

    # Close Configuration File #
    fp.close()

    return cfg

def getDirectories(root):
    # Get Path Object #
    path = Path(root)

    # Store Contents #
    dirs = []
    for dir in path.iterdir():
        if dir.is_dir():
            dirs.append(dir)

    return dirs

def readData(dir):
    # Declare Local Variables #
    data = {}       # Model Data (dict)
    subset = ""     # Subset Name (string)
    dupli = {}      # For Duplicaton Check (dict{string: int})

    # Glob CSV File #
    fnames = dir.glob('*.csv')

    # Loop #
    for fname in fnames:
        # Print File Name #
        print("file:", fname)

        # Search Model Data #
        m = re.search("/(?P<name>N00[012])_(?P<subset>(?P<type>Outer|Inner)_[a-zA-Z0-9]+_[a-zA-Z0-9]+).csv", str(fname))
        if m:
            # Extract Names #
            name = m.group("name")
            subset = m.group("subset")

            # Open Data File #
            fp = open(fname, "r", encoding="ms932", errors="", newline="" )
            file = csv.reader(fp, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

            # Remove Header #
            next(file)

            # Store Contents #
            contents = []
            for line in file:
                contents.append(line[1:])
            data[name] = contents
            dupli[subset] = 1   # value is dummy.

            # Close Data File #
            fp.close()
        else:
            print("--- Warning!!! Illegal File:", fname)

    # Check Subset Pattern #
    if len(dupli) > 1:
        print("--- Abort!!! Detected illegal subset pattern.", dupli.keys())
        exit()

    return data, subset

# ================
#  Main Process
# ================
# Get Configuration #
cfg = getConfig("./input/pattern.csv")

# Get Directory #
dirs = getDirectories("./input")

# Loop #
for dir in dirs:
    # Read Model Data #
    print("----dir: ", dir)
    data, subset = readData(dir)

    # Open Result File #
    outfile = str(dir) + "/" + subset + ".csv"
    fp = open(outfile, 'w')
    file = csv.writer(fp, lineterminator='\n')

    # Write Header #
    header = ["x", "y", "z"]
    file.writerow(header)

    # Write Body #
    for order in cfg:
        name = order[1]
        print("name:", name)
        for line in data[name]:
            print(line)
            file.writerow(line)

    # Close Result File #
    fp.close()

# Finish Script #
exit()
