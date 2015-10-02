# -*- coding: utf-8 -*-
#!/usr/bin/env python
__author__ = 'vdthoang'

from textblob.blob import TextBlob

string = "what's wrong with the bus"
testimonial = TextBlob(unicode(string, errors='ignore'))
print testimonial.sentiment
print testimonial.polarity