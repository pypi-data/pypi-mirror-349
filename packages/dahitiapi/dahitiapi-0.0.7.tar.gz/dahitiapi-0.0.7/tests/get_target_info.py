from dahitiapi.DAHITI import DAHITI

# Initialize Class
dahiti = DAHITI()

dahiti_id=10146

# Get Target Info
ret = dahiti.get_target_info(dahiti_id)

import pprint
pprint.pprint(ret)