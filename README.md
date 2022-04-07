# road_network
extend rpi ram:
sudo dphys-swapfile swapoff
echo 'CONF_SWAPSIZE=2048'|sudo tee /etc/dphys-swapfile
sudo dphys-swapfile swapon