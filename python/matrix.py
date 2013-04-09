import json, pickle, random, re, sys, urllib
import config, lib

class Matrix(object):
    # Override super methods
    def __init__(self, string):
        args = string.split()
        row = int(args[0])
        col = int(args[1])
        self.matrix = [[0 for colId in xrange(col)] for rowId in xrange(row)]
        self.config = config.Config()

    # Public methods
    def setConfig(self):
        self.config.inputConfig()

    def reset(self):
        self.config.reset()

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
            self._rowClip(begin, end)
        colMatch = re.search(r"col\s+(\d+)\s+(\d+)", string)
        if colMatch:
            begin = int(colMatch.group(1))
            end = int(colMatch.group(2))
            self._colClip(begin, end)

    def flip(self):
        self.matrix = [[row[colId] for row in self.matrix]
                                   for colId in xrange(len(self.matrix[0]))]

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
        params, headers = self._preprocess()
        string = string.strip()
        funcs = {"get": lib.getSubmit, "post": lib.postSubmit}
        if string in funcs:
            funcs[string](params, headers, self.config)
        else:
            print >>sys.stderr, "Unknown Submit Method!"

    # Private Methods
    def _rowClip(self, begin, end):
        self.matrix = self.matrix[begin:end]

    def _colClip(self, begin, end):
        self.matrix = [row[begin:end] for row in self.matrix]

    def _preprocess(self):
        data = json.dumps(self.matrix)
        paramDict = {"username": self.config.user, "matrix": data}
        params = urllib.urlencode(paramDict)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        return params, headers

