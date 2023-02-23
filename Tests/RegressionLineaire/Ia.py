import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import VisualizeNN as VisNN
from transaction import transaction
from produit import produit
import pymongo
import locale
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
import itertools
from sklearn.metrics import mean_squared_error

locale.setlocale(locale.LC_ALL, 'fr')

Dbclient = pymongo.MongoClient("mongodb+srv://app:DjTyiqM5GGwLSTSR@foodressources.qmjyzyw.mongodb.net/?retryWrites=true&w=majority&connect=false")

db = Dbclient["FoodRessource"]

dbTransaction = db["transaction"]

transactions = []
for x in dbTransaction.find({"ProductId" : 1, "IdShop" : 0}, {"_id":0,"Date":1,"QuantityBuy":1}):
    transactions.append(x)
df = pd.DataFrame.from_dict(transactions)
# serie = df.squeeze()
# serie['Date']= pd.to_date(serie['Date'], format='%d-%m-%Y')

# serie.plot(x="Date", y="QuantityBuy", figsize=(14,4))

df.index = pd.to_datetime(df['Date'], format='%d-%m-%Y')
del df['Date']
print(df.head())
# arma = ARIMA(serie, order=(1,0,3)).fit()
# arma.summary()
sns.set()

# plt.ylabel('QuantityBuy')
# plt.xlabel('Date')
# plt.xticks(rotation=45)

# plt.plot(df.index, df['QuantityBuy'])
# plt.show()

train = df[df.index < pd.to_datetime("2021-01-01", format='%Y-%m-%d')]
test = df[df.index > pd.to_datetime("2021-01-01", format='%Y-%m-%d')]



y = train['QuantityBuy']

# p = d = q = range(0, 2)
# pdq = list(itertools.product(p, d, q))
# seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

# for param in pdq:
#     for param_seasonal in seasonal_pdq:
#         try:
#             mod = SARIMAX(y,order=param,seasonal_order=param_seasonal,enforce_stationarity=False,enforce_invertibility=False)
#             results = mod.fit()
#             print('ARIMA{}x{}12 - AIC:{}'.format(param,param_seasonal,results.aic))
#         except: 
#             continue

ARIMAmodel = ARIMA(y, order = (7,0, 6))
ARIMAmodel = ARIMAmodel.fit()
ARIMAmodel.save('model.pkl')

y_pred = ARIMAmodel.get_forecast(len(test.index))
y_pred_df = y_pred.conf_int(alpha = 0.05) 
y_pred_df["Predictions"] = ARIMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
y_pred_df.index = test.index
y_pred_out = y_pred_df["Predictions"] 


plt.plot(train, color = "black")
plt.plot(test, color = "red")
plt.ylabel('QuantityBuy')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.title("Train/Test split for BTC Data")

arma_rmse = np.sqrt(mean_squared_error(test["QuantityBuy"].values, y_pred_df["Predictions"]))
print("RMSE: ",arma_rmse)

plt.plot(y_pred_out, color='Blue', label = 'SARIMA Predictions')
plt.legend()
plt.show()
