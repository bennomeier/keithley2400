#this script is to control the keithley via serial interface. To set an output voltage we have to run
# *RST
# :SOUR:FUNC:VOLT
# :SOUR:VOLT 1.25
# :OUTPUT ON

#This would have set the voltage to 1.25 Volt. To change the voltage we need to first switch off the output, i.e.
# :OUTP OFF
# :SOUR:VOLT 1.35
# :OUTPUT ON

#These instructions are taken from the sample script in the manual on p. 245 or 12-23. Use a carriage return and rate 9600. 
import serial
import time

class Keithley2400(object):
    """This class represents a Keithley 4 wire resistance / source meter"""

    def __init__(self, port=9):
        #port 9 is for the USB dongle.
        self.port = port
        self.ser =serial.Serial(self.port, baudrate=9600, stopbits=serial.STOPBITS_ONE,timeout=1)
        time.sleep(2)

    def close(self):
        self.ser.close()

    def sendValue(self,string):
        self.ser.write(string+"\r")
        time.sleep(0.2)

    def readValue(self, string):
        self.sendValue(string)
        answer = self.ser.readline()
        time.sleep(0.2)
        return answer
        
    def setComplianceCurrent(self, curr = 10):
        self.sendValue(":SENS:CURR:PROT " + str(curr) + "E-3")


    def reset(self):
        self.sendValue("*RST")
        time.sleep(1)

    def setSourceFunc(self, func="VOLT"):
        """set the source function. can be VOLT for a voltage source or CURR for a current source"""
        self.sendValue(":SOUR:FUNC "+func)

    def setVoltage(self, voltage):
        """set the voltage. voltage is a numerical value"""
        self.sendValue(":SOUR:VOLT " + str(voltage))

    def outputOn(self):
        self.sendValue(":OUTPUT ON")

    def outputOff(self):
        self.sendValue(":OUTP OFF")

    def switchVoltage(self, voltage):
        """switches the output off, changes the voltage and switches it on again"""
        self.outputOff()
        self.setVoltage(voltage)
        self.outputOn()

    def read(self):
        self.outputOn()
        val = float(self.readValue(":READ?").strip())
        self.outputOff()
        return val
        
    def setupVoltageMeasurement(self):
        """Function to prepare Keithley vor Voltage measurement.
        cf. page 3-21 in accompanying manual.
        Use this to set Keithley up, followed by calls to read to get the values."""
        #
        self.reset()
        self.setSourceFunc(func="CURR")
        self.sendValue(":SOUR:CURR:MODE FIXED")
        self.sendValue(":SENS:FUNC \"VOLT\"")
        self.sendValue(":SOUR:CURR:RANG MIN")
        self.sendValue(":SOUR:CURR:LEV 0")
        self.sendValue(":SENS:VOLT:PROT 25")
        self.sendValue(":SENS:VOLT:RANG 20")
        self.sendValue(":FORM:ELEM VOLT")

        

        
if __name__ == "__main__":
    keithley = Keithley2400(port = "/dev/cu.usbserial-FTFC37N3")
    keithley.reset()
    keithley.setSourceFunc(func="VOLT")
    keithley.setVoltage(1.2)
    keithley.switchVoltage(1.3)
    keithley.close()
