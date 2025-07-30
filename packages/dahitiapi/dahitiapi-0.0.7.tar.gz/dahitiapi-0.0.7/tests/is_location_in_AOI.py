from dahitiapi.DAHITI import DAHITI

# Initialize Class
dahiti = DAHITI()

args = {}
args['longitude'] = 1.0
args['latitude'] = 49.0

# Is location in AOI
ret = dahiti.is_location_in_AOI(args)

import pprint
pprint.pprint(ret)