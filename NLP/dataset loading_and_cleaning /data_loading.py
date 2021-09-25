#save files from colab to google driver
import pandas as pd
train_df = pd.read_csv('/content/drive/MyDrive/datagram/data/train_df.csv')
test_df = pd.read_csv('/content/drive/MyDrive/datagram/data/test_df.csv')

train_df['category_id'] = train_df['category_id'].astype(int) 
test_df['category_id'] = test_df['category_id'].astype(int)  

train_df['pname'] = train_df['pname'].astype(str) 
test_df['pname'] = test_df['pname'].astype(str)  

train_df = train_df.groupby('category_id').filter(lambda x : (x['category_id'].count()>=1).any())
test_df = test_df.groupby('category_id').filter(lambda x : (x['category_id'].count()>=1).any())


train_df.to_csv('train_datam.csv')
!cp train_datam.csv "/content/drive/MyDrive/datagram/data/"

test_df.to_csv('test_datam.csv')
!cp test_datam.csv "/content/drive/MyDrive/datagram/data/"