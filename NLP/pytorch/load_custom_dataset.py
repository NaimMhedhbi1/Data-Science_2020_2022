import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torchtext.legacy import data
TEXT = data.Field(sequential=True, tokenize=tokenize_input, lower=True)
LABEL = data.Field(sequential=False, use_vocab=False)


train,test = data.TabularDataset.splits(
        path='/content/drive/MyDrive/datagram/data/', train='/content/drive/MyDrive/datagram/data/train_datam.csv'
        , test='/content/drive/MyDrive/datagram/data/test_datam.csv', format='csv',
        fields=[('pname', TEXT), ('category_id', LABEL)])
