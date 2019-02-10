<?php
$logLines = [];

// $bedLampLog = '/home/pi/automation/bedLamp.log';
// $logLines = array_merge($logLines, preg_replace('/ - /', ' - switchRegulator: ', file($bedLampLog)));

$logsDir = '/home/pi/alastair/logs';
$logsDir_scanned = array_diff(scandir($logsDir), array('..', '.'));

foreach ($logsDir_scanned as $logFileName) {
	if (strpos($logFileName, '.log') !== false) {
		$logLines = array_merge($logLines,  preg_replace('/ - /', ' - '.str_replace(".log","",$logFileName).': ', file($logsDir.'/'.$logFileName)));
	}
}

// sort by time descending
arsort($logLines);

// remove miliseconds from time
$logLines = preg_replace('/,\d{3}/', '', $logLines);

// cut to first 1000 lines
$logLines= array_slice($logLines, 0, 1000);

echo "<b>Alastair's Consolidated Logs</b><br><br>";
echo "<u>".date('Y-m-d H:i:s', time())."</u> - System Time<br>";
foreach($logLines as $f){
    echo $f."<br />";
}

?>