mencoder mf:// on:w=800:h=600:fps=4 -ovc lavc -o output.avi \*.png
mencoder -speed 1/10 output.avi -ovc copy -nosound -o slower.flv

convert -delay 10 -loop 0 inputfiles*.png animation.gif

# viewers
gifview - fails
gwenview - works
