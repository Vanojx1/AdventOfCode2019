class IntcodeProgram:

    class Istruction:
        def __init__(self, intcode, params, param_modes):
            self.should_inc_pointer = True
            self.exec(
                intcode,
                *zip(
                    params,
                    param_modes + ([0] * (len(params) - len(param_modes)))
                )
            )
            if self.should_inc_pointer:
                intcode.pointer += self.jump

    class Add(Istruction):
        jump = 4

        @staticmethod
        def exec(cls, p1, p2, p3):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            target = cls.get_index(*p3)
            cls.set(target, cls.get(a) + cls.get(b))

    class Multiply(Istruction):
        jump = 4

        @staticmethod
        def exec(cls, p1, p2, p3):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            target = cls.get_index(*p3)
            cls.set(target, cls.get(a) * cls.get(b))

    class Input(Istruction):
        jump = 2

        @staticmethod
        def exec(cls, p1):
            target = cls.get_index(*p1)
            cls.set(target, cls.get_input())

    class Output(Istruction):
        jump = 2

        @staticmethod
        def exec(cls, p1):
            a = cls.get_index(*p1)
            cls.set_output(cls.get(a))

    class JumpIfTrue(Istruction):
        jump = 3

        def exec(self, cls, p1, p2):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            if cls.get(a) != 0:
                cls.set_pointer(cls.get(b))
                self.should_inc_pointer = False

    class JumpIfFalse(Istruction):
        jump = 3

        def exec(self, cls, p1, p2):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            if cls.get(a) == 0:
                cls.set_pointer(cls.get(b))
                self.should_inc_pointer = False

    class LessThan(Istruction):
        jump = 4

        @staticmethod
        def exec(cls, p1, p2, p3):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            target = cls.get_index(*p3)
            if cls.get(a) < cls.get(b):
                cls.set(target, 1)
            else:
                cls.set(target, 0)

    class Equal(Istruction):
        jump = 4

        @staticmethod
        def exec(cls, p1, p2, p3):
            a = cls.get_index(*p1)
            b = cls.get_index(*p2)
            target = cls.get_index(*p3)
            if cls.get(a) == cls.get(b):
                cls.set(target, 1)
            else:
                cls.set(target, 0)

    class Exit(Istruction):
        jump = 0

        @staticmethod
        def exec(cls):
            cls.halt()

    istructions_lib = {
        1: Add,
        2: Multiply,
        3: Input,
        4: Output,
        5: JumpIfTrue,
        6: JumpIfFalse,
        7: LessThan,
        8: Equal,
        99: Exit
    }

    def __init__(self, intcode, input_value=0):
        self.input = [input_value]
        self.output = None
        self.intcode = intcode.copy()
        self.pointer = 0
        self.halted = False

    def get_index(self, index, mode):
        if mode == 0:
            return self.intcode[index]
        else:
            return index

    def fetch_opcode(self, opcode):
        str_opcode = str(opcode)
        if len(str_opcode) == 1 or opcode == 99:
            return opcode, []
        else:
            return int(str_opcode[2:]), \
                list(map(lambda i: int(i), str_opcode[:-2]))[::-1]

    def set(self, index, value):
        self.intcode[index] = value

    def get(self, index):
        return self.intcode[index]

    def set_input(self, value):
        self.input.insert(0, value)

    def get_input(self):
        return self.input.pop()

    def set_output(self, value):
        self.output = value

    def set_pointer(self, value):
        self.pointer = value

    def halt(self):
        self.halted = True

    def next(self):
        opcode, param_modes = self.fetch_opcode(self.intcode[self.pointer])
        fn = self.istructions_lib[opcode]
        fn(
            self,
            range(self.pointer+1, self.pointer+fn.jump),
            param_modes
        )

    def run(self):
        self.output = None
        while not self.halted and self.output is None:
            self.next()
