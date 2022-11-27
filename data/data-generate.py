import pandas as pd
from sdv.tabular import GaussianCopula

data = pd.read_csv('./data.csv')
data.head()
model = GaussianCopula()
model.fit(data)
sample = model.sample(200)
sample.to_csv('syntethic_data.csv', header=True, sep=',', index=False)
sample.head()
