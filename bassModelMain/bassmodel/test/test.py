from BassOLS import *
model = BassOLS('../utils/data.csv')
model.fit()
model.predict()
model.plot()
model.summarize()
