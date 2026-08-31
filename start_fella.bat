@echo off
:: This script starts Fella's brain in the background without opening a command window
cd /d "c:\Users\Dell\Downloads\enn"
start /B pythonw fella_server.py
