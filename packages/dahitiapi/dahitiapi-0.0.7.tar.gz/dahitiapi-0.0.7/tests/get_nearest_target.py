from dahitiapi.DAHITI import DAHITI

# Initialize Class
dahiti = DAHITI()

longitude = 11.0
latitude = 49.0

# Get Nearest Target
ret = dahiti.get_nearest_target(longitude,latitude)

import pprint
pprint.pprint(ret)