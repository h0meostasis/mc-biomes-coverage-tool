#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

^u::
Loop, 500
{
MouseClick, Left, 800, 145, 1, 5
Sleep, 10000
MouseClick, Left, 820, 945, 1, 100
}
return

Esc::ExitApp