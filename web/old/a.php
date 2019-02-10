<?php
//echo exec('whoami');
$homedir = "/mnt/usbstorage/alastair";
$dir = $homedir."/data/";

echo file_get_contents($dir."lightLevel.dat")


?>