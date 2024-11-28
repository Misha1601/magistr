import numpy as np
import scipy.stats

x=np.array([349.671007, 416.244731, 466.861116, 514.37403, 563.829025, 622.248925, 733.276])
y=np.array([349.927119, 394.1195496, 435.4015628, 472.2445271, 503.7224655, 529.5681266, 550.0669615])

print(np.mean((x - y)**2))
print(np.corrcoef(x, y)[0][1])

print(scipy.stats.pearsonr(x, y)[0])    # Pearson's r
