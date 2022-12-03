import pandas as pd
from sdv.tabular import GaussianCopula
import os

def get_data(data_number, use_default_dataset, use_default_syntetic_dataset):
    data_file = ''
    if use_default_dataset:
        data_file = 'default_data.csv'
        return pd.read_csv(os.path.join(os.getcwd(),'data',data_file))
    elif use_default_syntetic_dataset:
        data_file = 'syntethic_data_'+str(data_number)+'.csv'
        return pd.read_csv(os.path.join(os.getcwd(),'data',data_file))
    data_file = 'syntethic_data_random.csv'
    data = pd.read_csv(os.path.join(os.getcwd(),'data','default_data.csv'))
    data.head()
    model = GaussianCopula()
    model.fit(data)
    sample = model.sample(data_number)
    sample.to_csv(os.path.join(os.getcwd(),'data',data_file), header=True, sep=',', index=False)
    sample.head()
    return pd.read_csv(os.path.join(os.getcwd(),'data',data_file))
