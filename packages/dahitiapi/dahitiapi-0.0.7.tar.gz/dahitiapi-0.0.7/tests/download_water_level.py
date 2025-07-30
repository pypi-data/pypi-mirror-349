from dahitiapi.DAHITI import DAHITI

# Initialize Class
dahiti = DAHITI()

dahiti_id=10146

# Download Water Level Time Series
ret = dahiti.download_water_level(dahiti_id,format='csv')

import pprint
pprint.pprint(ret)