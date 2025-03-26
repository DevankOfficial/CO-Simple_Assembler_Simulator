from sys import stdout
#from typing_extensions import IntVar

A_TYPE={"add":"10000","sub": "10001","mul":"10110","xor":"11010","or":"11011","and":"11100"}
B_TYPE={"mov" : "10010","rs":"11000","ls":"11001" }   
C_TYPE={"mov": "10011","div":"10111","not":"11101","cmp":"11110"}
D_TYPE={"ld":"10100","st":"10101"}
E_TYPE={"jmp":"11111","jlt":"01100","jgt":"01101","je":"01111"}
F_TYPE={"hlt":"01010"} 

file_1=stdout
from sys import stdin

E_Flag_2=False
Label_Label=[]
Variables_Variables=[]

Memory_Addresss=[None]*256
reg_list = {"R0":"0000000000000000", "R1":"0000000000000000", "R2":"0000000000000000", "R3":"0000000000000000",
 "R4": "0000000000000000", "R5": "0000000000000000", "R6":"0000000000000000","FLAGS":"0000000000000000"}

Allowed_Register_Names = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4": "100", "R5": "101", "R6":"110","FLAGS":"111"}  
Allowed_Label_Names=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_","1","2","3","4","5","6","7","8","9","0",":"]

Memory=["0"*16]*256 #Memory Dump

line_no=1


pc=0 #Program counter --- updates after every instruction
def Imm(NUMBER):
    NUMBER=int(NUMBER)
    Binary=""
    while NUMBER:
        Binary=str(NUMBER%2)+Binary
        NUMBER=NUMBER//2
    lenght=len(Binary)
    if lenght>16:
        return Binary[len(Binary)-16:]
    while len(Binary)<16:
        Binary="0"+Binary
    return Binary

def Shift_L(bin,imm):
    shift=str("0"*int(imm))
    bin=bin+shift
    bin=bin[int(imm):]
    return bin

def Shift_R(binary,imm):
    shift=str("0"*int(imm))
    binary=shift+bin
    binary=binary[0:16]
    return binary

def Return_Register(reg): #returns the Register 
    for key, value in Allowed_Register_Names.items():
        if value==reg:
            return key

def Return_Instruction(Type,Instruction_Key,BINARY_VALUE,element):
    instruct=""
    if Type=="B":
        r1=Return_Register(BINARY_VALUE[5:8])
        imm=int(BINARY_VALUE[8:],2)

        instruct=Instruction_Key+" "+r1+" "+ str(imm)
        
    elif Type=="A":
        r1=Return_Register(BINARY_VALUE[7:10])
        r2=Return_Register(BINARY_VALUE[10:13])
        r3=Return_Register(BINARY_VALUE[13:])
        instruct=Instruction_Key + " " + r1+" "+ r2+" "+ r3
        
    elif Type=="C":
        r1=Return_Register(BINARY_VALUE[10:13])
        r2=Return_Register(BINARY_VALUE[13:])
        instruct=Instruction_Key+" "+r1+" "+r2
        
    elif Type=="D":
        r1=Return_Register(BINARY_VALUE[5:8])
        Memory=int(BINARY_VALUE[8:],2)
        Memory_Addresss[Memory]=["var "+"x"]
        instruct=Instruction_Key+" "+r1+" " +str(Memory)  

    elif Type=="E":
        Memory=int(BINARY_VALUE[8:],2) 
        instruct=Instruction_Key+" "+ str(Memory)
        
    Memory_Addresss[element]=[instruct]+ [Type] 
  


def Instruction_Execution(inst,Type,pc):
    
    global Memory
    inst=inst.split(" ")

    if Type=="B":

        """ This type contains mov, rs, ls; 
            which perform operations with the semantic of (<operation> RegA $Imm) ,
            i.e., the intruction performs its operation on RegA with the immediate $Imm,and 
            then stores it on RegA.
        """
        if inst[0]=="mov":
            reg_list[inst[1]]=Imm(inst[2])
            
        elif inst[0]=="ls":
            reg_list[inst[1]]=Shift_L(reg_list[inst[1]],inst[2])
            
        elif inst[0]=="rs":
            reg_list[inst[1]]=Shift_R(reg_list[inst[1]],inst[2])
            
        Flag_Reset()
    elif Type=="A": 
        """ This type contains add, sub, mul, xor, or & and;
            which perform operations with the semantic of (<operation> RegC RegA RegB) ,
            i.e., the intruction performs its operation on RegA & RegB ,and then stores it on RegC.
        """
        A=int(reg_list[inst[2]],2)
        B=int(reg_list[inst[3]],2)

        if inst[0]=="add":
            C=B+A
            if C>65535:
                reg_list[inst[1]]=Imm(C)
                reg_list["FLAGS"]=reg_list["FLAGS"][0:12]+"1"+reg_list["FLAGS"][13:]
            else:
                reg_list[inst[1]]=Imm(C)
            
                
        elif inst[0]=="sub":
            C=A-B
            if C>=0:
                reg_list[inst[1]]=Imm(C)
            else:
                reg_list[inst[1]]="00000000"
                reg_list["FLAGS"]=reg_list["FLAGS"][0:12]+"1"+reg_list["FLAGS"][13:]
            
        elif inst[0]=="mul":
            C=A*B
            if C>65535:
                reg_list[inst[1]]=Imm(A*B)
                reg_list["FLAGS"]=reg_list["FLAGS"][0:12]+"1"+reg_list["FLAGS"][13:]
            else:
                reg_list[inst[1]]=Imm(A*B)
            
        elif inst[0]=="xor":
            reg_list[inst[1]]=Imm(A^B)
            Flag_Reset()
        elif inst[0]=="or":
            reg_list[inst[1]]=Imm(A|B)
            Flag_Reset()
        elif inst[0]=="and":
            reg_list[inst[1]]=Imm(A&B)
            Flag_Reset()


    elif Type=="C":
        """ This type contains mov, div , not, & cmp;
            which perform operations with the semantic of (<operation> RegA RegB) ,
            i.e., the intruction performs its operation on RegB, and then stores it on RegA.
        """
        A=int(reg_list[inst[1]],2)
        B=int(reg_list[inst[2]],2)
        if inst[0]=="div":
            C = A/B
            D = A%B
            reg_list["R0"] = format(C, '08b')
            reg_list["R1"] = format(D, '08b')
            Flag_Reset()
        elif inst[0]=="not":
            C = ~B
            C = format(C, '08b')
            reg_list[inst[1]] = C
            Flag_Reset()
        elif inst[0]=="cmp":
            
            if A==B:
                reg_list["FLAGS"] = reg_list["FLAGS"][0:15] + "1"
            elif A>B:
                reg_list["FLAGS"] = reg_list["FLAGS"][0:14] + "1" + reg_list["FLAGS"][15]
            else:
                reg_list["FLAGS"] = reg_list["FLAGS"][0:13] + "1" + reg_list["FLAGS"][14:]
            

        elif inst[0]=="mov":
            reg_list[inst[1]] = reg_list[inst[2]]
            Flag_Reset()

    elif Type=="D":
        """ This type contains ld & st;
            which perform operations with the semantic of (<operation> RegA memory_Address) ,
            i.e., the intruction performs either loads data from memory_Address into RegA, or 
            stores data from RegA to memory_Address.
        """
        if inst[0] == "ld":
            reg_list[inst[1]] = Memory[int(inst[2])]
        elif inst[0] == "st":
            Memory[int(inst[2])] = reg_list[inst[1]]
        Flag_Reset()

    elif Type=="E":

        """ This type contains jmp, jlt, jgt & je;
            which perform follow the semantic of (<operation> memory_Address) ,
            i.e., the intruction jumps to the given memory address either conditionally, or 
            unconditionally.
        """

        if inst[0]=="jgt":
            if reg_list["FLAGS"][-2]=="1":
                pc= int(inst[1])
                Flag_Reset()
                return pc
            Flag_Reset()

        elif inst[0]=="jlt":
            if reg_list["FLAGS"][-3]=="1":
                pc=int(inst[1])
                Flag_Reset()
                return pc
            Flag_Reset()

        elif inst[0]=="jmp":
            pc=int(inst[1])
            Flag_Reset()
            return pc
            
        elif inst[0]=="je":
            if reg_list["FLAGS"][-1]=="1":
                pc=int(inst[1])
                Flag_Reset()
                return pc
            
            Flag_Reset()

        else:
            1

    return (pc+1) 
    

j=0
Halt=False
line_no=1


while(not Halt):
    BINARY_VALUE=input()
    Memory[j]=(BINARY_VALUE)
    if(BINARY_VALUE=="0101000000000000"):
        Memory_Addresss[j]=["hlt"]
        Halt=True
        break
    OPc=BINARY_VALUE[:5]
    Instruction_Key=""
    for Key, Value in B_TYPE.items():
        if Value==OPc:
            Type="B"
            Instruction_Key=Key

    for Key, Value in A_TYPE.items():
        if Value==OPc:
            Type="A"
            Instruction_Key=Key
            
            
    for Key, Value in C_TYPE.items():
        if Value==OPc:
            Type="C"
            Instruction_Key=Key
            
    for Key, Value in D_TYPE.items():

        if Value==OPc:
            Type="D"
            Instruction_Key=Key
            
    for Key, Value in E_TYPE.items():
        if Value==OPc:
            Type="E"
            Instruction_Key=Key
    Return_Instruction(Type,Instruction_Key,BINARY_VALUE,j)
    j+=1
def Flag_Reset():
    reg_list["FLAGS"]="0"*16
pc=0
Halt=False
C=0

while (not Halt) : 
    
    Type=""
    inst=""
    if Memory_Addresss[pc]==["hlt"]:
        Halt=True
    inst=Memory_Addresss[pc][0]
    mem_lenght=len(Memory_Addresss[pc])
    if mem_lenght>1:
        Type=Memory_Addresss[pc][1]

    i=Instruction_Execution(inst,Type,pc) 
    #Printing the required output
    # file_1.write()
    # file_1.write((format(pc, '08b')),end=" ")
    # file_1.write(reg_list["R0"],reg_list["R1"],reg_list["R2"],reg_list["R3"],reg_list["R4"],reg_list["R5"],reg_list["R6"],end=" ")
    # file_1.write(reg_list["FLAGS"])
    print()
    print((format(pc, '08b')),end=" ")
    print(reg_list["R0"],reg_list["R1"],reg_list["R2"],reg_list["R3"],reg_list["R4"],reg_list["R5"],reg_list["R6"],end=" ")
    print(reg_list["FLAGS"])
    
    pc=i #Program counter is updated
    
    line_no+=1  
   
    
for i in range(len(Memory)): # Memory Dump of the program.
    print(Memory[i])


file_1.close()