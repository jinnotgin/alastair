<?php
	if (isset($_GET['mode']) == false || isset($_GET['type']) == false) {
		die('ERROR: Not enough paramaters given.');
	} else {
		$mode = $_GET['mode'];
		$type = $_GET['type'];
	}
	
	$homedir = "/home/pi/alastair";
	$dir = "/mnt/usbstorage/alastair"."/data/";
	$allJson = "/run/shm/alastairData.json";

	// [START OF AUTOMATED COMPILE OF DATA]
	$settings = [];
	$settingsJson = file_get_contents($allJson);
	if ($settingsJson != false) {
		$settings = json_decode($settingsJson,true);
	}
	
	// make sure lightlevel always have 2 decimal points
	$settings["lightLevel"] = number_format($settings["lightLevel"], 2, '.', '');
	// [END OF AUTOMATED COMPILE OF DATA]
	
	
	// [START OF MANUAL COMPILE OF DATA]
	/*$settingsKeys = scandir($dir);
	$settingsKeys = str_replace('.dat','',$settingsKeys);
	array_shift($settingsKeys);	// removes "."
	array_shift($settingsKeys); // removes ".."
		
	foreach ($settingsKeys as $key) {
		$value = file_get_contents($dir.$key.".dat");
		if ($value != false) {
			$value = str_replace("\n",'',$value);
			$settings[$key] = (int)$value;
		} else {
			$settings[$key] = 0;
		}
	}
	
	// set light (has permissions problem)
	//exec("/usr/bin/python ".$homedir."/sensorLight.py -once",$sensorLight_output);
	//$settings["lightLevel"] = $sensorLight_output;
		
	$settings["lightLevel"] = file_get_contents($dir."lightLevel.dat");
	
	# get validaity of presenceMotion
	if ($settings["presenceMotion"] != 0) {
		$presenceMotion_elapsed = time() - $settings["presenceMotion"];
		
		if ($presenceMotion_elapsed <= 300) {
			$settings["presenceMotion"] = 1;
		} else {
			$settings["presenceMotion"] = 0;
		}
	}
	
	# convert wifi values
	if (array_sum(str_split($settings["presenceWifi"])) == 0) {
		$settings["presenceWifi"] = 0;
	} else {
		$settings["presenceWifi"] = 1;
	} */
	// [END OF MANUAL COMPILE OF DATA]
	
	# get current Bedroom Lamp status
	$settings["bedroomLamp_status"] = 0;
	$bedroomLamp_status = explode('"', file_get_contents("http://192.168.1.76/cgi-bin/json.cgi?get=state"))[3];
	if ($bedroomLamp_status == "on") {
		$settings["bedroomLamp_status"] = 1;
	} else if ($bedroomLamp_status == "off") {
		$settings["bedroomLamp_status"] = 0;
	}

	# get current Bedroom Fan status
	$bedroomFan_status = explode('"', file_get_contents("http://192.168.1.77/cgi-bin/json.cgi?get=state"))[3];
	if ($bedroomFan_status == "on") {
		$settings["bedroomFan_status"] = 1;
	} else if ($bedroomFan_status == "off") {
		$settings["bedroomFan_status"] = 0;
	}
	
	# convert roomSleep value if necessary
	if ($settings["roomSleep"] == -1) {
		$settings["roomSleep"] = 0;
	}
	
	# add current time
	$settings["time"] = date('h:i:s A');
	
	# add more stuff
	$uptime = str_replace(" day, ",":",shell_exec("uptime"));
	$uptime = str_replace(" days, ",":",$uptime);
	$settings["serverUptime"] = explode(",",explode(" up ", $uptime)[1])[0];
	$settings["serverTemp"] = round(floatval(shell_exec("cat /sys/class/thermal/thermal_zone0/temp"))/1000, 2);
	$settings["serverCpu"] = ((string)sys_getloadavg()[0]*100).".00";
	$settings["serverRam"] = round(get_server_memory_usage(),2);
	
	$rulesProcessor_trigger = false;
	$callerName = "PHP";
	switch ($mode){
		case('get'): {
			if ($type == 'all') {
				echo json_encode($settings);
			} else if ($type == 'room') {
				echo $settings["roomSleep"];
			} else if ($type == 'keepkeepPcAwake') {
				echo $settings["keepkeepPcAwake"];
			} else if ($type == 'pc') {
				echo $settings["presencePc"];
			} else if ($type == 'bluetooth') {
				echo $settings["presenceBt"];
			} else if ($type == 'light') {
				echo $settings["lightLevel"];
			}
			break;
		}
		case('set'): {
			if ($type == 'room' && isset($_GET['state']) && ($_GET['state'] == -1 || $_GET['state'] == 0 || $_GET['state'] == 1)) {
				$rulesProcessor_trigger = true;
				$callerName = "roomSleep";
				
				$settings["roomSleep"] = (int) $_GET['state'];
				file_put_contents($dir."roomSleep.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;  //echo 1 here mean the change was successful
				else echo "roomSleep = ".$settings["roomSleep"];
			} else if ($type == 'switch_keepPcAwake' && isset($_GET['state']) && ($_GET['state'] == 0 || $_GET['state'] == 1)) {
				$settings["keepPcAwake"] = (int) $_GET['state'];
				file_put_contents($dir."keepPcAwake.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "keepPcAwake = ".$settings["keepPcAwake"];
			/*} else if ($type == 'bluetooth' && isset($_GET['state']) && ($_GET['state'] == 0 || $_GET['state'] == 1)) {
				$settings["presenceBt"] = (int) $_GET['state'];
				file_put_contents($dir."presenceBt.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "presenceBt = ".$settings["presenceBt"];*/
			} else if ($type == 'pc' && isset($_GET['state']) && ($_GET['state'] == 0 || $_GET['state'] == 1)) {
				$rulesProcessor_trigger = true;
				$callerName = "presencePc";
				
				$settings["presencePc"] = (int) $_GET['state'];
				file_put_contents($dir."presencePc.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "presencePc = ".$settings["presencePc"];
			/*} else if ($type == 'light' && isset($_GET['state'])) {
				//if (($settings["roomSleep"] > 450) && ($_GET['state'] <= 450)) || (($settings["roomSleep"] < 550) && ($_GET['state'] >= 550)) {
					if (($settings["lightLevel"] > 450 && $_GET['state'] <= 450) || ($settings["lightLevel"] < 550 && $_GET['state'] >= 550)) {
					$rulesProcessor_trigger = true;	
					$callerName = "lightLevel";
				}
				$settings["lightLevel"] = (int) $_GET['state'];
				file_put_contents($dir."lightLevel.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "lightLevel = ".$settings["lightLevel"];
			*/} else if ($type == 'sensorsMode' && isset($_GET['state'])) {
				$rulesProcessor_trigger = true;
				$callerName = "sensorsMode";
				
				$settings["sensorsMode"] = (int) $_GET['state'];
				file_put_contents($dir."sensorsMode.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "sensorsMode = ".$settings["sensorsMode"];
			} else if ($type == 'switch_bedroomLight' && isset($_GET['state'])) {
				$setTo = 'off';
				if ($_GET['state'] == 1) $setTo = 'on';
				file_get_contents("http://192.168.1.76/cgi-bin/json.cgi?set=".$setTo);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "switch_bedroomLight = ".$setTo;
			} else if ($type == 'switch_bedroomFan' && isset($_GET['state'])) {
				$setTo = 'off';
				if ($_GET['state'] == 1) $setTo = 'on';
				file_get_contents("http://192.168.1.77/cgi-bin/json.cgi?set=".$setTo);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "switch_bedroomFan = ".$setTo;
			} else {
				die('ERROR: Not enough or invalid paramaters given.');
			}
			// saveData();
			break;
		}
		case('preset'): {
			if ($type == 'pcPresent') {
				$settings["presencePc"] = (int) 1;
				file_put_contents($dir."presencePc.dat", 1);
				$settings["roomSleep"] = (int) 0;
				file_put_contents($dir."roomSleep.dat", 0);
				$settings["keepPcAwake"] = (int) 0;
				file_put_contents($dir."keepPcAwake.dat", 0);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo json_encode($settings);
				
				$rulesProcessor_trigger = true;
				$callerName = "onResume";
			}
			//saveData();
			break;
		}
	}
	
	if ($rulesProcessor_trigger == true) {
		//exec("/usr/bin/python ".$homedir."/rulesProcessor_php.py ".$callerName,$rulesProcessor_output);
		$rulesProcessor_output = file_get_contents('http://127.0.0.1:5000/php_'.$callerName);
		//var_dump($rulesProcessor_output);
	}
	
	
	function get_server_memory_usage() {
		$free = shell_exec('free');
		$free = (string)trim($free);
		$free_arr = explode("\n", $free);
		$mem = explode(" ", $free_arr[1]);
		$mem = array_filter($mem);
		$mem = array_merge($mem);
		$memory_usage = $mem[2]/$mem[1]*100;

		return $memory_usage;
	}
	
	function saveData(){
		/*global $settings, $file;
		
		if ($settings["presenceBt"] == 1 && $settings["presencePc"] == 1) $settings["presence"] = 9;
		else if ($settings["presenceBt"] == 1) $settings["presence"] = 1;
		else if ($settings["presencePc"] == 1) $settings["presence"] = 2;
		else $settings["presence"] = 0;
		
		file_put_contents($file,serialize($settings));*/
	}

?>