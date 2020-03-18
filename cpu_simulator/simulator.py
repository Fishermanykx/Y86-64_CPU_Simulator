'''
@Description: Y86指令集CPU模拟器
@Author: Fishermanykx
@Date: 2020-03-17 20:59:08
@LastEditors: Fishermanykx
@LastEditTime: 2020-03-18 23:54:58
'''
from pprint import pprint


class CPUSimulator:

  def __init__(self, filename):
    ## 将内存分为不同的区域，每位代表一个数字(4bit)
    # 规定各部分大小
    self.max_ins_mem_size = 1024
    self.max_data_mem_size = 1024
    self.max_stack_size = 1024
    # 初始化内存各区域
    self.instruction_memory = []  # 指令区域
    self.data_memory = [0] * self.max_data_mem_size
    # 初始化寄存器文件(str-int)
    self.regFile = {}  # 寄存器文件，编号依次为字符0~7
    for i in range(8):
      self.regFile[str(i)] = 0
    # 初始化栈区
    # self.stack = []
    # 读入指令，并将其存储在instruction_memory中
    inf = open(filename + ".bin", "r")
    instruction_memory = ''
    while True:
      line = inf.readline()
      if line == '':
        break
      line = line.strip()[4:]
      instruction_memory += line
    inf.close()
    # 将指令按字节切分
    for bit in range(0, len(instruction_memory), 2):
      self.instruction_memory.append(instruction_memory[bit] +
                                     instruction_memory[bit + 1])
    # print(self.instruction_memory)
    ## 初始化条件码
    self.cc = {"ZF": 0, "SF": 0, "OF": 0}  # ZF: 为0；SF: 为负；OF: 溢出
    ## 初始化PC
    self.pc = 0
    ## 初始化状态码
    self.stat = "AOK"
    self.stat_list = ["AOK", "HLT", "ADR", "INS"]

  def MainCycle(self):
    self.f_predPC_reg = 0
    self.do_fun_related_jmp = 0  # M阶段出结果
    self.fun_jmp_dest = 0  # 函数跳转的目的地
    self.do_jmp = 0  # jxx指令跳转，E阶段出结果
    self.jmp_dest = 0  # 跳转目标的目的地
    while self.stat == "AOK":
      # F-Register
      self.f_predPC = self.f_predPC_reg
      ## Fetch
      self.Fetch()

  def Fetch(self):
    '''
    @description: 取指阶段
    @param {type} 
    @return: 取出的二进制指令(str)
    '''
    # select PC
    if self.do_jmp:
      f_pc = self.jmp_dest
    elif self.do_fun_related_jmp:
      f_pc = self.fun_jmp_dest
    else:
      f_pc = self.f_predPC
    # 取指
    (f_icode, f_ifun) = self.instruction_memory[f_pc]
    cur_ins_len = 0
    # 判断取出指令的长度(单位：byte)
    if f_icode == 0 or f_icode == 1 or f_icode == 9:
      cur_ins_len = 1
    elif f_icode == 2 or f_icode == 6 or f_icode == 'A' or f_icode == 'B':
      cur_ins_len = 2
    elif f_icode == 7 or f_icode == 8:
      cur_ins_len = 5
    elif f_icode == 3 or f_icode == 4 or f_icode == 5:
      cur_ins_len = 6
    else:
      self.stat = 'INS'
      print("Error! Error type: " + self.stat +
            "at instruction which starts from %d" % f_pc)
      exit(1)
    # 计算正常情况下的PC_next
    valP = f_pc + cur_ins_len
    f_valC = None
    # 计算predictPC
    if f_icode == 7 or f_icode == 8:
      # 计算f_valC
      imm_str = ''
      for i in range(1, 5):
        imm_str += self.instruction_memory[f_pc + i]
      f_valC = self.ConvertImmNum(imm_str)
      if f_ifun == 0:  # 无条件跳转
        self.f_predPC_reg = f_valC
    else:
      self.f_predPC_reg = valP

    # imem_error
    if self.f_predPC_reg > self.max_ins_mem_size:
      print(
          "Error: Instruction memory exceeded! Max instruction memory size is: %d byte."
          % self.max_ins_mem_size)
      exit(1)

    ## 取出单条指令并返回
    res_ins = {
        "D_stat": "AOK",
        "D_icode": f_icode,
        "D_ifun": f_ifun,
        "D_rA": '',
        "D_rB": '',
        "D_valC": f_valC,
        "D_valP": valP
    }
    if cur_ins_len == 1:
      res_ins["D_rA"] = 'F'
      res_ins["D_rB"] = 'F'
    elif cur_ins_len == 2:
      (rA, rB) = self.instruction_memory[f_pc + 1]
      res_ins["D_rA"] = rA
      res_ins["D_rB"] = rB
    elif cur_ins_len == 6:
      imm_str = ''
      for i in range(2, 2 + 4):
        imm_str += self.instruction_memory[f_pc + i]
      f_valC = self.ConvertImmNum(imm_str)
    else:
      print("Error! Error type: " + self.stat +
            "at instruction which starts from %d" % f_pc)
      exit(1)

    return res_ins

  def Decode(self, ins):
    '''
    @description: 译码阶段: 将二进制指令转换为opcode与操作数(十进制int)
    @param {type}: ins{str}
    @return: list
    '''
    opcode = ins[0:2]
    res = []
    # 根据指令类型切分
    op_type = int(opcode[0])
    if op_type == 0:
      self.has_next_ins = False
      res = ["00"]
    elif op_type == 1:
      res = ["00"]
    elif op_type == 2:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
    elif op_type == 3:
      res.append(opcode)
      res.append(None)
      res.append(self.regFile[int(ins[3])])
      res.append(self.ConvertImmNum(ins[4:]))
    elif op_type == 4 or op_type == 5:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
      res.append(self.ConvertImmNum(ins[4:]))
    elif op_type == 6:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(self.regFile[int(ins[3])])
    elif op_type == 7 or op_type == 8:
      res.append(opcode)
      res.append(self.ConvertImmNum(ins[2:]))
    elif op_type == 8:
      res.append(opcode)
    elif op_type == 10 or op_type == 11:
      res.append(opcode)
      res.append(self.regFile[int(ins[2])])
      res.append(None)
    else:
      print("Error: Illegal instruction. Exit code: INS")
      exit(1)
    return res

  def Execute(self, slided_ins):
    '''
    @description: 执行阶段
    @param {type} 根据opcode与操作数执行指令
    @return: 计算所得的结果
    '''

  def Memory(self):
    '''
    @description: 访存阶段
    @param {type} 
    @return: 将执行阶段的值写回内存或从内存中取出值
    '''
    pass

  def WriteBack(self):
    '''
    @description: 写回阶段
    @param {type} 
    @return: 将计算结果写回寄存器文件
    '''
    pass

  def ConvertImmNum(self, num_str):
    '''
    @description: 将用小端法表示的立即数转换为十进制整数
    @param {type} num_str {str}
    @return: int
    '''
    '''
    >>> ConvertImmNum("10000000")
    16
    >>> ConvertImmNum("10100000")
    4112
    '''
    # 将立即数反转为正常顺序
    rev_str = ""
    for i in range(6, 0, -2):
      rev_str += (num_str[i] + num_str[i + 1])
    return int("0x" + rev_str, 16)


if __name__ == "__main__":
  simulator = CPUSimulator(
      "D:/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  )  # Windows
  # simulator = CPUSimulator(
  #     "/media/fisher/DATA/Materials_Study/Computer_Science/Computer_Architecture/Exercises/Y86-64_CPU_Simulator/cpu_simulator/testbench"
  # )  # Linux
  # simulator.MainProcess()
  reg = str(0)
  print(simulator.regFile[reg])  # 结果的值在rax里
