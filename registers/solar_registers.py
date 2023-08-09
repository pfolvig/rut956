from collections import namedtuple
from decode import *

READ_INPUT_REGISTERS = 4
READ_HOLDING_REGISTERS = 3
READ_COILS=1

Block = namedtuple('Block',['function','start','length','registers'])
Register = namedtuple('Register',['name', 'decode','len', 'extra'])

nop = Register('nop',None,None,None)
offset = 0   # Address offset to apply
registers = [

    Block(READ_INPUT_REGISTERS,0x3100 ,7,{  # input_A
        0x3100:Register('SOL_INPV',r_integer,1,2),    #(V, 100)
        0x3101:Register('SOL_INPA',r_integer,1,2),    #(A, 100)
        0x3102:Register('SOL_INPW',r_integer,1,2),    #(A, 100)
        0x3103:nop,
        0x3104:Register('SOL_BATV',r_integer,1,2),    #(V, 100)
        0x3105:Register('SOL_BATA',r_integer,1,2),    #(A, 100)
        0x3106:Register('SOL_BATW',r_integer,1,2),    #(A, 100)
    }),
    Block(READ_INPUT_REGISTERS,0x310C,3,{   
        0x310C:Register('SOL_OUTV',r_integer,1,2),    #(V, 100)
        0x310D:Register('SOL_OUTA',r_integer,1,2),    #(A, 100)
        0x310E:Register('SOL_OUTW',r_integer,1,2),    #(A, 100)
       
        }
    ),
    
    Block(READ_INPUT_REGISTERS,0x311A,1,{
        0x311A:Register('SOL_SOC',r_integer,1,2)
        }
    ),
   
]
