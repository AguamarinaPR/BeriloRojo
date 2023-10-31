#!/usr/bin/php -q
<?php
/*
 * Aguamarina Repo Description Generator/Berilo Rojo Extras script 1.0
 * Based on Aptoide server generate script version 1.4
 */
/***************************************/
/*
 * Directory where apk's are stored
 * Configuration changes go here! 
 */
$DIR = "/mnt/c/Users/Quartz/Documents/Eclipse/adt080/eclipse332/workspace/AguamarinaServer/repo/";

/****************************************/
$xml_path = $DIR."extras.xml";

if(file_exists($xml_path)){
echo "\nIMPORTANT, PLEASE READ IF YOU ALREADY WROTE AN extras.xml \n";
echo "\nIf you already wrote an extras.xml this generator will overwrite ALL user added information. \n";
echo "A backup named 'extras.xml.bak' will be made so you can transfer the information to the new one. \n";
echo "Are you sure you want to overwrite extras.xml? if so, type 'yes': ";
$handle = fopen ("php://stdin","r");
$line = fgets($handle);
if(trim($line) != 'yes'){
    echo "Cancelling...\n";
    exit;
} else {
	exec('cp -f ' . $xml_path . ' ' . $xml_path . '.bak');
}
echo "\n";
echo "Proceeding...\n";
}

if(file_exists($xml_path)){exec('rm ' . $xml_path);}
exec('ls ' . $DIR . ' | grep ".apk"', $dump);
echo "\n Berilo Rojo Extras 1.0";
echo "\n Description file generator for Aguamarina";
echo "\n ======================== \n";
$dom = new DomDocument("1.0","UTF-8");
$dom->preserveWhiteSpace = false;
$dom->formatOutput = true;
$root = $dom->createElement('extras');
$root = $dom->appendChild($root);

foreach ($dump as $apk) {

	echo "\nAPK: " . $apk;

	if(ends($apk, "apk")){

	$rtrn = getInfo($apk);

	echo "\nName: " . $rtrn["name"];
	echo "\nPackage ID: " . $rtrn["pkg"];
	echo "\n ======================== \n";
	
	$occ = $dom->createElement('pkg');
	$occ = $root->appendChild($occ);

	$child = $dom->createElement('apkid');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["pkg"]);
		$value = $child->appendChild($value);
       
	$child = $dom->createElement('cmt');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode("This is a description, write any information about the application here.");
        $value = $child->appendChild($value);
	
	$child = $dom->createElement('catg');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode("Main Category");
        $value = $child->appendChild($value);
	
	$child = $dom->createElement('catg2');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode("Secondary Category");
        $value = $child->appendChild($value);
	}

}
$xml_string = $dom->saveXML();
$fp = @fopen($xml_path,'w');
if(!$fp) {
       die('Error cannot create XML file');
}
fwrite($fp,$xml_string);
fclose($fp);
echo "\nXML FILE SUCCESSFULLY CREATED!\n";
echo "\nBe sure to edit the generated xml file extras.xml with information about the applications in your repository!\n";
echo "\nAfter editing categories, make sure to regenerate info.xml to add them to it.\n";

function getInfo($file){
	global $DIR;
	$send = array();
	exec("./aapt d badging " . $DIR . $file . "|grep package| cut -d\' -f2", $out);
	$send["pkg"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep application| cut -d\' -f2", $out);
	$send["name"] = implode("",$out);
	$out = "";
	return($send);
}

function ends($string, $end){
	$len = strlen($end);
	$string_end = substr($string, strlen($string) - $len);
	return $string_end == $end;
}
?>
