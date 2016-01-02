<html>
 <head>
  <title>Test PHP</title>
 </head>
 <body>
<br>
 <?php
/* Скрипт показывает клиентов, которые яблоки любят больше чем апельсины */

/* Переменные для соединения с базой данных */
$hostname = "127.6.216.130";
$username = "admin";
$password = "123456";
$dbName = "testst1984";

/* Таблица MySQL, в которой хранятся данные */
$userstable = "message_hub";

/* создать соединение */
mysql_connect($hostname,$username,$password) OR DIE("No connection ");
/* выбрать базу данных. Если произойдет ошибка - вывести ее */
mysql_select_db($dbName) or die(mysql_error()); 

$run_cmd = 0;
$show_cmd = 0;
$start_id = 0;
$num_ids = 0;
$query = "SELECT * FROM $userstable";

if (isset($_GET['self']))
{
  $self = $_GET['self'];
}

if (isset($_GET['add']))
{
  $sender = $_GET['sender'];
  $receiver = $_GET['receiver'];
  $custom = $_GET['custom'];
  $data = $_GET['data'];
  $query = "INSERT INTO message_hub "."VALUES(NULL,'$sender','$receiver','$data',NULL,'$custom')";
  $run_cmd = 1;
}
if (isset($_GET['clear']))
{
  if(!isset($_GET['self']))
  {
    $query = "DELETE FROM message_hub";
  }
  else
  {
    $query = "DELETE FROM message_hub WHERE receiver='$self'";
  }
  $run_cmd = 1;
}
if (isset($_GET['show']))
{
  if(isset($_GET['start_id']))
  {
    $start_id = $_GET['start_id'];
  }
  if(isset($_GET['num_ids']))
  {
    $num_ids = $_GET['num_ids'];
  }
  $show_cmd = 1;
}

if($run_cmd == 1)
{
  /* Выполнить запрос. Если произойдет ошибка - вывести ее. */
  $res = mysql_query($query) or die(mysql_error());
}
if(($show_cmd == 1))
{
  if(!isset($_GET['self']))
  {
    if($start_id != 0)
    {
      $query = "SELECT * FROM $userstable WHERE msg_id >= $start_id";
    }
    else
    {
      $query = "SELECT * FROM $userstable";
    }
  }
  else
  {
    if($start_id != 0)
    {
      $query = "SELECT * FROM $userstable WHERE msg_id >= $start_id AND receiver='$self'";
    }
    else
    {
      $query = "SELECT * FROM $userstable WHERE receiver='$self'";
    }
  }
  $res = mysql_query($query) or die(mysql_error());
  /* Как много нашлось таких */
  $number = mysql_num_rows($res);
  if($num_ids == 0)
  {
    $num_ids = $number;
  }
  $n = 0;
  /* Напечатать всех в красивом виде*/
  if ($number == 0) {
    echo "<CENTER><P></CENTER>";
  } else {
    echo "{ ";
    while ($row=mysql_fetch_array($res)) {
        if($n >= $num_ids)
          break;
      $rt = $row['data'];
      $strings = explode("DELIM", $row['data']);
      foreach( $strings as $string)
      {
        //echo $strings[0]
        if((($n+1) < $number) and (($n+1) < $num_ids))
            echo "{ \"msg_id\" : \"".$row['msg_id']."\", \"sender\" : \"".$row['sender']."\", \"receiver\" : \"".$row['receiver']."\", \"data\" : \"".$string."\", \"time\" : \"".$row['time']."\", \"custom\" : \"".$row['custom']."\" },";
        else
            echo "{ \"msg_id\" : \"".$row['msg_id']."\", \"sender\" : \"".$row['sender']."\", \"receiver\" : \"".$row['receiver']."\", \"data\" : \"".$string."\", \"time\" : \"".$row['time']."\", \"custom\" : \"".$row['custom']."\" } }";
        echo "<BR><BR>";
      }
      $n=$n + 1;
    }
    echo "</CENTER>";
  }
} 
 ?>
 </body>
</html>
