@ECHO OFF
:start1
TIMEOUT 1 >nul
cls
ECHO.
ECHO 			Ghost Car Launcher
ECHO.
TIMEOUT 3 >nul
ECHO.
ECHO Please choose an option to Run.
ECHO "1> All Programs"
ECHO "2> TCP Server"
ECHO "3> Prediction CNN"
ECHO "4> SSH Connection"
ECHO "5> Exit"
ECHO.
SET /P _option= ">"
IF "%_option%"=="1" GOTO:ALL
IF "%_option%"=="2" GOTO:TCP
IF "%_option%"=="3" GOTO:CNN
IF "%_option%"=="4" GOTO:SSH
IF "%_option%"=="5" GOTO:END
ECHO.
ECHO INVALID SELECTION..!!
ECHO.
GOTO :start1
:TCP
ECHO.
ECHO Running TCP Server
ECHO.
TIMEOUT 1 >nul
start cmd.exe /k "python uploadTCP.py"
TIMEOUT 3 >nul
GOTO :start1
:CNN
ECHO.
ECHO Running CNN Prediction Program
ECHO.
TIMEOUT 1 >nul
start cmd.exe /k "python videoPredict.py"
TIMEOUT 3 >nul
GOTO :start1
:SSH
ECHO.
ECHO Opening New SSH Connection
ECHO.
TIMEOUT 1 >nul
start cmd.exe /k "ssh pi@192.168.43.222"
TIMEOUT 3 >nul
GOTO :start1
:ALL
ECHO.
ECHO Launching All Programs
ECHO.
TIMEOUT 2 >nul
start cmd.exe /k "python videoPredict.py"
TIMEOUT 2 >nul
start cmd.exe /k "python uploadTCP.py"
TIMEOUT 2 >nul
start cmd.exe /k "ssh pi@192.168.43.222"
start cmd.exe /k "ssh pi@192.168.43.222"
TIMEOUT 3 >nul
GOTO :start1
:END
PAUSE