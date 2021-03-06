__author__ = 'vdthoang'

from string import letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="white")

# Generate a large random dataset
rs = np.random.RandomState(33)
d = pd.DataFrame(data=rs.normal(size=(100, 26)),
                 columns=list(letters[:26]))

# Compute the correlation matrix
corr = d.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
            square=True, xticklabels=5, yticklabels=5,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)


plt.show()

# import matplotlib.pyplot as plt
# import pylab
#
# x = [1,2,3,4]
# y = [3,4,8,6]
#
# plt.scatter(x,y)
# plt.show()
#
# f, ax = plt.subplots(figsize=(11, 9))
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
#
# sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
#             square=True, xticklabels=5, yticklabels=5,
#             linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)
#
# plt.show()
