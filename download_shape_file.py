import traceback
from pyrosm import OSM
from pyrosm import get_data

try:
  fp = get_data("maryland", update=False, directory='.')
  osm = OSM(fp)
  # Read all drivable roads
  drive_net = osm.get_network(network_type="driving")
  drive_net.to_file("maryland.shp")
  # drive_net.show()
  # print(drive_net)
except:
  print(traceback.format_exc())