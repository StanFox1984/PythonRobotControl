<?php


$host = $_GET['argument1']; 
$user = $_GET['argument2']; 
$pass = $_GET['argument3'];; 



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


$query = "SELECT id, latitude, longitude, devname from bluetoothmap";

$rs = mysql_query($query);

if (!$rs) {
    echo "Could not execute query: $query\n";
    trigger_error(mysql_error(), E_USER_ERROR);
} else {
    //echo "Query: $query executed\n"; 
}

echo "{ positions : [ \n";
$numresults = mysql_num_rows($rs);
$counter = 0;
while( $row = mysql_fetch_array($rs) )
{
    $s = stripslashes($row[3]);
    echo "{ id:$row[0], latitude:$row[1], longitude:$row[2], devname:\"$s\" }";
    ++$counter;
    if( $counter < $numresults )
    {
        echo ",";
    }
    echo "\n";
}

echo "] }\n";

mysql_close();

?>
<?php

