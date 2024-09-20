"""
A library to interface Arduino through serial connection
"""
import serial
import time

class Arduino():
    """
    Models an Arduino connection
    """

    def __init__(self, serial_port='COM9', baud_rate=9600,
            read_timeout=5):
        """
        Initializes the serial connection to the Arduino board
        """
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        time.sleep(3)
        print ("Attached to Arduino.")

    def set_pin_mode(self, pin_number, mode):
        """
        Performs a pinMode() operation on pin_number
        Internally sends b'M{mode}{pin_number} where mode could be:
        - I for INPUT
        - O for OUTPUT
        - P for INPUT_PULLUP MO13
        """
        command = (''.join(('M',mode,str(pin_number)))).encode()
        #print 'set_pin_mode =',command,(''.join(('M',mode,str(pin_number))))
        self.conn.write(command)    

    def digital_read(self, pin_number):
        """
        Performs a digital read on pin_number and returns the value (1 or 0)
        Internally sends b'RD{pin_number}' over the serial connection
        """
        command = (''.join(('RD', str(pin_number)))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':') # e.g. D13:1
        if header == ('D'+ str(pin_number)):
            # If header matches
            return int(value)   

    def digital_write(self, pin_number, digital_value):
        """
        Writes the digital_value on pin_number
        Internally sends b'WD{pin_number}:{digital_value}' over the serial
        connection
        """
        command = (''.join(('WD', str(pin_number), ':',
            str(digital_value)))).encode()
        self.conn.write(command) 
   
     
    def analog_read(self, pin_number):
        """
        Performs an analog read on pin_number and returns the value (0 to 1023)
        Internally sends b'RA{pin_number}' over the serial connection
        """
        command = (''.join(('RA', str(pin_number)))).encode()
        print ('analog_read =',command,(''.join(('RA',':',str(pin_number)))))
        self.conn.write(command) 
        line_received = self.conn.readline().decode().strip()
        print ("analog_read_received", line_received)
        header, value = line_received.split(':') # e.g. A4:1
        if header == ('A'+ str(pin_number)):
            # If header matches
            return int(value)

    def analog_write(self, pin_number, analog_value):
        """
        Writes the analog value (0 to 255) on pin_number
        Internally sends b'WA{pin_number}:{analog_value}' over the serial
        connection
        """
        command = (''.join(('WA', str(pin_number), ':',
            str(analog_value)))).encode()
        self.conn.write(command)
        
    def servo_attach(self,servo_number, pin_number):     
        """
        Sets up a servo motor on your Arduino board. You can have up to 5 servo
        motors connected to PWM pins...
        Internally sends b'S{servo_number}{pin_number}' over the serial connection.
        """
        command = (''.join(('S',str(servo_number),str(pin_number)))).encode()
        print ('servo_attach =',command,(''.join(('S',str(servo_number),str(pin_number)))))
        self.conn.write(command)
        time.sleep(1)
        line_received = self.conn.readline().decode().strip()
        print (line_received)

    def servo_read(self,servo_number):
        """
        Performs a servo read on a serevo and returns the value (1 to 180)
        Internally sends b'RS{servo_number}' over the serial connection
        """
        command = (''.join(('RS',':',str(servo_number)))).encode()
        print ('servo_read =',command,(''.join(('RS',':',str(servo_number)))))
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        print ("line_received=",line_received)
        header, value = line_received.split(':') # e.g. D13:1
        if header == ('T'+ str(servo_number)):
            # If header matches
            return int(value)     
        
    def servo_write(self, servo_number,servo_value):
        """
        Writes the angle to a servo
        Internally sends b'SW:{servo_number}' over the serial
        connection
        """
        command = (''.join(('WS',str(servo_number),':',str(servo_value)))).encode()
        print ('servo_write =',command,(''.join(('WS',str(servo_number),":",str(servo_value)))))
        time.sleep(1)
        self.conn.write(command)  
        
    def sevenSeg_setup(self,seg_type, pin_number, pin_number1, pin_number2):     
        """
        Sets up a Seven Segment single bit display on your Arduino board. 
        The first pin_number is the latchPin. The second pin_number1 is the clockPin, 
        and the third pin_number2 is the dataPin.
        The seg_type is 1 for a single bit and 4 for the 4 bit.
        The command sent is b'L{seg-type},{pin_number},{pin_number2},{pin_number3}' over the serial
        """
        command = (''.join(('L',str(seg_type),str(pin_number),',',str(pin_number1),',',str(pin_number2)))).encode()
        print ('sevSeg_setup =',command,(''.join(('L',str(seg_type),str(pin_number),',',str(pin_number1),',',str(pin_number2)))))
        self.conn.write(command)
        time.sleep(1)
        line_received = self.conn.readline().decode().strip()
        print (line_received)  
                   
    def sevenSeg_write(self,seg_pin,seg_byte):
        """
        Writes a byte to a Single bit Seven Segment display. 
        Internally sends b'WL{seg-pin}:{seg_byte}' over the serial
        connection
        """
        command = (''.join(('WL',str(seg_pin),':',str(seg_byte)))).encode()
        print ('sevenSeg_write =',command,(''.join(('WL',str(seg_pin),":",str(seg_byte)))))
        self.conn.write(command)
                       

    def close(self):
        """
        To ensure we are properly closing our connection to the
        Arduino device. 
        """
        self.conn.close()
        print ('Connection to Arduino closed')
        
    