import json, pickle, random, re, sys, urllib
import config, lib

class Matrix(object):
    # Override super methods
    def __init__(self, string):
        args = string.split()
        pack = [int(arg) for arg in args]
        row, col = pack
        self.matrix = [[0 for colId in xrange(col)] for rowId in xrange(row)]
        self.config = config.Config()

    # Public methods
    def setConfig(self):
        self.config.inputConfig()

    def fill(self):
        row = len(self.matrix)
        col = len(self.matrix[0])
        numbers = range(row * col)
        random.shuffle(numbers)
        for rowId in xrange(row):
            for colId in xrange(col):
                self.matrix[rowId][colId] = numbers[rowId * col + colId]

    def clip(self, string):
        rowMatch = re.search(r"row\s+(\d+)\s+(\d+)", string)
        if rowMatch:
            begin = int(rowMatch.group(1))
            end = int(rowMatch.group(2))
            self.__rowClip(begin, end)
        colMatch = re.search(r"col\s+(\d+)\s+(\d+)", string)
        if colMatch:
            begin = int(colMatch.group(1))
            end = int(colMatch.group(2))
            self.__colClip(begin, end)

    def flip(self):
        self.matrix = [[row[colId] for row in self.matrix] for colId in xrange(len(self.matrix[0]))]

    def show(self):
        for row in self.matrix:
            for col in row:
                print "%02d" % col,
            print

    def save(self):
        pickle.dump(self.matrix, open(lib.dataPath, "w"))

    def load(self):
        try:
            self.matrix = pickle.load(open(lib.dataPath))
        except IOError:
            print >>sys.stderr, "No Saved Data!"

    def submit(self, string):
        params, headers = self.__preprocess()
        string = string.strip()
        if string in ["get", "post"]:
            exec "lib.%sSubmit(params, headers, self.config)" % string
        else:
            print >>sys.stderr, "Unknown Submit Method!"

    # Private Methods
    def __rowClip(self, begin, end):
        self.matrix = self.matrix[begin:end]

    def __colClip(self, begin, end):
        self.matrix = [row[begin:end] for row in self.matrix]

    def __preprocess(self):
        data = json.dumps(self.matrix)
        paramDict = {"username": self.config.user, "matrix": data}
        params = urllib.urlencode(paramDict)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        return params, headers

