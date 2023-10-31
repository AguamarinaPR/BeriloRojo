#!/usr/bin/php -q
<?php
/*
 * Aguamarina Server/Berilo Rojo script 1.0
 * Based on Aptoide server generate script version 1.4
 */
/***************************************/
/*
 * Directory where apk's are stored
 * Configuration changes go here! 
 */
$DIR = "/mnt/c/Users/Quartz/Documents/Eclipse/adt080/eclipse332/workspace/AguamarinaServer/repo/";
$ICON_DIR_OUT = "icons/";

/****************************************/
$ICON_DIR = $DIR.$ICON_DIR_OUT;
$xml_path = $DIR."info.xml";
$loopcount = 0;

if(file_exists($xml_path)){exec('rm ' . $xml_path);}
exec('rm -rf ' . $ICON_DIR);
exec('mkdir ' . $ICON_DIR);
exec('ls ' . $DIR . ' | grep ".apk"', $dump);
echo "\n Berilo Rojo 1.0";
echo "\n Repository generator for Aguamarina";
echo "\n ======================== \n";
$dom = new DomDocument("1.0","UTF-8");
$dom->preserveWhiteSpace = false;
$dom->formatOutput = true;
$root = $dom->createElement('apklst');
$root = $dom->appendChild($root);
if (file_exists($DIR."extras.xml")){
	$extrainfo = new DomDocument("1.0","UTF-8");
	$extrainfo->load($DIR."extras.xml");
}

foreach ($dump as $apk) {

	echo "\nAPK: " . $apk;

	if(ends($apk, "apk")){

	$rtrn = getInfo($apk);

	if($rtrn["icon"] == ""){
		$icon = "";
	}else{
		$icon = getIcon($DIR."/".$apk, $rtrn["icon"], $rtrn["pkg"]);
	}

	echo "\nPackage (hasID): " . $rtrn["pkg"];
	echo "\nVersion: " . $rtrn["ver"];
	echo "\nVersion Code: " . $rtrn["vercode"];
	echo "\nName: " . $rtrn["name"];
	echo "\nIcon: " . $rtrn["icon"];
	echo "\nIcon(L): " . $icon;
	echo "\nDate: " . $rtrn["date"];
	echo "\nMd5Hash: " . $rtrn["md5h"];
	echo "\nSize: " . $rtrn["size"] . "KB";
	echo "\nMinimum Android SDK version: " . $rtrn["sdkver"];
	echo "\n ======================== \n";
	
	$occ = $dom->createElement('package');
	$occ = $root->appendChild($occ);

	$child = $dom->createElement('name');
	$child = $occ->appendChild($child);
	$value = $dom->createTextNode($rtrn["name"]);
	$value = $child->appendChild($value);
       
	$child = $dom->createElement('path');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($apk);
        $value = $child->appendChild($value);

	$child = $dom->createElement('ver');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["ver"]);
        $value = $child->appendChild($value);

	$child = $dom->createElement('vercode');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["vercode"]);
        $value = $child->appendChild($value);

        $child = $dom->createElement('apkid');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["pkg"]);
	$value = $child->appendChild($value);
	
       	$child = $dom->createElement('icon');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($icon);
	$value = $child->appendChild($value);
	
	if (file_exists($DIR."extras.xml")){
		$categ1 = $extrainfo->getElementsByTagName("catg")->item($loopcount);
		$categ1 = $dom->importNode($categ1, true);
		$categ2 = $extrainfo->getElementsByTagName("catg2")->item($loopcount);
		$categ2 = $dom->importNode($categ2, true);
		
		$child = $occ->appendChild($categ1);
	
		$child = $occ->appendChild($categ2);
	
	$loopcount++;
	}
	
	$child = $dom->createElement('date');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["date"]);
	$value = $child->appendChild($value);
		
	$child = $dom->createElement('md5h');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["md5h"]);
	$value = $child->appendChild($value);
	
	$child = $dom->createElement('sz');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["size"]);
	$value = $child->appendChild($value);
	
		$child = $dom->createElement('sdkver');
        $child = $occ->appendChild($child);
        $value = $dom->createTextNode($rtrn["sdkver"]);
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

function getIcon($file, $icon, $apk){
	global $ICON_DIR;
	global $ICON_DIR_OUT;
	exec("unzip " . $file . " -d .tmp");
	exec("mv ./.tmp/".$icon . " " . $ICON_DIR.$apk);
	exec("rm -rf ./.tmp");
	return($ICON_DIR_OUT.$apk); 
}


function getInfo($file){
	global $DIR;
	$send = array();
	exec("./aapt d badging " . $DIR . $file . "|grep application| cut -d\' -f2", $out);
	$send["name"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep application| cut -d\' -f4", $out);
	$send["icon"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep package| cut -d\' -f2", $out);
	$send["pkg"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep package| cut -d\' -f6", $out);
	$send["ver"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep package| cut -d\' -f4", $out);
	$send["vercode"] = implode("",$out);
	$out = "";
	exec("du " . $DIR . $file . "| cut -f1", $out);
	$send["size"] = implode("",$out);
	$out = "";
	exec("./aapt d badging " . $DIR . $file . "|grep sdkVersion| cut -d\' -f2", $out);
	$send["sdkver"] = implode("",$out);
	$out = "";
	exec("md5sum " . $DIR . $file . "| cut -d\  -f1", $out);
	$send["md5h"] = implode("",$out);
	$out = "";
	exec("stat " .$DIR . $file . "|grep Change| cut -d ' ' -f2", $out);
	$send["date"] = implode("",$out);
	return($send);
}

function ends($string, $end){
	$len = strlen($end);
	$string_end = substr($string, strlen($string) - $len);
	return $string_end == $end;
}
?>
