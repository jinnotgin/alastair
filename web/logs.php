<?php
$logLines = [];

// $bedLampLog = '/home/pi/automation/bedLamp.log';
// $logLines = array_merge($logLines, preg_replace('/ - /', ' - switchRegulator: ', file($bedLampLog)));

$logsDir = '/home/pi/alastair/logs';
$logsDir_scanned = array_diff(scandir($logsDir), array('..', '.'));

foreach ($logsDir_scanned as $logFileName) {
	if (strpos($logFileName, '.log') !== false) {
	//if (preg_match("/.log$/", $logFileName)) {
		$currentLog = file($logsDir.'/'.$logFileName);
		$currentLog_recent = array_splice($currentLog, count($currentLog)-150);
		$logLines = array_merge($logLines,  preg_replace('/ - /', ' '.str_replace(".log","",$logFileName).': ', $currentLog_recent));
	}
}

// sort by time descending
arsort($logLines);

// remove miliseconds from time
$logLines = preg_replace('/,\d{3}/', '', $logLines);

// cut to first 1000 lines
$logLines= array_slice($logLines, 0, 1000);

//echo "<b>Alastair's Consolidated Logs</b><br><br>";
//echo "<u>".date('Y-m-d H:i:s', time())."</u> - System Time<br>";
$dateCurrent = "";
foreach($logLines as $f) {
	$fArr = explode(" ",$f);
	$dateNow = array_shift($fArr);
	if ($dateCurrent != $dateNow) {
		$dateCurrent = $dateNow;
		echo "<b><u>".$dateCurrent."</u></b><br />";
	}
	
	$timeNow = array_shift($fArr);
	
	$fArr[0] = preg_replace("/\.\d+/", "", $fArr[0]);
    echo "[".$timeNow."] ".implode(" ",$fArr)."<br />";
}

?>