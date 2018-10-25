import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Classes.mongoDB import mongoDB
from scipy.stats import skewnorm
from scipy.stats import norm

# change default directory in the graph viewer
plt.rcParams["savefig.directory"] = "~/Project/Report/Results"

a = -10
# skewset = skewnorm.rvs(a, size=1000)
sns.set()
sns.set_style('darkgrid')
sns.despine()
np.random.seed(5366)

db = mongoDB('field_collection_170918')

sample = db.findByQuery({"location": "B1"}).next()
count = 0

if False:
    for cell_sample in sample["primary_print"]:
        if cell_sample != '0000' and cell_sample != 'ffff':
            normset = np.random.normal(
                sample["primary_print"][cell_sample], 1, 1000)
            sns.distplot(normset, hist=True, kde=False, rug=False,
                         label=cell_sample, bins='sqrt',
                         hist_kws={'alpha': 0.9})
            plt.legend()
            count += 1

if False:
    for cell_sample in sample["fingerprint_set"]:
        if cell_sample != '0000' and cell_sample != 'ffff':
            if len(sample["fingerprint_set"][cell_sample]) > 35:
                realset = sample["fingerprint_set"][cell_sample]
                sns.distplot(realset, fit=norm,
                             label=cell_sample,
                             hist=True, rug=False, kde=False)
                plt.legend()

plt.title('Histogram of a typical fingerprint')
plt.xlabel('Signal Strength')
plt.ylabel('Frequency')
plt.show()

# plt.hist(normset)
# plt.title("Gaussian Histogram")
# plt.xlabel("Value")
# plt.ylabel("Frequency")