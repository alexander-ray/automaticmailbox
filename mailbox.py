import serial
import smtplib
import mysql.connector
import time
from array import array

# Function to send email
def email(orig, to, password, text):
	
	# setting variables
	receiver = to
	gmail_user = orig
	gmail_pwd = password
	
	# setting up smtplib
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	
	# specifying header text
	header = 'To:' + receiver + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Python Project \n'
	
	# Indicate email has been sent
	print header
	msg = header + text
	
	# Send email and end program
	smtpserver.sendmail(gmail_user, receiver, msg)
	print 'done!'
	smtpserver.close()
	return

# Query database
def database(userTemp, passwordTemp, hostTemp, portTemp, databaseTemp, state, date, time):
	
	# Connect
	cnx = mysql.connector.connect(user=userTemp,
							  	  password=passwordTemp,
							      host=hostTemp,
                                  port=portTemp,
                                  database=databaseTemp)
                              
	cursor = cnx.cursor()
	
	query = "INSERT INTO mailbox_state (state, date, time) VALUES (%s, %s, %s)" 
	data_sensor = (state, date, time)
	
	cursor.execute(query, data_sensor)
	cnx.commit()
	
	# Close
	cursor.close()
	cnx.close()
	
# Main method
def main():

	# Initializations
	# Counters ensure there are only queries to the database with changes of state,
	# not all the time
	flagCounter = 0
	counter = 0
	accNumCurrent = 0

	# Find accurate initial accNumCurrent--helps eliminate early false readings
    x = 0
	while x < 4:
		s = serial.Serial(port="/dev/ttyACM0", baudrate = 9600)
		numbers = s.readline().split()
		accNumCurrent = int(numbers[0])
		x += 1	
	
	# Set previous to current
	accNumPrevious = accNumCurrent 
	irNum = 0
	
	# Loop forever
	while 1:
		
		# Connect to serial port
		s = serial.Serial(port="/dev/ttyACM0", baudrate = 9600)
		
		# Make list with accelerometer value and IR value
		# Data is sent as "accelerometerInfo  IRinfo", split function gets those individually
		numbers = s.readline().split()
		
		# Set variables
		accNumCurrent = int(numbers[0])
		irNum = int(numbers[1])
		
		# Find the difference between the two latest accelerometer readings
		difference = accNumCurrent-accNumPrevious
		print "The accelerometer difference is: ", difference
                print "The IR value is: ", irNum
                
        # If difference > 300, flag was lifted up
		if difference > 300:
			# Time function sends current date and time with time module
			database("mailbox", "mailbox", "192.168.1.100", 8889, "mailbox", "Flag", time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S %p"))
			# Ensure it won't check for mail if flag is up
			flagCounter = 1
			
		# If difference < 300, flag was lowered
		elif difference < -300:
			# Reset flag counter
			flagCounter = 0
			
			# Report on mail
			if counter == 0:
				email("1alexray@gmail.com", "ejray@raycomm.com", "arduinoProject", "Check the mail, damnit.")
				database("mailbox", "mailbox", "192.168.1.100", 8889, "mailbox", "True", time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S %p"))
				counter = 1
			else:
				if counter == 1:
                    database("mailbox", "mailbox", "192.168.1.100", 8889, "mailbox", "False", time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S %p"))
				counter = 0
		else:
			if flagCounter == 0:
				if irNum < 100:
					if counter == 0:
						email("1alexray@gmail.com", "ejray@raycomm.com", "arduinoProject", "Check the mail, damnit.")
						database("mailbox", "mailbox", "192.168.1.100", 8889, "mailbox", "True", time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S %p"))
						counter = 1
				else:
					if counter == 1:
                        database("mailbox", "mailbox", "192.168.1.100", 8889, "mailbox", "False", time.strftime("%d/%m/%Y"), time.strftime("%I:%M:%S %p"))
					counter = 0
		
		
		
		accNumPrevious = accNumCurrent
		
# Starting program
main()



