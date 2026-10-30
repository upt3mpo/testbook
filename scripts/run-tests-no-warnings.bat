@echo off
REM Keep CRLF line endings (enforced by .gitattributes); cmd mis-parses LF-only batch files.
REM Run tests without NO_COLOR/FORCE_COLOR warnings

REM Set FORCE_COLOR to 0 to disable colored output and avoid warnings
set FORCE_COLOR=0

REM Run the command passed as arguments
%*
