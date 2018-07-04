@echo off
cd /d %~dp0
pushd \\UNC\path

md test
rename test Fine
rd Fine
