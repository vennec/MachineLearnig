import random
import array
import numpy as np
import pandas as pd

dates = pd.date_range(start='1/1/2018', periods=20, freq='D').tolist()

for i in range(20):
    print(dates[i])
