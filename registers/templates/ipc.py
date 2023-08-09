
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
           6354:Register('alarms',number_int,1,None),
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
    Block(READ_HOLDING_REGISTERS,225,1,{
        225:Register('flow',number_int,2,1),
        }
    ),
    Block(READ_HOLDING_REGISTERS,143,1,{
        143:Register('level',number_int,2,1),
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
        62:Register('bin',unpack_bits,1,{0:'Emergency stop',
              1:'Flow Switch',   
              2:'RemoteStart',   
              3:'RemoteStop',    
              4:'EStop',}),
        63:Register('bout',unpack_bits,1,{0:'Starter',
              1:'Fuel solenoid', 
              2:'Prestart',      
              3 :'BI5 stat',    
              4:'Horn',    })    ,
        64:nop,
        65:nop,
        66:nop,
        67:nop,
        68:nop,
        69:nop,
        70:nop,
        71:nop,
        72:Register('state', lookup,1,
            { 23:'Init',          
            24:'Not ready',     
            25 :'Prestart',      
            26 :'Cranking',      
            27 :'Pause',         
            28  :'Starting',      
            29  :'Running',       
            30  :'Loaded',        
            31  :'Stop',          
            32  :'Shutdown',      
            33  :'Ready',         
            34  :'Cooling',       
            35  :'EmergMan',      
            36  :'MainsOper',     
            37  :'MainsFlt',      
            38  :'ValidFlt',      
            39  :'IslOper',       
            40  :'MainsRet',      
            41  :'Brks Off',      
            42  :'No Timer',      
            43  :'MCB close',     
            44  :'RetTransf',     
            45  :'FwRet Brk',     
            46  :'Idle Run',      
            47  :'MinStabTO',     
            48  :'MaxStabTO',     
            49  :'AfterCool',     
            50  :'GCB open',      
            51  :'StopValve',     
            52  :'1Ph',         
            53  :'3PD',         
            54  :'3PY',         
            55  :'Run Timer',     
            56  :'SdVentil',      
            57  :'Ventil',        
            58  :'Idle',  }        ),
            
       
        }),  #Alarms and Status
]