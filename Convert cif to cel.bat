:: Name: 		Convert cif to cell.bat
:: Author:   	Joshua L. Vincent, ASU Crozier Group
:: Email: 		Joshua.Vincent@asu.edu
:: Purpose: 	This batch file converts .cif structure files in a specified folder
::				to .cel files, which are saved in a specified folder. The .cel files
::				can be rotated about a specified axis a designated number of degrees.
::				The .cel files are saved with the same filename as the .cif files 
::				used in the conversion.
:: 				RUN THIS BATCH FILE ONLY AFTER ENTERING THE VARIABLES SPECIFIED IN SECTION 1.
:: 
:: Revisions: 	November 25, 2019 - Set up beginning of file and the header.
::									Began witing and testing code.
::				November 26, 2019 - Implemented delayed expansion setting in for loop
::										(this solved the variable call issues which allowed
::										the file name to be written as .cel).
::									Code works acceptably for current purposes.
::				December 03, 2019 - Added and clarified documentation
::
::
:: */*/* OUTLINE of CODE and ALGORITHM */*/*
:: 	1. USER INPUT and SETUP
:: 	1.1) 	Specify a directory which contains the .cif files you want to convert to .cel
:: 	1.2) 	Specify how many degrees you'd like to rotate the files, and specify rotation axis. Can be set to 0.
:: 	1.3) 	Specify the directory where you'd like to save the .cel files
::	
::	2. MAIN CODE
::	2.1)	Create a temporary directory (cif_path\temp_cel) to store the cel files before they are rotated
:: 	2.2) 	Read the .cif files from the chosen directory where they are located; Convert from .cif to .cel, store in temporary directory
::			Apply rotation along specified degrees and rotation axis, save rotated cells to .cel directory
::	2.3)	Delete the temporary directory and its contents
:: */*/* END CODE */*/*
::
:: ---------------------------------------------------------------------------------------------------------
@echo OFF

:: */*/* BEGIN BATCH FILE */*/*
:: 	1. USER INPUT and SETUP */*/*

:: 	1.1) 	Specify a directory which contains the .cif files you want to convert to .cel */*/*

REM Set working directory to E:\
f:

REM Create cif_directory variable with path to folder containing .cif files to be converted 
set cif_directory=F:\N2PtNP_MS_Sims\2_OutputData\20210309_operando_paper\cif

:: 	1.2) 	Specify how many degrees you'd like to rotate the files, and specify rotation axis */*/*

REM Degrees of rotation
set r_deg=0
REM Rotation x axis
set r_axis_x=0
REM Rotation y axis
set r_axis_y=0
REM Rotation z axis
set r_axis_z=0

:: 	1.3) 	Specify the directory where you'd like to save the .cel files */*/*

REM Create cel_directory variable with path to folder containing 
set cel_directory=F:\N2PtNP_MS_Sims\2_OutputData\20210309_operando_paper\cel

REM if the path doesn't exist, create it
if exist "%cel_directory%" echo The cel directory already exists at "%cel_directory%"
if not exist "%cel_directory%" echo The cel directory does not exist and will be made at "%cel_directory%"
if not exist "%cel_directory%" mkdir "%cel_directory%"

::  2. MAIN CODE */*/*
::	2.1)	Create a temporary directory (cif_path\temp_cel) to store the cel files before they are rotated */*/*

REM Create temporary cel directory in the cif directory
set temp_cel_directory=%cif_directory%\cel_temp

REM if the path doesn't exist, create it
if exist "%temp_cel_directory%" echo The temporary cel directory already exists at "%temp_cel_directory%"
if not exist "%temp_cel_directory%" echo The cel directory does not exist and will be made at "%temp_cel_directory%"
if not exist "%temp_cel_directory%" mkdir "%temp_cel_directory%"

:: 	2.2) 	Read the .cif files from the chosen directory where they are located, convert them from .cif to .cel, store in temporary directory  */*/*

setlocal ENABLEDELAYEDEXPANSION
REM For all .cif files in the cif_directory...
for %%f in ("%cif_directory%\*.cif") do (
	
	REM Create a filename variable which contains the .cel extension
	set cif_file_name=%%~nxf
	SET NoExtension_file_name=!cif_file_name:~0,-3!
	SET cel_file_name=!NoExtension_file_name!cel
		
	REM Build the .cel from the .cif file and save it in the temporary directory
	BuildCell --cif="%cif_directory%\!cif_file_name!" --output="%temp_cel_directory%\!cel_file_name!"
	
	REM Apply the rotation to the .cel file and save it in the cel_directory
	CellMuncher --preview=VESTA --rotate-non-periodic=%r_axis_x%,%r_axis_y%,%r_axis_z%,%r_deg% --input="%temp_cel_directory%\!cel_file_name!" --output="%cel_directory%\!cel_file_name!")

::	2.3)	Delete the temporary directory */*/*

REM Remove the temporary .cel directory
echo on
rmdir /Q /S "%temp_cel_directory%"

:: */*/* END BATCH FILE */*/*