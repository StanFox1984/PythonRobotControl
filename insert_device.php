<?php


$host = "127.6.216.130"; 
$user = "testtest"; 
$pass = "pass";
$device_id  = $_GET['device_id'];
$message = $_GET['message'];




$r = mysql_connect($host, $user, $pass);

if (!$r) {
    echo "Could not connect to server\n";
    trigger_error(mysql_error(), E_USER_ERROR);
} else {
    //echo "Connection established\n"; 
}

$r = mysql_select_db('testst1984');

if( !$r)
{
  echo "could not select database";
}
else
{
  //echo "database selected";
}

if(isset($_GET("message")))
{
$s = addslashes($devname);
$query = "INSERT INTO Devices VALUES (0,0,$message,$device_id);";

$rs = mysql_query($query);

if (!$rs) {
    echo "Could not execute query: $query\n";
    trigger_error(mysql_error(), E_USER_ERROR);
} else {
    //echo "Query: $query executed\n"; 
}
}

$query = "SELECT id, time, message, device_id from Devices";

$rs = mysql_query($query);

if (!$rs) {
    echo "Could not execute query: $query\n";
        trigger_error(mysql_error(), E_USER_ERROR);
    } else {
            //echo "Query: $query executed\n"; 
            }
            
echo "{ records : [ \r\n";
$numresults = mysql_num_rows($rs);
$counter = 0;
while( $row = mysql_fetch_array($rs) )
{
    $s = stripslashes($row[3]);
    echo "{ id:$row[0], time:$row[1], message:$row[2], device_id:$row[3] }";
    ++$counter;
    if( $counter < $numresults )
    {
        echo ",\r\n";
    }
    echo "\r\n";
}
                                                
echo "] }\r\n";
                                                
//$row = mysql_fetch_row($rs);

//echo "$row[0] $row[1]\n";

mysql_close();

?>
<?php

