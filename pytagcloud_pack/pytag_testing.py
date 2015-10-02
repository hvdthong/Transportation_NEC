__author__ = 'vdthoang'
from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts
from pytagcloud import LAYOUT_MIX, LAYOUTS, LAYOUT_HORIZONTAL, LAYOUT_MOST_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES

# TEXT = 'Bunch Jam Crowd/Squeeze Delay/Slow Kill/Dead Breakdown Aircon Accident'
# TEXT = 'Bunch Jam Crowd Delay Dead Breakdown Aircon Accident'
# counts = get_tag_counts(TEXT)
# tags = make_tags(counts, maxsize=175, colors=COLOR_SCHEMES['audacity'])
# create_tag_image(tags, 'cloud_event.png', size=(900, 600), background=(0, 0, 0, 255), fontname='Molengo', layout=LAYOUT_HORIZONTAL, rectangular=True)
#
# import webbrowser
# webbrowser.open('cloud_event.png') # see results

TEXT = '960 960 960 176 176 176 962 962 300'
counts = get_tag_counts(TEXT)
tags = make_tags(counts, maxsize=25, colors=COLOR_SCHEMES['audacity'])
create_tag_image(tags, 'cloud_num.png', size=(900, 600), background=(0, 0, 0, 0), fontname='Lobster', layout=LAYOUT_MIX, rectangular=True)

import webbrowser
webbrowser.open('cloud_num.png') # see results




