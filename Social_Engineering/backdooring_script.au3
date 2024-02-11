#include <StaticConstants.au3>
#include <WindowsConstants.au3>

Local $arr[2] ;The array containing the URL's

$arr[0] = "url1" ; The first URL, replace it 
$arr[1] = "url2" ; The second URL, replace it

for $url In $arr
    $file = _DownloadFile($url) ; We download the URL in the array and get the location of the executable
    shellExecute($file) ; Runs an external program using the ShellExecute API.

Next

Func _DownloadFile($url)
    Local $download, $file, $directory

    $file = StringRegExpReplace($url,"^.*/","") ; We obtain the name of the file.
    
    ; Regular Expression
    ; ^ -> begginin of the string
    ; . -> any character
    ; * -> kleene star
    ; / -> "/" character
    ; So, our function finds the all characters from beginning up to the last / inclusively, and replace it by the third parameter


    $directory = @TempDir & $file ; We get the directory of the file. @TempDir is the macro that gives the temp dir as "../___ .. /"
    $download = InetGet($url,$directory,17,1) ; Downloads a file from the internet using the HTTP, HTTPS or FTP protocol.
    InetClose($download) ; Use the returned handle with InetGetInfo() to determine if there was an error with the download. The returned handle must be closed with InetClose().
    Return $directory ; Return the path
EndFunc ;==>_GetURLImage
