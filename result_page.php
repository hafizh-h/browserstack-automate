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
   <title>Automated Testing Device Log</title>
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
      width:70%;}
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
    <?php
        $query = mysqli_query($con,"SELECT * FROM device_log ORDER BY id DESC LIMIT 1");
        $desired_caps = mysqli_fetch_array($query);
	?>
   <h2>Automation Testing Device Log</h2>
   <table>
        <tr>
            <td style="background-color: #c1d5fb">Build</td>
            <td style="background-color: #c1d5fb"><?php echo $desired_caps['build']; ?></td>
        </tr>
        <tr>
            <td style="background-color: #c1d5fb">Platform Version</td>
            <td style="background-color: #c1d5fb"><?php echo $desired_caps['platformVersion']; ?></td>
        </tr>
        <tr>
            <td style="background-color: #c1d5fb">Device Name</td>
            <td style="background-color: #c1d5fb"><?php echo $desired_caps['deviceName']; ?></td>
        </tr>
        <tr>
            <td style="background-color: #c1d5fb">App</td>
            <td style="background-color: #c1d5fb"><?php echo $desired_caps['app']; ?></td>
        </tr>
        <tr>
            <td style="background-color: #c1d5fb">Type</td>
            <td style="background-color: #c1d5fb">
                <?php
                if($desired_caps['type'] == 'cold') {
                    echo 'Cold Launch';
                }
                elseif($desired_caps['type'] == 'warm') {
                    echo 'Warm Launch';
                }
				?>
            </td>
        </tr>
    </table>
    <br>
    <table style="text-align:center">
        <tr>
           <th>Iteration</th>
           <th>Displayed</th>
           <th>Fully Drawn</th>
        </tr>
        <?php
        while($row = mysqli_fetch_array($result))
        {
           echo "<tr>";
           echo "<td>".$row['iteration']."</td>";
           echo "<td>".$row['displayed']."</td>";
           echo "<td>".$row['fully_drawn']."</td>";
           echo "</tr>";
        }
        mysqli_close($con);
        ?>
    </table>
</body>