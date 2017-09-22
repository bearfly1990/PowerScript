$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
$TestDir    = "$CurrentDir/test"
#move to folder
$FileFrom   = "$TestDir/test.txt"
$FolderTo   = "$TestDir/temp"
Move-Item $FileFrom $FolderTo -force

#move back
$FileFrom   = "$TestDir/temp/test.txt"
$FolderTo   = $TestDir
Move-Item $FileFrom $FolderTo -force