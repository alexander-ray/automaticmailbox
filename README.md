# automaticmailbox
	A way to eliminate the long, dangerous trek out to the mailbox to see if you have mail. Using Arduino and Raspberry Pi.

	The basic premise of my project is that it is a full journey up a stack of technologies—from the circuits to the webpage. This chart shows the progression of information from the mailbox to the webpage.
	The C code uploaded to the Arduino constantly loops and reads information from the IR emitter/receiver and the accelerometer. This information is then broadcast out of whichever serial port the Arduino is connected to. 
	The python program has two major functions: using the information from the serial port, it must decide the “state” of the mailbox and then it must transmit this information. Once it goes through the logic to decide what “state” the mailbox is in, the program will use the mysql.connector module to query the MySQL database on the server. If the state is a positive “There is mail in the mailbox!” the program will use the smtplib module to send an email informing the mail recipient that they do have mail.
	The MySQL database is set up on a MAMP (Mac Apache MySQL PHP) server. The database holds a table with three fields: state, date, and time. The state is “True” (there is mail), “False” (no mail), or “Flag” (the mail is waiting to be picked up).
	Finally, the PHP script connects to the database and reads the latest entry (sorted by date and time). It then decides what page to show depending on the state field.

