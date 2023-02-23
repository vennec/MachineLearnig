import logging
import math
import sys
import pandas as pd
import random
from transaction import transaction
import locale
from produit import produit
import pymongo

locale.setlocale(locale.LC_ALL, 'fr')

Dbclient = pymongo.MongoClient("mongodb+srv://app:DjTyiqM5GGwLSTSR@foodressources.qmjyzyw.mongodb.net/?retryWrites=true&w=majority&connect=false")

db = Dbclient["FoodRessource"]

products = []

transactions = []

# Params
nbJourGenere = 1300
NbMag = 100
xlsx_file = "output.xlsx"
csv_file = "output.csv"

logging.basicConfig(level = logging.INFO)
     
def DataToexcel(dataf) -> None:
    logging.info('Génération du fichier xlsx')
    dataf.to_excel(xlsx_file)  

def DataToCSV(dataf) -> None:
    logging.info('Génération du CSV')
    dataf.to_csv(csv_file)

def main() -> int:
    logging.info('Génération des dates')
    lDates = pd.date_range(start='1/1/2018', periods=nbJourGenere, freq='D', tz='Europe/Paris').tolist()

    lastId = int(0)
    for i in range(NbMag):
        lastId += 1
        products.append(produit(lastId, 1,'Pattes',1.50,200,i))
        lastId += 1
        products.append(produit(lastId, 2,'Glaces',4,100, i))
        lastId += 1
        products.append(produit(lastId, 3,'Fromage raclette',6.50,100, i))
        lastId += 1
        products.append(produit(lastId, 4,'Bannane',2.5,50, i))

    logging.info('fin de la génération de %s produits', len(products))

    dbShop = db["product"]
    dbShop.insert_many([p.to_dict() for p in products])

    for d in products:
        for i in range(nbJourGenere):
            transactions.append(transaction(lDates[i], d.IdProduct, d.basePrice, d.QuantityTotal, d.IdShop))

    logging.info('fin de la génération de %s dates', len(lDates) * len(products))

    lastQuantity = random.randint(45, 70)
    indexfor = 1
    for t in transactions:
        t.generateQuantity()
        qbuy = t.generateQuantityBuy()
        t.CalcPrice(lastQuantity)
        lastQuantity = qbuy
        t.quantityToCategorie()
        if(indexfor %5 == 0):
            logging.info('génération de %s / %s', indexfor, len(transactions))
        indexfor += 1


    logging.info('Génération du dataframe')
   
    df = pd.DataFrame.from_records([t.to_dict() for t in transactions])
       
    logging.info('Fin de la génération de %s transactions', len(df.index))
    
    dbTransaction = db["transaction"]
    dbTransaction.insert_many([t.to_dict() for t in transactions])

    # DataToexcel(df)
    # DataToCSV(df)
    return 0

if __name__ == '__main__':
    sys.exit(main())