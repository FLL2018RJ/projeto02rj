<!DOCTYPE html>
<html>
<?php
$page = $_SERVER['PHP_SELF'];
$sec = "40";
//setlocale(LC_ALL, "pt_BR", "ptb", "pt_BR.utf-8", "portuguese");
//date_default_timezone_set("America/Sao_Paulo");
//echo strftime("%A, %d de %B de %Y", strtotime("today"));
header("Content-Type: text/html; Content-Language: pt-br; charset=utf-8_encode", true);
?>
<head>
<meta http-equiv="refresh" content=<?php echo $sec;?> URL=<?php echo $page;?>>
<!--<meta http-equiv="content-Type" content="text/html; charset=iso-8859-1; pt-br"/>-->

<style>
        body
        {
            font-family: arial,verdana,sans-serif,Georgia, "Times New Roman", Times, serif;
            text-align:center;
            background:#cceeff;
        }
        h1
        {
            text-shadow: 5px 5px 5px #aaaaaa;
        }
</style>
</head>
<body>
<!--<meta http-equiv="content-Type" content="text/html; charset=iso-8859-1; pt-br"/>-->
<h1 lang="pt-br" charset=iso-8859-1>ESTA&Ccedil;&Atilde;O DE ALIMENTA&Ccedil;&Atilde;O</h1>
<?php
$username = "root";
$password = "1234";
$database = "db_estacao";
//Create connection
mysql_connect("localhost",$username,$password) or die ("Unable to connect");
@mysql_select_db($database) or die ("Could not select database");
$query = "SELECT * FROM estacao e ORDER by id DESC LIMIT 25";
$result=mysql_query($query);
$num=mysql_numrows($result);
mysql_close();?>
<table border=1 align=center>
<tr>	
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Temp Bebedouro</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Temp Po&ccedil;o</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">&Aacute;gua Bebedouro</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">&Aacute;gua Po&ccedil;o</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Alimento</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Data</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Hor&aacute;rio</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">V&aacute;lvula</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Bomba</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Mensagem</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Consumo &Aacute;gua</font></th>
		<th><font div style="color:Blue" face="Arial, Helvetica, sans-serif">Consumo Ra&ccedil;&atilde;o</font></th>
		
</tr>
<?php
$i=0;
while ($i < $num)
{
$temp1=mysql_result($result,$i,"temp1");
$temp2=mysql_result($result,$i,"temp2");
$ultra1=mysql_result($result,$i,"ultra1");
$ultra2=mysql_result($result,$i,"ultra2");
$peso=mysql_result($result,$i,"peso");
$datetime=mysql_result($result,$i,"datetime");
$date = date('d/m/Y', strtotime($datetime));
$time = date('H:i:s A', strtotime($datetime));
$statusValvula=mysql_result($result,$i,"status_valvula");
$statusBomba=mysql_result($result,$i,"status_bomba");
$mensagem=mysql_result($result,$i,"mensagem");
$consumoAgua=mysql_result($result,$i,"consumo_agua");
$consumoAlimento=mysql_result($result,$i,"consumo_alimento");
//$datetime=mysql_result($result,$i,"data");
//$date = date('d/m/Y', strtotime($datetime));
//  //$date = date('jS F Y', strftime($datetime));
//    //$day = date('l', strtotime($datetime));
//$time = date('H:i:s A', strtotime($datetime));
//$nome=mysql_result($result,$i,"nome");
//$image=mysql_result($result,$i,"Image")
?>
<tr>
<!--a http-equiv="content-Type" content="text/html; charset=utf-8; pt-br"/>-->
<td><font face="Arial, Helvetica, sans-serif"><?php echo $temp1; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $temp2; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $ultra1; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $ultra2; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $peso; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $date; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $time; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $statusValvula; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $statusBomba; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $mensagem; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $consumoAgua; ?></font></td>
<td><font face="Arial, Helvetica, sans-serif"><?php echo $consumoAlimento; ?></font></td>
</tr>
<?php $i++;
}?>
</table>
</body>
</html>



