#!/bin/zsh
# Export decks to PDF with PowerPoint (fonts must be installed; see README).
# usage: tools/export_pdf.sh name [name...]   (name.pptx files in the folder below)
D=~/Library/Containers/com.microsoft.Powerpoint/Data/kenya-export/v2
HFS=$(osascript -e "POSIX file \"$D\" as text"); HFS=${HFS%:}
for d in "$@"; do
rm -f $D/$d.pdf
osascript <<EOF 2>&1
with timeout of 1800 seconds
tell application "Microsoft PowerPoint"
  open file "${HFS}:${d}.pptx"
  repeat 120 times
    if (name of every presentation) contains "${d}.pptx" then exit repeat
    delay 3
  end repeat
  delay 5
  if (name of every presentation) does not contain "${d}.pptx" then error "not opened cleanly: " & (name of every presentation as text)
  set p to presentation "${d}.pptx"
  save p in "${HFS}:${d}.pdf" as save as PDF
  delay 5
  close p saving no
end tell
end timeout
EOF
ls -la $D/$d.pdf
done
