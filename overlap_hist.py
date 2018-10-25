import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Classes.mongoDB import mongoDB
from scipy.stats import skewnorm
from scipy.stats import norm
np.random.seed(5366)
plt.rcParams["savefig.directory"] = "~/Project/Report/Results"
sns.set()
sns.set_style('darkgrid')
sns.despine()

data = []
tower = []
db = mongoDB('field_collection_170918')

sample = db.findByQuery({"location": "B34"}).next()
for cell in sample["fingerprint_set"]:
    if len(sample["fingerprint_set"][cell]) > 30:
            for el  in sample["fingerprint_set"][cell]:
                    data.append(el)
                    tower.append(cell)

# for cell in sample["primary_print"]:
#         if len(sample["fingerprint_set"][cell]) > 30:
#                 normset = np.random.normal(sample["primary_print"][cell],1.3,250)
#                 for el in normset:
#                         data.append(el)
#                         tower.append(cell)

df = pd.DataFrame(dict(x=data,g=tower))


sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Create the data
# rs = np.random.RandomState(1979)
# x = rs.randn(500)
# g = np.tile(list("ABCDEFGHIJ"), 50)
# df = pd.DataFrame(dict(x=x, g=g))
# m = df.g.map(ord)
# df["x"] += m

df = df.sort_values('g')

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(10, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x", clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()


    # change labels here.
    if label == 'f565':
            label = 'f564/VL'
    if label == 'f58d':
            label = 'f58d/CL'
    ax.text(0, .2, 'ID: '+label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "x")

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set_xlabels("Signal Strength")
g.set(yticks=[])
g.despine(bottom=True, left=True)

plt.show()


