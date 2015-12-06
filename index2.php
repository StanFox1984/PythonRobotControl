<html>
 <head>
  <title>Тестируем PHP</title>
 </head>
 <body>
<input type="submit" class="button" name="LeftMotorOn" value="LeftMotorOn" style="height:150px; width:150px"  onClick='location.href="?add=1&command=LeftMotorOn&reply="' />
<br>
<input type="submit" class="button" name="RightMotorOn" value="RightMotorOn" style="height:150px; width:150px" onClick='location.href="?add=1&command=RightMotorOn&reply="' />
<br>
<input type="submit" class="button" name="LeftMotorOff" value="LeftMotorOff" style="height:150px; width:150px" onClick='location.href="?add=1&command=LeftMotorOff&reply="' />
<br>
<input type="submit" class="button" name="RightMotorOff" value="RightMotorOff" style="height:150px; width:150px" onClick='location.href="?add=1&command=RightMotorOff&reply="' />
<br>
<input type="submit" class="button" name="Beep" value="Beep" style="height:150px; width:150px"  onClick='location.href="?add=1&command=Beep&reply="' />
<br>
<input type="submit" class="button" name="SelfControl" value="SelfControl" style="height:150px; width:150px"  onClick='location.href="?add=1&command=SelfControl&reply="' />
<br>
<input type="submit" class="button" name="Sensor0" value="Sensor0" style="height:150px; width:150px"  onClick='location.href="?add=1&command=Sensor0&reply="' />
<br>
<input type="submit" class="button" name="Sensor1" value="Sensor1" style="height:150px; width:150px"  onClick='location.href="?add=1&command=Sensor1&reply="' />
<br>
<input type="submit" class="button" name="Clear" value="Clear" style="height:150px; width:150px"  onClick='location.href="?clear=1"' />
<br>
 <?php
/* Скрипт показывает клиентов, которые яблоки любят больше чем апельсины */

/* Переменные для соединения с базой данных */
$hostname = "127.3.113.130";
$username = "admin";
$password = "123456";
$dbName = "stanfoxarduino";

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
