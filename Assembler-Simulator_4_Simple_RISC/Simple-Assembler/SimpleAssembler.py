import sys
from sys import stdout

Updated_List_of_Data=[]
Memmory_Address=[]
Label_Address={}


# File_main_open = open('C:/Python/CO_PROJECT/errors.txt','w')


Memory_Address=[]
i=0                 #line counter

Allowed_Instructions=["add","sub","mul","xor","or","and","mov","rs","ls","div","not","cmp",
                      "ld","st","jmp","jlt","jgt","je","hlt"]
Allowed_Register_Names=["R0","R1","R2","R3","R4","R5","R6","FLAGS"]  
Allowed_Label_Names=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","_","1","2","3","4","5","6","7","8","9","0",":"]

A_TYPE={"add":"10000","sub": "10001","mul":"10110","xor":"11010","or":"11011","and":"11100"}
B_TYPE={"mov" : "10010","rs":"11000","ls":"11001" }   
C_TYPE={"mov": "10011","div":"10111","not":"11101","cmp":"11110"}
D_TYPE={"ld":"10100","st":"10101"}
E_TYPE={"jmp":"11111","jlt":"01100","jgt":"01101","je":"01111"}
F_TYPE={"hlt":"01010"} 
E_Flag_2 = False
Label_Label=[]
Variables_Variables=[]
#this is error dictionary
errors={ 1 : "[ Error Detected : Typos in instruction name or register name at line {}",
 2: "[Error Detected] : Use of undefined variable at line {}",
 3: "[Error Detected] : Use of undefined labels at line {}",
 4:"[Error Detected] : Illegal use of FLAGS register at line{}",
 5: "[Error Detected] : Illegal Immediate values (more than 8 bits) at line {}",
 6: "[Error Detected] : Variable name used instead of label name in line {}",
 7: "[Error Detected] : Label name used instead of variable name in line {}",
 8: "[Error Detected] : Variables not declared at the beginning", 
 9: "[Error Detected] : Missing hlt instruction", 
 10: "[Error Detected] : hlt not being used as the last instruction",
 11: "Error Detected : General Syntax Error in instruction in line {}",
 12:"[Error Detected] : Variable name is not valid (must be alphabet or number) in line {}",
 13: "[Error Detected] : Variable used already initialised in memory {}",
 14: "[Error Detected] : immediate value should be an integer in line {}",
 15:"[Error Detected] : Gap between two lines detected at line {}"
       } 

def FInd_Type(var): #Finds the type of instruction
    if var:
        One_Position=var[0]
        Memory=""
        for i in var:
            Memory+=i
        if One_Position == "hlt":
            return "F"
        elif One_Position in A_TYPE.keys():
            return "A"
        elif One_Position in B_TYPE.keys() and ("$" in Memory):
            return "B"
        
        elif One_Position in D_TYPE.keys():
            return "D"
        elif One_Position in C_TYPE.keys():
            return "C"
        elif One_Position in E_TYPE.keys():
            return "E"
        
        elif ":" in One_Position:
            return "label"
        elif "var" == One_Position:
            return "variable"
        else:
            return "none"
    else:
        return "none"

def check_int(integer): # Check whether a certain variable has integer data type or not.
    try:
        int(integer)
        return True
    except ValueError:
        return False

class Lines:
    def __init__(self,line = list) -> None:
        self.line = line

    def Check_For_Valid_Label(line): #Checks if labelname is invalid
        # print(line,"Hello")
        for char in line:
            if not(char in Allowed_Label_Names):
                return False
        if(line.find(":")==len(line)-1):
            return True
        else:
            return False        

    def Instruction_check(line): #Checks if the instruction is invalid
        if line:
            if line[0]=="var":
                return False
            else :
                z1=0
                for i in Allowed_Instructions:
                    if line[0]==i:
                        return False
                # if line[0] in Allowed_Instructions:
                #     return False
                else:
                    if(Lines.Check_For_Valid_Label(line[0])):
                        return False
                    else:
                        return True
        else:
            return True

    def Line_CHECK(passed_line): #It returns the line no. from the original code
        z1=len(Main_Instruction)
        for j in range(z1):
            if passed_line == Main_Instruction[j]:
                return 1+j
            else:
                j= j+1
        return -(1)
        

class Err:

    def Typos_Error_Check(Instruction_Value): # Gives the type of instruction, input arg is in form of array of strings of each line
        global E_Flag_2
        Instruction_Type=FInd_Type(Instruction_Value)
        z3=Instruction_Type.split()
        if(z3[0]=="label"):
            x= Err.Typos_Error_Check(Instruction_Value[1: ])
            return x
        E_Flag_2 = Lines.Instruction_check(Instruction_Value)
        Exact_line = Lines.Line_CHECK(Instruction_Value)
        if not(E_Flag_2):
            return False
        else:
            return True

    def SYNTAX_ERROR(Instruction_Value): # Checks the syntax of the given line, and returns true if any error is found.
        global E_Flag_2
        Instruction_Type=FInd_Type(Instruction_Value)
        z2=Instruction_Type.split()
        if(z2[0]=="label"):
            a= Err.SYNTAX_ERROR(Instruction_Value[1 : ])
            return a


        if(Instruction_Type=="F"):
            if(Instruction_Value!=["hlt"]):
                E_Flag_2=True
                return(E_Flag_2)

        elif(Instruction_Type=="A"):
            if(len(Instruction_Value)!=4):
                E_Flag_2=True
                return(E_Flag_2)
            elif(not(Instruction_Value[1] in Allowed_Register_Names) or not(Instruction_Value[2] in Allowed_Register_Names) or not(Instruction_Value[3] in Allowed_Register_Names)):
                E_Flag_2=True
                
                print("[Error Detected] : Typos in register name\n")
                return(E_Flag_2)
        elif(Instruction_Type=="B"):
            if(len(Instruction_Value)!=3):
                E_Flag_2=True
                return(E_Flag_2)
            elif((Instruction_Value[1] not in Allowed_Register_Names) or str((Instruction_Value[2] )).find("$")!=0):
                E_Flag_2=True
                # print("[Error Detected] : Typos in register name")
                print("[Error Detected] : Typos in register name\n")
                return(E_Flag_2)
        elif(Instruction_Type=="C"):
            if(len(Instruction_Value)!=3):
                E_Flag_2=True
                return(E_Flag_2)
            elif(not(Instruction_Value[1] in Allowed_Register_Names) or not(Instruction_Value[2] in Allowed_Register_Names) ):
                E_Flag_2=True
                # print("[Error Detected] : Typos in register name")
                print("[Error Detected] : Typos in register name\n")
                return(E_Flag_2)
        elif(Instruction_Type=="D"):
            if(len(Instruction_Value)!=3):
                E_Flag_2=True
                return(E_Flag_2)
            elif(not(Instruction_Value[1] in Allowed_Register_Names)):
                E_Flag_2=True
                # print("[Error Detected] : Typos in register name")
                print("[Error Detected] : Typos in register name\n")
                return(E_Flag_2)
        elif(Instruction_Type=="E"):
            if(len(Instruction_Value)!=2):
                E_Flag_2=True
                return(E_Flag_2)
            elif(not(Instruction_Value[1] in Label_Label) ):
                E_Flag_2=True
                # print("[Error Detected] : Typos in register name")
                print("[Error Detected] : Typos in register name\n")
                return(E_Flag_2)
        else:
            return False

    def WronG_Var_Declaration(line):  # Returns true if undefined variable is used
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.WronG_Var_Declaration(line[1: ])
            return a
        if(Instruction_Type=="D"):
            if line[2] not in Variables_Variables :
                return True   
        return False

    def Gap_Line_Check(line): # Returns true if an empty gap between two lines is detected.
        if line == "":
            return True

    def Wrong_Label(line): #returns true if undefined label is used
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.Wrong_Label(line[1:])
            return a
        if(Instruction_Type=="E"):
            if line[1] not in Label_Label:
                return True
        return False


    def FLag_Reg_Error(line): #checks if flags are used incorrectly
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.FLag_Reg_Error(line[1:])
            return a
        if "FLAGS"in line:
            if(line[1] in Allowed_Register_Names) and (line[1]!="FLAGS" and line[2]=="FLAGS"):
                return False 
            else:
                return True
        else:
            return False

    def Imm_Val_Error(line): # Checks if immediate value is invalid.
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.FLag_Reg_Error(line[1:])
            return a
        if Instruction_Type=="B":
            Imm=int(line[2].replace("$",""))
            if(Imm>=256 or Imm<0) :
                return True

        return False  

    def ifValid_Var(line): # check if the given variable is valid.
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.ifValid_Var(line[1: ])
            return a
        if Instruction_Type=="variable":
            if len(line)>=2:
                if (line[1].isalnum()):
                    return False
            else:
                return True

        return False
   

    def Immediatie_Error_Check(line): # Checks the validity of variable from Type B.
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.Variable_Label_Check(line[1:])
            return a
        if Instruction_Type=="B":
            if not(check_int(line[2].replace("$",""))):
                return True
        return False

    def Label_Vriable_Check(line): # Checks the validity of variable from Type C.
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.Label_Vriable_Check(line[1:])
            return a
        if(Instruction_Type=="E" and (line[1] in Variables_Variables)):
            return True
        return False

    def Variable_Label_Check(line): # Checks the validity of variable from Type D.
        Instruction_Type=FInd_Type(line)
        if Instruction_Type=="label":
            a = Err.Variable_Label_Check(line[1:])
            return a
        if(Instruction_Type=="D" and (line[1] in Label_Label)):
            return True
        return False

    

""" this function checks all the possible errors"""
def Iterate_Error_Check(line):
    Exact_line = Lines.Line_CHECK(Instruction_Value) 
    # print(line)
    if Err.Typos_Error_Check(line):
        # print(errors[1].format(Exact_line))
        print(errors[1].format(Exact_line))
        E_Flag_2=True
        return E_Flag_2
    if Err.Label_Vriable_Check(line):
        
        print(errors[6].format(Exact_line))
        # print(str(errors[6].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.Variable_Label_Check(line):
        # print(errors[13].format(Exact_line))
        # print((errors[13].format(Exact_line)))
        print(errors[7].format(Exact_line))
        # print((errors[7].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.WronG_Var_Declaration(line):
        print(errors[2].format(Exact_line))
        # print((errors[2].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.Immediatie_Error_Check(line):
        print(errors[14].format( Exact_line))
        # print((errors[14].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.SYNTAX_ERROR(line):  
        print(errors[11].format(Exact_line))  
        # print((errors[11].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.Wrong_Label( line):
        print(errors[3].format( Exact_line))
        # print((errors[3].format( Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.FLag_Reg_Error(line):
        print(errors[4].format( Exact_line))
        # print((errors[4].format( Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.Imm_Val_Error(line):
        print(errors[5].format(Exact_line))
        # print((errors[5].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2    
    if Err.ifValid_Var(line):
        print(errors[12].format(Exact_line))
        # print((errors[12].format(Exact_line)))
        E_Flag_2=True
        return E_Flag_2
    if Err.Gap_Line_Check(line):
        print(errors[15].format(Exact_line))
        E_Flag_2=True
        return E_Flag_2


""" Main code"""


Main_Instruction=[]
LINES_LIST=[]

# with open(r'C:/Python/CO_PROJECT/errorsassembler.txt',"r") as f:
#     LINES_LIST=f.readlines()
Halted= False

while(not Halted):
    x=input()
    LINES_LIST.append(x)
    if ("hlt" in x):
        break




Original_Data=[Line for Line in LINES_LIST]
List_of_Data = [Line for Line in LINES_LIST if Line.strip() ] 
lenght=len(List_of_Data)
if(lenght)>256:
    print("Error Detected : The assembler can only write < or = 256 lines.")
    # print("Error Detected : The assembler can only write < or = 256 lines.")

for y in Original_Data:
    z = ""
    z=y.split()
    Main_Instruction.append(z)

for y in range(lenght): 
    Instruction_Value=List_of_Data[y].split()
    Updated_List_of_Data.append(Instruction_Value)
    
    if(FInd_Type(Instruction_Value)=="variable"):
        syze=len(Instruction_Value)
        if (syze)>=2 :
            if Instruction_Value[1] in Variables_Variables:
                print("Error Detected : Vague declaration in line "+str(Lines.Line_CHECK(Instruction_Value))+", you have declared variable "+Instruction_Value[1]+" already")
                E_Flag_2=True
                break
            Variables_Variables.append(Instruction_Value[1])
            Memmory_Address.append(Instruction_Value)
        else:
            print("Error Detected : Syntax for variable declaration is wrong ")
            E_Flag_2=True
            sys.exit()

    if(FInd_Type(Instruction_Value) !="variable"):
        Memory_Address.append(Instruction_Value)
        if(FInd_Type(Instruction_Value)=="label"):
            if(Instruction_Value[0].replace(":","")in Label_Label):
                if (Instruction_Value[0].replace(":","") in Memory_Address[Memory_Address.index(Instruction_Value)-1]):
                    pass
                else:
                    print("Error Detected : Vague declaration in line "+ str(Lines.Line_CHECK(Instruction_Value))+", you have declared variable "+Instruction_Value[0].replace(":","")+ " already")
                    E_Flag_2=True
                    break
                # Checks if label is declared twice   
            Label_Label.append(Instruction_Value[0].replace(":",""))
            Label_Address[Instruction_Value[0].replace(":","")]=Memory_Address.index(Instruction_Value)

N_variable = len(Memory_Address) 
Memory_Address=Memory_Address+Memmory_Address

#checks whether variable is initialised at the right location
check=True
for instruction in Updated_List_of_Data:
    type=FInd_Type(instruction)
    if (type!="variable"):
        check=False
    if(type=="variable" and check==False):
        E_Flag_2=True
        print(errors[8])
        # print(errors[8])
        sys.exit()

def FInd_Type1(line):# Checks if hlt instruction is misplaced
    type=FInd_Type(line)
    if type=="label":
        return FInd_Type1(line[1:])
    else:
        return type
# print(Variables_Variables)

#Updated_List_of_Data stores the updated instructions after removing all empty LINES_LIST and white spaces  
for Instruction_Value in Updated_List_of_Data:
    
    if Iterate_Error_Check(Instruction_Value):
        E_Flag_2=True
        sys.exit()
        
found=False
for instruction in range(len(Updated_List_of_Data)):
    type=FInd_Type1(Updated_List_of_Data[instruction])
    if type=="F":
        found=True
        if(instruction!=len(Updated_List_of_Data)-1):
            E_Flag_2=True
            print(errors[10])
            # print(errors[10])
            sys.exit()
            
            

if found==False: # Checks whether hlt instruction is missing
    E_Flag_2=True
    print(errors[9])
    # print(errors[9])
    sys.exit()
 
Reg_Memory = {"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4": "100", "R5": "101", "R6":"110","FLAGS":"111"}

def Bin_Converion(N):# Converts given integer to 8 bit binary
    BINARY_STR=""
    while N:
        BINARY_STR=str(N%2)+BINARY_STR
        N//=2
    sioze=len(BINARY_STR)
    while len(BINARY_STR)<8:
        BINARY_STR="0"+BINARY_STR
    return BINARY_STR   

def PRINT(Instruction_Value,TYPE):    
        Encoding_Value="\n"
        j=0

        if TYPE=="F":
            for i in range(0, len(Instruction_Value),1):
                if(Instruction_Value[i] !="hlt"):
                    pass
                else: 
                    break
            Encoding_Value="0101000000000000"

        elif TYPE =="A":
            #ignore labels and find executable instruction
            # while j<len(Instruction_Value):
            for j in range(0, len(Instruction_Value),1):          
                if(Instruction_Value[j]  in A_TYPE.keys()):
                    K=Instruction_Value[j]
                    break
                else: 
                    pass           
            OPcode=A_TYPE[K]
            Unused_Bit="00"
            Encoding_Value=OPcode+Unused_Bit+Reg_Memory[Instruction_Value[j+1]]+Reg_Memory[Instruction_Value[j+2]]+Reg_Memory[Instruction_Value[j+3]]

        elif TYPE == 'B':
            for j in range(0, len(Instruction_Value),1):
                if(Instruction_Value[j]  in B_TYPE.keys()):
                    K=Instruction_Value[j]
                    break
                else: 
                    pass
            OPcode=B_TYPE[K]
            Imm=Bin_Converion(int(Instruction_Value[j+2].replace("$","")))
            Encoding_Value=OPcode+Reg_Memory[Instruction_Value[j+1]]+Imm
            
        elif TYPE == 'C':
            for j in range(0, len(Instruction_Value),1):
                if(Instruction_Value[j] in C_TYPE.keys()):
                    K=Instruction_Value[j]
                    break
                else: 
                    pass
            OPcode=C_TYPE[K]
            Encoding_Value = OPcode+ "00000" + Reg_Memory[Instruction_Value[j+1]] + Reg_Memory[Instruction_Value[j+2]]
            
        elif TYPE == 'D':
            for j in range(0, len(Instruction_Value),1):
                if(Instruction_Value[j] in D_TYPE.keys()):
                    K=Instruction_Value[j]
                    break
                else: 
                    pass
            OPcode=D_TYPE[K]
            Var_memory_A = N_variable + Variables_Variables.index(Instruction_Value[j+2])
            Encoding_Value = OPcode + Reg_Memory[Instruction_Value[j+1]] + format(Var_memory_A, '08b')
         
        elif TYPE =="E":
            for j in range(0, len(Instruction_Value),1):
                if(Instruction_Value[j] in E_TYPE.keys()):
                    K=Instruction_Value[j]
                    break
                else: 
                    pass
            OPcode=E_TYPE[K]
            Unused_Bit="000"            
            label=Instruction_Value[1]
            Memory_INDEX= str(format(Label_Address[label], '08b'))
            Encoding_Value=OPcode+Unused_Bit+Memory_INDEX
            
        
        
        print(Encoding_Value)
    

if E_Flag_2==False:
    for Instruction_Value in Updated_List_of_Data:
        type=FInd_Type1(Instruction_Value)
        PRINT(Instruction_Value,type) 
