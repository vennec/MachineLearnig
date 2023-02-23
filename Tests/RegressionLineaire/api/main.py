from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import joblib

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/train")
def root():

    dbTransaction = app.database["transaction"]

    transactions = []
    for x in dbTransaction.find({"ProductId" : 1, "IdShop" : 0}, {"_id":0,"Date":1,"QuantityBuy":1}):
        transactions.append(x)
    df = pd.DataFrame.from_dict(transactions)

    df.index = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    del df['Date']
    print(df.head())

    train = df[df.index < pd.to_datetime("2021-01-01", format='%Y-%m-%d')]

    y = train['QuantityBuy']

    ARIMAmodel = ARIMA(y, order = (7,0, 6))
    ARIMAmodel = ARIMAmodel.fit()
    joblib.dump(ARIMAmodel, 'arima_model.joblib')

    return {"message": "OK model train"}

@app.get("/predict")
def root():

    model_fit = joblib.load('arima_model.joblib')
    y_pred = model_fit.get_forecast(7)
    y_pred_df = y_pred.conf_int(alpha = 0.05) 
    y_pred_df["Predictions"] = model_fit.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = pd.date_range(start=y_pred_df.index[0], periods=7, freq='D', tz='Europe/Paris').tolist()
    y_pred_out = y_pred_df["Predictions"] 

    return {"message": y_pred_out}