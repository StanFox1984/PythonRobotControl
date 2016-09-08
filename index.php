<html>
 <head>
  <title>Тестируем PHP</title>
 </head>
 <body>
 <?php
/* Скрипт показывает клиентов, которые яблоки любят больше чем апельсины */

/* Переменные для соединения с базой данных */
$hostname = "127.3.113.130";
$username = "admin";
$password = "123456";
$dbName = "stanfoxarduino";

$command = escapeshellcmd('./python_functor2.py');
$output = shell_exec($command);

echo "OUT: $output";

/* Таблица MySQL, в которой хранятся данные */
$userstable = "arduino_cmds";

/* создать соединение */
mysql_connect($hostname,$username,$password) OR DIE("Не могу создать соединение ");
/* выбрать базу данных. Если произойдет ошибка - вывести ее */
mysql_select_db($dbName) or die(mysql_error()); 

$run_cmd = 0;
$query = "SELECT * FROM $userstable";
/* составить запрос, который выберет всех клиентов - яблочников */
if (isset($_GET['add']))
{
  $command = $_GET['command'];
  $reply = $_GET['reply'];
  $query = "INSERT INTO arduino_cmds "."VALUES(NULL,'$command','$reply')";
  $run_cmd = 1;
}
if (isset($_GET['clear']))
{
  $query = "DELETE FROM arduino_cmds";
  $run_cmd = 1;
}


if($run_cmd == 1)
{
  /* Выполнить запрос. Если произойдет ошибка - вывести ее. */
  $res = mysql_query($query) or die(mysql_error());
}

$query = "SELECT * FROM $userstable";

/* Выполнить запрос. Если произойдет ошибка - вывести ее. */
$res = mysql_query($query) or die(mysql_error());

/* Как много нашлось таких */
$number = mysql_num_rows($res);

/* Напечатать всех в красивом виде*/
if ($number == 0) {
  echo "<CENTER><P></CENTER>";
} else {
  while ($row=mysql_fetch_array($res)) {
    echo "\"id\":\"".$row['id']."\"\"command\":\"".$row['command']."\"\"reply\":\"".$row['reply']."\"";
    echo "<BR><BR>";
  }
  echo "</CENTER>";
} 
 ?>
 </body>
</html>
