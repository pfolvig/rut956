#!/usr/bin/python3

import os
import time
import serial
import modbus_tk.defines as cst
import sys
import json
import sys
from collections import namedtuple
from decode import *
import argparse

class CompatSerial(serial.Serial):
     def is_open(self):
         return self.isOpen()
     def reset_input_buffer(self):
         return self.flushInput()
     def reset_output_buffer(self):
         return self.flushOutput()

def load_registers(registerfile):
    try:
        module = __import__(registerfile)
        return module.registers, module.offset
    except Exception as e:
        sys.stderr.write(str(e))
        raise

def unpick(registers, block):
    names = block.registers
    payload = {}
    
    for addr, reg in names.items():
        
        try:   
            
            if reg.name == "nop":
                continue

            length = reg.len
            
            if not isinstance(length, int):
                length = 1
            start,finish = (addr-block.start),(addr-block.start)+length
            result = reg.decode(reg.name,registers[start:finish], reg.extra,addr, block, registers)
        except Exception as e:           
            print( reg.name, e)

        if result:
            payload.update(result)

    return payload    

def get_alarms(client, x):
    
    result = []
    
    for i in range(x):
        try:            
            res = client.execute(1,cst.READ_HOLDING_REGISTERS,6668 + (i*25), 25)
            value = struct.pack(">" + "I" * (len(res)), *res).replace(b'\x00',b'').decode("utf-8")
    
            result.append(value)            
        except Exception as e:
            break
            
    return {"alarms":result}


def read(master,registers,offset,unit):
    payload = {}
    # remove errors by default
    # payload = {'errors':[]} 
        
    for reg  in registers:
       
        function = reg.function
        length = reg.length
        if callable(reg.length):
            length = reg.length(payload)
        try:
            res = master.execute(unit, function, reg.start-offset, length)
            payload.update(unpick(res,reg))           
        except Exception as e:
            if "errors" not in payload:
                payload['errors'] = [reg.start,str(e)]
            else:
                payload['errors'].append((reg.start,str(e)))        
    return payload

def publish(topic,payload):
    cmd = "mosquitto_pub -h localhost -m '%s'	-t %s" %  (payload,  args.topic)
    os.system(cmd)

def serial_connection(port):
    from modbus_tk import modbus_rtu
    port = CompatSerial(port=port,baudrate=115200,bytesize=8,parity='N',stopbits=1,timeout=1)
    master =  modbus_rtu.RtuMaster(port)
    return master

def network_connection(ipaddress):
    from modbus_tk import modbus_tcp
    master = modbus_tcp.TcpMaster(ipaddress)
    return master
    
def main(args):
    device = ''
    unit = args.unit
    if args.port and args.port != "/dev/null":
        master = serial_connection(args.port)
        device = args.port
    elif args.network:
        master = network_connection(args.network)
        device = args.network
    else:
        raise ValueError("No connection defined - port %s, network %s" % (args.port, args.network))
    
    registers, offset = load_registers(args.registers)
    
    while True: 
        try:
            master._do_open()
        except Exception as e:
            message = device + " connection failure: " + str(e)
            print(f"{device} connection failure: {e}",file=sys.stderr)
            payload = json.dumps({"error":message})
            publish(args.topic,payload)
            time.sleep(30)

        master.set_timeout(5.0)

        payload = read(master, registers, offset,unit)
        payload['reg_source'] = args.registers
        payload['device'] = device
        
        if payload.get("alarms",0):
            payload.update(get_alarms(master, payload.get("alarms")))
            
        payload = json.dumps({"data":payload})
        #payload = json.dumps(payload)
        publish(args.topic,payload)
        print(args.topic,payload)
        if not hasattr(master,'_serial') :
            master._do_close()
        master._do_close()
        #print('Read successful', file=sys.stderr)
        time.sleep(args.interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Monitor Modbus device")
    parser.add_argument("registers",type=str,help="MODBUS register file")
    parser.add_argument("-t","--topic",dest="topic",type=str,help="Losant topic")
    parser.add_argument("-c","--channel",dest="channel",type=str,help="Redis channel")
    parser.add_argument("-i","--interval",nargs="?",type=int,default=60,dest="interval", help="Time between samples")
    parser.add_argument("-p","--port",nargs="?",type=str,default="/dev/null",dest="port", help="RS485 device name")
    parser.add_argument("-u","--unit",nargs="?",type=int,default=1,dest="unit", help="Modbus Unit Address")
    parser.add_argument("-n","--network",type=str,nargs="?",dest="network",help="IP address")
    parser.add_argument("-o","--offset",type=int,default=0,dest="offset",help="Register Address Offset - should be 1 for comap")
    
    publishers = {}

    args = parser.parse_args()
        
    print(args)
    main(args)
        
            
