<html> 
	<link href="mailStyles.css"
	rel="stylesheet" type="text/css">
</html>

<?php
// declarations
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "test_db";

// Creating the connection
if (!mysql_connect($servername, $username, $password)) 
	die('Could not connect: ' . mysql_error());
if (!mysql_select_db($dbname)) 
	die('Could not select database');

// MySQL query
// Taking last entry sorted by date and time
$result = mysql_query("SELECT * FROM ir_data ORDER BY date DESC, time DESC LIMIT 1");
if (!$result) {
	die("MYSQL query failed");
}

$fields_num = mysql_num_fields($result);

// Creating array with result of query
$array = mysql_fetch_array($result);

// If there's mail
if ($array[state] == "True") {
	echo "<img src='Mail.jpg' alt='Mail' style='width:425px;height:425px'>";
	echo "<h1>You've got mail! It arrived at $array[time] on $array[date].</h1>";
}

// If there's no mail
else if ($array[state] == "False"){
	echo "<img src='NoMail.jpg' alt='No Mail' style='width:425px;height:425px'>";
	echo "<h1>No mail as of $array[time] on $array[date]</h1>.";
}

// If the flag's up
else if ($array[state] == "Flag"){
	echo "<img src='MailAndFlag.jpg' alt='Flag' style='width:425px;height:425px'>";
	echo "<h1>The mail is waiting to be picked up as of $array[time] on $array[date].</h1>";
}

// Freeing data
mysql_free_result($result);
mysql_close($conn);
?>