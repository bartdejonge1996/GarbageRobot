lan="$(ip addr show wlo1 | grep '\<inet\>' | tr -s ' ' | cut -d ' ' -f3)"
lan="${lan%/*}"
export ROS_IP=${lan}
export ROS_MASTER_URI=http://rpi:11311
