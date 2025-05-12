set appFile to (POSIX file "/Users/kian/Desktop/OVERSIGHT") as alias
set appFilePath to POSIX path of appFile
set iconFilePath to "/Users/kian/Desktop/Software/nikimonitorscreen/OVERSIGHT.png"

tell application "Finder"
  try
    set file_icon to POSIX file iconFilePath
    set file_to_icon to POSIX file appFilePath
    set icon of file_to_icon to file_icon
    log "Icon set successfully!"
  on error errMsg
    log "Error setting icon: " & errMsg
  end try
end tell
