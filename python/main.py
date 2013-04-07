import cmd, os
import matrix

class MatrixCmd(cmd.Cmd):
    prompt = "MatCmd > "

    def __init__(self):
        cmd.Cmd.__init__(self)
        if not os.path.exists("../data"):
            os.mkdir("../data")
        self.matrix = matrix.Matrix("1 1")

    def do_init(self, rest):
        self.matrix = matrix.Matrix(rest)

    def do_config(self, rest):
        self.matrix.setConfig()

    def do_reset(self, rest):
        self.matrix.reset()

    def do_fill(self, rest):
        self.matrix.fill()

    def do_clip(self, rest):
        self.matrix.clip(rest)

    def do_flip(self, rest):
        self.matrix.flip()

    def do_show(self, rest):
        self.matrix.show()

    def do_save(self, rest):
        self.matrix.save()

    def do_load(self, rest):
        self.matrix.load()

    def do_submit(self, rest):
        self.matrix.submit(rest)

    def do_exit(self, rest):
        return True

matrixCmd = MatrixCmd()
matrixCmd.cmdloop()
