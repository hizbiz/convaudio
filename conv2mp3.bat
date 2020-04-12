date /t
time /t
for /r C:\record %%f in (*.wav) do (
ffmpeg -i "%%f" -vn -ar 44100 -ac 2 -b:a 192k "%%f.mp3
)
time /t