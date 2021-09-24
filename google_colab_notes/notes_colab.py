#access to the driver 
from google.colab import drive
drive.mount('/content/drive',force_remount = True) 

import pandas as pd
import numpy as np
import os
#read the data
df = pd.read_csv('/content/drive/MyDrive/datagram/train_data.csv')