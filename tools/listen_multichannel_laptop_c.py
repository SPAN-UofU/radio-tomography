from serial import *
from time import *
from datetime import *
import sys

#1st input parameter: filename.txt
filename = str(sys.argv[1])
#2nd input parameter: MAX_NUM_NODES (as defined in spin_multichannel.h)
num_nodes = int(sys.argv[2])
#3rd input parameter: /dev/tty.usbmodem001
serial_line = str(sys.argv[3])
#4th sample count: 10
#samples = int(sys.argv[4])

channels_list = [11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
channels_list_set = set(channels_list)

string_length = num_nodes + 7

preamble = 0xDEAD
suffix = 0xBEEF

fout = open(filename,'w')

#MAC MACHINES
#ser = Serial(s3r1al,38400)

#LINUX MACHINES
#serial_line = '/dev/ttyACM0'
print "%s" % (str(serial_line))
ser = Serial(serial_line,38400)

#WINDOWS MACHINES
#ser = Serial('COM5',38400)

rsamples = 0

currentLine = []

def rssi2dbm(rssi):
    #"""Convert rssi register values from hexidecimal 2's complement to dBm."""
    offset = 0
    i = int(rssi,16)
    result = (i + 2**7) % 2**8 - 2**7 + offset
    return result

start = datetime.now()
while(1):
    #while rsamples < samples:
    tempInt = ser.read().encode('hex')
    currentLine.append(tempInt)

    #print len(currentLine)
    #print "%s" % (str(currentLine))

    if currentLine[-2:] == ['ef','be']:
        if len(currentLine) != string_length:
            print 'packet corrupted - wrong string length'
            #print len(currentLine)
            #print "%s" % (str(currentLine))
            del currentLine[:]
            continue

        #dataStr =  ",".join([str(rssi2dbm(A)) for A in currentLine[:-2]])
        TX_id_number = rssi2dbm(currentLine[2])
        #print TX_id_number

        channel_number = rssi2dbm(currentLine[string_length-4])
        #print channel_number
        channel_num = [channel_number]
        #print channel_num
        channel_number_set = set(channel_num)

        #print channel_number_set
        #print channels_list_set

        if (TX_id_number < 1):
            print 'packet corrupted - negative TX_id_number'
            del currentLine[:]
            continue
        if (TX_id_number > num_nodes):
            print 'packet corrupted - too big TX_id_number'
            del currentLine[:]
            continue
        a = channels_list_set.intersection(channel_number_set)
        if (not a):
            print 'packet corrupted - wrong channel number'
            del currentLine[:]
            continue

        #dataStr = str(int(currentLine[0],16)) + " " + str(int(currentLine[1],16))
        #for i in range(2,2+num_nodes+3):
            #dataStr +=  " " + str((currentLine[i]))
            #dataStr +=  " " + str((rssi2dbm(currentLine[i])))
            #dataStr +=  " ".join([str(rssi2dbm(A)) for A in currentLine[:-2]])

        dataStr = str(int(currentLine[1],16)) + " " + str(int(currentLine[0],16))
        for i in range(2,2+num_nodes+3):
            dataStr +=  " " + str((currentLine[i]))
        s = dataStr

        now = datetime.now()
        elapsed = now - start
        s = s + ' ' + str(elapsed.total_seconds())
        s = s + ' ' + str(now) + '\n'

        print "Slot# " + currentLine[-3] + \
                " TX " + currentLine[2] + \
                " Chn " + currentLine[-4]
        #print s

        fout.write(s)
        currentLine = []
        rsamples += 1

#fout.close()

