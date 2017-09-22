$CurrentDir = Split-Path $MyInvocation.MyCommand.Path
$TestDir    = "$CurrentDir/test"
#move to folder
$FileFrom   = "$TestDir/test.txt"
$FolderTo   = "$TestDir/temp"
Copy-Item $FileFrom $FolderTo -Recurse
Copy-Item $FileFrom -Destination "$FolderTo/test2.txt" -Recurse

#Delete Copied File In Folder
$File1      = "$TestDir/temp/test.txt"
$File2      = "$TestDir/temp/test2.txt"
Remove-Item $File1 -force
Remove-Item $File2 -force