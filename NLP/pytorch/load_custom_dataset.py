import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchtext.legacy import data


import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchtext.legacy import data

train_data,test_data = data.TabularDataset.splits(
        path='/content/drive/MyDrive/datagram/data/', train='/content/drive/MyDrive/datagram/data/train_datam.csv'
        , test='/content/drive/MyDrive/datagram/data/test_datam.csv', format='csv',
        fields=[('pname', TEXT), ('category_id', LABEL)])

#loading datsets
train_data, valid_data=train_data.split(random_state=random.seed(999),split_ratio=0.8)
device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
train_iter, valid_iter, test_iter = data.BucketIterator.splits((train_data, valid_data, test_data),batch_size = 64,device = device)
