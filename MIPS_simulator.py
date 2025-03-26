#MIPS simulator
class MIPS_Sim:
    #program initialization
    def __init__(self):
        #given register and memory
        self.reg = {'$t0': 0, '$t1': 0, '$t2': 6, '$t3': 4, '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0}
        self.mem = {}

        #line counter of the program
        self.counter = 0
        #list of labels for branching
        self.labels = {}

    #execute the program
    def parser(self, prog):
        lines = prog.splitlines()

        #finds all labeled branches given in the program
        for i, line in enumerate(lines):
            line = line.strip()

            #finds branches copies the location of the branch to a new list
            if line.endswith(":"):
                label = line[:-1]
                self.labels[label] = i

        lines = [line for line in lines if not line.endswith(":")]
        
        return lines
    
    #instruction executor
    def execute(self, prog):
        line = self.parser(prog)

        #loops through program line by line and strips then splits the instructions of each line into an array
        while self.counter < len(line):
            inst = line[self.counter].strip()
            x = inst.split()
            operator = x[0]

            #finds the instruction that is given in the provided line
            if operator == 'add':
                self.add(x)
            elif operator == 'sub':
                self.sub(x)
            elif operator == 'lw':
                self.lw(x)
            elif operator == 'sw':
                self.sw(x)
            elif operator == 'beq':
                self.beq(x)
            elif operator == 'bgt':
                self.bgt(x)
            else:
                print("Unrecognized Instruction {operator}")
            
            self.counter += 1
        
        self.display_state()


    #instruction functions

    #'add' instruction
    def add(self, x):
        rd = x[1]
        rs = x[2]
        rt = x[3]
        self.reg[rd] = self.reg[rs] + self.reg[rt]
    
    #'sub' instruction
    def sub(self, x):
        rd = x[1]
        rs = x[2]
        rt = x[3]
        self.reg[rd] = self.reg[rs] - self.reg[rt]
    
    #lw instruction
    def lw(self, x):
        rt = x[1]
        offset = int(x[2])
        self.reg[rt] = self.mem.get(offset, 0)

    #'sw' instruction
    def sw(self, x):
        rt = x[1]
        offset = int(x[2])
        self.mem[offset] = self.reg[rt]
    
    #'beq' instruction
    def beq(self, x):
        rs = x[1]
        rt = x[2]
        z = x[3]
        if self.reg[rs] == self.reg[rt]:
            self.counter = self.labels[z] - 1
    
    #'bgt' instruction
    def bgt(self, x):
        rs = x[1]
        rt = x[2]
        z = x[3]
        if self.reg[rs] == self.reg[rt]:
            self.counter = self.labels[z] - 1


    #display final state
    def display_state(self):
        print("Final Register State: ", self.reg)
        print("Final Memory State: ", self.mem)

    
#example program
program_list = [
    "add $t1 $t2 $t3",
    "sub $t4 $t1 $t2",
    "sw $t4 100",
    "lw $t5 100",
    "beq $t5 $t4 loop",
    "add $t6 $t5 $t3",
    "loop:",
    "sub $t7 $t5 $t3",
    "bgt $t7 $t2 end",
    "add $t6 $t7 $t4",
    "end:"
]
#splitlines cant be run with a list so I turned it into a string, it also wouldnt work as a normal string but this did work so here you go
program = '\n'.join(program_list)

#run the program
simulator = MIPS_Sim()
simulator.execute(program)