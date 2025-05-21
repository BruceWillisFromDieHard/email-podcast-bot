set targetPhoneNumber to "+61449510357" -- Your iPhone number
set audioFile to "/Users/andrewknowles/Desktop/email-podcast/daily_email_recap.mp3"

tell application "Messages"
    set myBuddy to buddy targetPhoneNumber of service "E:andrewknowles94@gmail.com"
    send POSIX file audioFile to myBuddy
end tell