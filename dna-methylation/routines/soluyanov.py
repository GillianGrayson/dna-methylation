from scipy.stats import norm
import math
import numpy as np

pval = [8.74917961373949e-06, 0.00022421892310087928, 0.3193338878272714, 3.750831681249651e-05] # cg07553761 TRIM59
ni = [656, 729, 2711, 1803]
signs = [-1, +1, -1, +1]
zi = [norm.ppf(x / 2.0) if signs[x_id] > 0 else -norm.ppf(x / 2.0) for x_id, x in enumerate(pval)]
wi = [math.sqrt(x) for x in ni]
z_num = 0.0
z_den = 0.0
for i in range(0, len(pval)):
    z_num += zi[i] * wi[i]
    z_den += wi[i] * wi[i]

z = z_num / math.sqrt(z_den)
p = 2.0 * norm.cdf(-abs(z))
print(p)