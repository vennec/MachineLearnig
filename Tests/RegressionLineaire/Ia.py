import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model

df = pd.read_excel('C:/Users/venne/Documents/Dev/MachineLearnig/output.xlsx')
print(df.head())

x = df [['QuantityEOD', 'QuantitySOD','Price','QuantityBuy']]
y = df['QuantityEchelone']
#fractionner dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 0)
#instanciation du modèle
modele_regLog = linear_model.LogisticRegression(random_state = 0,
solver = 'liblinear', multi_class = 'auto')
#training
modele_regLog.fit(x_train,y_train)
#précision du modèle
precision = modele_regLog.score(x_test,y_test)
print(precision*100)

#prédiction
prediction_fruit = modele_regLog.predict([[90,100,1.50,10]])
print(prediction_fruit)