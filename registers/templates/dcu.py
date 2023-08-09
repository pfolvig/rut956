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
    Block(READ_HOLDING_REGISTERS,11,6,{
        11:Register('bvolt',number_dec,2,1),
        12:nop,
        13:Register('volute',number_int,2,0),
        14:Register('suction',number_dec,2,1),
        15:Register('discharge',number_dec,2,1),
        16:Register('level',number_int,2,0),
    }),
    Block(READ_HOLDING_REGISTERS,159,1,{
        159:Register('rpm',number_int,2,0),
    }),
    Block(READ_HOLDING_REGISTERS,168,4,{
        168:Register('oil_pressure',number_dec,2,2),
        169:Register('oil_temp',number_int,2,0),
        170:Register('coolant_temp',number_int,2,0),
        171:Register('fuel',number_int,2,0),
    }),
   Block(READ_HOLDING_REGISTERS,3001,1,{
        3001:Register('requested_level',number_int,2,0),
    }),
    Block(READ_HOLDING_REGISTERS,3007,2,{
        3007:Register('CMP_on',number_int,2,0),
        3008:Register('CMP_off',number_int,2,0),
    }),
    Block(READ_HOLDING_REGISTERS,3034,2,{
        3034:Register('runhrs',r_unsigned32,2,0),    
    }),
    Block(READ_HOLDING_REGISTERS,3059,1,{
        3059:Register('mode',lookup,1,{
            0:'OFF',
            1:'RUN',
        }),
    }),
    Block(READ_HOLDING_REGISTERS,114,1,{
        114:Register('state',lookup,1,{
            0:'Init',
            1:'Ready',
            2:'NotReady',
            3:'Prestart',
            4:'Cranking',
            5:'Pause',
            6:'Starting',
            7:'Running',
            8:'Loaded',
            9:'Unloading',
            10:'Cooling',
            11:'Stop',
            12:'Shutdown',
            13:'Ventil',
            14:'EmergMan',
            15:'Cooldown',
            16:'LoadShar',
        }),      
    }),
    Block(READ_HOLDING_REGISTERS,79,1,{
        79:Register('lbout',unpack_bits,1,{
            1:'Horn',
            2:'Alarm',
            3:'Common Alarm',
            4:'Common Wrn',
            5:'Common Sd',
            6:'Common Fls',
            7:'OFF Mode',
            8:'RUN Mode',
            9:'not_used_1',
            10:'not_used_2',
            11:'Not In LOC',
            12:'In LOC',
            13:'CPU Ready',
            14:'not_used_3',
            15:'Idle/Nominal',
        }),
    }),

]