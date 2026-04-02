* roundhouse
5, 3, 7, 8, 19, 4, 5

1000, 800

200, 150

for i in $(seq -f "%05g" 0 100000) ; do screencapture -x -R0,0,1600,1200 caps/"screen_${i}.png"; sleep 0.01 ; done
