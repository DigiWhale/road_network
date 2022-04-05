import traceback
from pyrosm import OSM
from pyrosm import get_data
import traceback

# Pyrosm comes with a couple of test datasets 
# that can be used straight away without
# downloading anything
try:
  fp = get_data("maryland", update=False, directory='/home/pi/map_files')

  # Initialize the OSM parser object
  osm = OSM(fp)

  # Read all drivable roads
  # =======================
  drive_net = osm.get_network(network_type="driving")
  print(drive_net)
except:
  print(traceback.format_exc())