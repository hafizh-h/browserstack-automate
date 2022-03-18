<?php
$con = mysqli_connect("localhost","root","","automation_test");
if (mysqli_connect_errno())
{
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$result = mysqli_query($con,"SELECT * FROM device_log");
?>
<!DOCTYPE html>
<head>
   <meta charset="UTF-8">
   <title>Automation Testing Device Log</title>
   <style>
   h2{
      text-align:center; }
   table {
      border-collapse:collapse;
      border-spacing:0;
      font-family:Arial, sans-serif;
      font-size:16px;
      padding-left:300px;
      margin:auto;
      width:100%;}
   table th {
      font-weight:bold;
      padding:10px;
      color:#fff;
      background-color:#2A72BA;
      border-top:1px black solid;
      border-bottom:1px black solid;
      border-right:1px black solid;
      border-left:1px black solid;}
   table td {
      padding:10px;
      border-top:1px black solid;
      border-bottom:1px black solid;
      border-right:1px black solid;
      border-left:1px black solid;}
   tr:nth-child(even) {
     background-color: #DFEBF8; }
   </style>
</head>
<body>
   <h2>Automation Testing Device Log</h2>
<table>
<tr>
   <th>ID</th>
   <th style="width:70%">Log</th>
   <th>Desired Capabilities</th>
</tr>
<?php
while ($row=mysqli_fetch_array($result))
{
   echo "<tr>";
   echo "<td>".$row['id']."</td>";
   echo "<td>".nl2br($row['log'])."</td>";
   echo "<td>".nl2br($row['desired_caps'])."</td>";
   echo "</tr>";
}
mysqli_close($con);
?>
</table>
</body>