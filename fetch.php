<?php


$host = $_GET['argument1']; 
$user = $_GET['argument2']; 
$pass = $_GET['argument3'];; 



$r = mysql_connect($host, $user, $pass);

if (!$r) {
    echo "Could not connect to server\n";
    trigger_error(mysql_error(), E_USER_ERROR);
} else {
    echo "Connection established\n"; 
}

$r = mysql_select_db('testst1984');

if( !$r)
{
  echo "could not select database";
}
else
{
  echo "database selected";
}


$query = "SELECT id, name from test";

$rs = mysql_query($query);

if (!$rs) {
    echo "Could not execute query: $query\n";
    trigger_error(mysql_error(), E_USER_ERROR);
} else {
    echo "Query: $query executed\n"; 
}

$row = mysql_fetch_row($rs);

echo "$row[0] $row[1]\n";

mysql_close();

?>
<?php

