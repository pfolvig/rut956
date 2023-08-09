from collections import namedtuple
from decode import *

READ_INPUT_REGISTERS = 4
READ_HOLDING_REGISTERS = 3
READ_COILS=1


Block = namedtuple('Block',['function','start','length','registers'])
Register = namedtuple('Register',['name', 'decode', 'len','extra'])

nop = Register('nop',None,1,None)

offset = 1 # Address offset to apply COMAP docs +1 more than actual
registers = [

    Block(READ_HOLDING_REGISTERS,6354 ,1,{  # Alarm Records
        6354:Register('alarms',number_int,1,0),
        }
    ), 
    Block(READ_HOLDING_REGISTERS,11,1,{
        11:Register('rpm',number_int,1,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,164,16,{
        164:Register('airgate',r_string0,16,16),
        }
    ),
    Block(READ_HOLDING_REGISTERS,154,3,{
        154:Register('suction',number_int,2,1),
        155:Register('discharge',number_int,2,1),
        156:Register('flow',number_int,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,143,4,{
	143:Register('volute',number_int,2,1),
	144:Register('fuel',number_int,2,1),
        145:Register('level',number_int,2,1),
	146:Register('extFuel',number_int,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,193,6,{
	193:Register('fuel_rate',number_int,2,1),
	194:Register('coolant_temp',number_int,2,1),
        195:nop,
	196:Register('oil_pressure',number_int,2,2),
	197:Register('boost_pressure',number_int,2,2),
	198:Register('load',number_int,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,3198,2,{
        3198:Register('CMP_off',number_int,2,1),
	3199:Register('CMP_on',number_int,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,3001,2,{
    3001:Register('runhrs',r_unsigned32,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,80,1,{
        80:Register('mode',lookup,1,{
          0: "OFF",           
          1 :"MAN",           
          2 :"AUT",
          }),
        }
    ),
    Block(READ_HOLDING_REGISTERS,51,22,{
        51:Register('bvolt',number_dec,1,1),
        52:Register('cputemp',number_dec,1,1),
        53:nop,
        54:nop,
        55:nop,
        56:nop,
        57:nop,
        58:nop,
        59:nop,
        60:nop,
        61:nop,
        62:nop,
        63:nop,
        64:nop,
        65:nop,
        66:nop,
        67:nop,
        68:nop,
        69:nop,
        70:nop,
        71:nop,
        72:Register('state', lookup,1,
            { 19:'Init',          
            20:'Not ready',     
            21:'Prestart',      
            22:'Cranking',      
            23:'Pause',         
            24:'Starting',      
            25:'Running',       
            26:'Loaded',        
            27:'Stop',          
            28:'Shutdown',      
            29:'Ready',         
            30:'Cooling',       
            31:'EmergMan',      
            32:'MainsOper',     
            33:'MainsFlt',      
            34:'ValidFlt',      
            35:'IslOper',       
            36:'MainsRet',      
            37:'Brks Off',      
            38:'No Timer',      
            39:'MCB close',     
            40:'RetTransf',     
            41:'FwRet Brk',     
            42:'Idle Run',      
            43:'MinStabTO',     
            44:'MaxStabTO',     
            45:'AfterCool',     
            46:'GCB open',      
            47:'StopValve',     
            48:'1Ph',         
            49:'3PD',         
            50:'3PY',         
            51:'Run Timer',     
            52:'SdVentil',      
            53:'Ventil',        
            54:'Idle',
            }),
        }),  #Alarms and Status
]