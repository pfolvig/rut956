
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
    
    Block(READ_HOLDING_REGISTERS,1,3,{
        1:Register('voltage_L1_N',number_dec,1,1),
        2:Register('voltage_L2_N',number_dec,1,1),
        3:Register('voltage_L3_N',number_dec,1,1),
    }),
    Block(READ_HOLDING_REGISTERS,5,3,{
        5:Register('voltage_L1_L2',number_dec,1,1),
        6:Register('voltage_L2_L3',number_dec,1,1),
        7:Register('voltage_L3_L1',number_dec,1,1),
    }),
    Block(READ_HOLDING_REGISTERS,8,5,{
        8:Register('current_L1',number_int,1,1),
        9:Register('current_L2',number_int,1,1),
        10:Register('current_L3',number_int,1,1),
        11:Register('rpm',number_int,1,1),
        12:Register('freq',number_dec,1,1),
     }), 

     Block(READ_HOLDING_REGISTERS,14,5,{    
        14:Register('realpwr',number_int,1,2),
        15:Register('gen_kw_L1',number_int,1,2),
        16:Register('gen_kw_L2',number_int,1,2),
        17:Register('gen_kw_L3',number_int,1,2),
        18:Register('nominal_kva',number_int,1,2),
    }),
        #19:Register('gen_kvar',number_dec,2), 
        #~ 20:Register('gen_kvar_L1',number_dec,2),
        #~ 21:Register('gen_kvar_L2',number_dec,2),
        #~ 22:Register('gen_kvar_L3',number_dec,2),
        #~ 23:Register('pwrfactor',number_dec,2),
        #~ 24:Register('gen_pf_L1',number_dec,2),
        #~ 25:Register('gen_pf_L2',number_dec,2),
        #~ 26:Register('gen_pf_L3',number_dec,2),
    
        #~ 28:nop,
        #~ 29:nop,
        #~ 30:nop,
        #~ 31:nop,
        #~ 32:Register('apparpwr',number_dec,0),
        #~ 33:Register('gen_kva_L1',number_dec,0),
        #~ 34:Register('gen_kva_L2',number_dec,0),
        #~ 35:Register('gen_kva_L3',number_dec,0),
        
   
    Block(READ_HOLDING_REGISTERS,51,1,{
        51:Register('bvolt',number_dec,1,1),
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
    Block(READ_HOLDING_REGISTERS,161,16,{
        161:Register('airgate',r_string0,16,16),
        }
    ),
     Block(READ_HOLDING_REGISTERS,3001,2,{
       3001:Register('runhrs',r_unsigned32,2,1),
        }
    ),
   
    Block(READ_HOLDING_REGISTERS,62,10,{
       
        62:Register('bin',unpack_bits,1,{
              0:'Emergency Stop',
              1:'S-S Fault',     
              2:'RCD Fault',     
              3:'ECR Fault',     
              4:'Flow Fault',    
              5:'Rem Start-Stop',
              6:'Not Used',      
              }),
        63:Register('bout',unpack_bits,1,{
            0:'KM1',           
            1:'Ready',             
            2:'Running',           
            3:'AL Common Sd',      
            4:'RemoteControl1',    
            5:'Not used',          
            6:'Alarm',            
              })    ,
        64:nop,
        65:nop,
        66:nop,
        67:nop,
        68:nop,
        69:nop,
        70:nop,
        71:Register('state', lookup, 1,{ 
            16:'Init',          
            17:'Not ready',             
            18:'Brake Release',         
            19:'Starting',              
            20:'Pause',                 
            21:'Starting',              
            22:'Running',               
            23:'Running',               
            24:'Stop',                  
            25:'Shutdown',              
            26:'Ready',                 
            27:'Cooling',               
            28:'EmergMan',              
            29:'MainsOper',             
            30:'MainsFlt',              
            31:'MainsFlt',              
            32:'IslOper',               
            33:'MainsRet',              
            34:'Brks Off',              
            35:'No Timer',              
            36:'MCB Close',             
            37:'ReturnDel',             
            38:'Trans Del',             
            39:'Starting',              
            40:'MinStabTO',            
            41:'MaxStabTO',             
            42:'AfterCool',             
            43:'GCB Open',              
            44:'StopValve',             
            45:'Start Del',             
            46:'1Ph',                 
            47:'3PD',                 
            48:'3PY',                 
            49:'StartNextMotor',        
            }        
        ),
    })
     
        
]