<?php
	if (isset($_GET['mode']) == false || isset($_GET['type']) == false) {
		die('ERROR: Not enough paramaters given.');
	} else {
		$mode = $_GET['mode'];
		$type = $_GET['type'];
	}
	
	$homedir = "/home/pi/alastair";
	$dir = $homedir."/data/";
	
	/*$settingsDefault = [
		"presence"=>0,
		"presenceBt"=>0,
		"presencePc"=>0,
		"presenceMotion"=>0,
		"roomSleep"=>0,
		"pcAwake"=>0,
		"lightLevel"=>0
	];*/
	$settings = [];
	$settingsKeys = ["presenceMotion","presenceBt","presencePc","roomSleep","pcAwake","lightLevel"];
	
	/*$settingsJson = file_get_contents($dir."all.json");
	if ($settingsJson != false) {
		$settings = json_decode($settingsJson,true);
	} else {
		$settings = $settingsDefault;
	}
	
	$settings["lightLevel"] = file_get_contents($dir."lightLevel.dat");*/
	
	foreach ($settingsKeys as $key) {
		$value = file_get_contents($dir.$key.".dat");
		if ($value != false) {
			$settings[$key] = $value;
		} else {
			$settings[$key] = 0;
		}
	}
	
	# set overall presence (depends only on PC and BT for now)
	$presenceOverall = 0;
	if ($settings["presenceBt"] == 1 && $settings["presencePc"] == 1) $presenceOverall = 9;
	else if ($settings["presencePc"] == 1) $presenceOverall = 2;
	else if ($settings["presenceBt"] == 1) $presenceOverall = 1;
	$settings["presence"] = $presenceOverall;
	
	# get validaity of presenceMotion
	if ($settings["presenceMotion"] != 0) {
		$presenceMotion_elapsed = time() - $settings["presenceMotion"];
		
		if ($presenceMotion_elapsed <= 180) {
			$settings["presenceMotion"] = 1;
		} else {
			$settings["presenceMotion"] = 0;
		}
	}
	
	# get current Bedroom Lamp status
	$settings["bedroomLamp_status"] = 0;
	$bedroomLamp_status = explode('"', file_get_contents("http://192.168.1.76/cgi-bin/json.cgi?get=state"))[3];
	if ($bedroomLamp_status == "on") {
		$settings["bedroomLamp_status"] = 1;
	} else if ($bedroomLamp_status == "off") {
		$settings["bedroomLamp_status"] = 0;
	}
	
	# convert roomSleep value if necessary
	if ($settings["roomSleep"] == -1) {
		$settings["roomSleep"] = 0;
	}
	
	$rulesProcessor_trigger = false;
	$callerName = "PHP";
	switch ($mode){
		case('get'): {
			if ($type == 'all') {
				echo json_encode($settings);
			} else if ($type == 'room') {
				echo $settings["roomSleep"];
			} else if ($type == 'pcAwake') {
				echo $settings["pcAwake"];
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
			} else if ($type == 'pcAwake' && isset($_GET['state']) && ($_GET['state'] == 0 || $_GET['state'] == 1)) {
				$settings["pcAwake"] = (int) $_GET['state'];
				file_put_contents($dir."pcAwake.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "pcAwake = ".$settings["pcAwake"];
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
			} else if ($type == 'light' && isset($_GET['state'])) {
				//if (($settings["roomSleep"] > 450) && ($_GET['state'] <= 450)) || (($settings["roomSleep"] < 550) && ($_GET['state'] >= 550)) {
					if (($settings["lightLevel"] > 450 && $_GET['state'] <= 450) || ($settings["lightLevel"] < 550 && $_GET['state'] >= 550)) {
					$rulesProcessor_trigger = true;	
					$callerName = "lightLevel";
				}
				$settings["lightLevel"] = (int) $_GET['state'];
				file_put_contents($dir."lightLevel.dat", $_GET['state']);
				
				if (isset($_GET['json']) && $_GET['json'] == 1) echo 1;
				else echo "lightLevel = ".$settings["lightLevel"];
			}  else {
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
				$settings["pcAwake"] = (int) 0;
				file_put_contents($dir."pcAwake.dat", 0);
				
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
		exec("/usr/bin/python ".$homedir."/rulesProcessor_php.py ".$callerName,$rulesProcessor_output);
		//var_dump($rulesProcessor_output);
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