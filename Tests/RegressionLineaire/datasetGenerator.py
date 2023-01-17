import logging
import math
import sys
import pandas as pd
import random
from transaction import transaction

class produit:
    def __init__(self, productCB, name, basePrice):
        self.productCB = productCB
        self.name = name
        self.basePrice = basePrice

products = []

products.append(produit(1,'Pattes',1.50))
products.append(produit(2,'Glaces',4))
products.append(produit(3,'Fromage raclette',6.50))

transactions = []

# Params
nbJourGenere = 364
xlsx_file = "output.xlsx"
QuantityTotal = 100
dict_data = {'Date' : [], 'QuantityEOD':  [],'QuantitySOD': QuantityTotal, 'Price' : [], 'Lat' : 0, 'Long': 0, 'ProductId': [], 'QuantityBuy': [],'QuantityEchelone': []} 

logging.basicConfig(level = logging.INFO)


# def generateDate() -> pd.DatetimeIndex:
#     logging.info('Génération des dates')
#     dates = pd.date_range(start='1/1/2018', periods=nbJourGenere, freq='D').tolist()
    
#     dict_data['Date'] += dates
    
#     logging.info('Génération de %s dates', len(dates))
#     return dates

# def generateQuantity() -> list:
#     logging.info('Génération des quantitées')
#     qTotal = []
#     for i in range(int(nbJourGenere/7)):
#         qTotal += [random.randint(45, 70),random.randint(45, 70),random.randint(30, 60),random.randint(45, 70),random.randint(45, 70),random.randint(10, 40),random.randint(45, 70)]
#     dict_data['QuantityEOD'] += qTotal
#     logging.info('Fin de la génération de %s quantitées', len(qTotal))
#     return qTotal  

# def DataToexcel(dataf) -> None:
#     logging.info('Génération du fichier xlsx')
#     dataf.to_excel(xlsx_file)  

# def CalcQuantityBuy(quantityEOD) -> list:
#     logging.info('Calcule des quatitées achetées')
#     data = []
#     for i in quantityEOD:
#         data.append(QuantityTotal - i)

#     dict_data['QuantityBuy'] += data
#     logging.info('Fin de la génération de %s quatitées achetées', len(data))
#     return data

# def CalcPrice(QuantityBuy, basePrice) -> list:
#     logging.info('Calcule des prix')
#     data = []
#     lastQuantity = random.randint(45, 70)
#     for i in QuantityBuy:
#         augmentation = (((lastQuantity * 20)/100)/100)+1
#         data.append(basePrice*augmentation)
#         lastQuantity = i
#     dict_data['Price'] += data

# def addProductId(productId) -> None:
#     logging.info('Ajout des id produit')
#     for i in range(nbJourGenere):
#         if "ProductId" in dict_data:
#             dict_data['ProductId'].append(productId)
   
# def quantityToCategorie() -> None: 
#     logging.info('Mise a la bonne echele des quantitées')
#     for i in dict_data['QuantityEOD']:
#         q = math.floor((i * 3)/100)
#         match q:
#             case 0:
#                 dict_data['QuantityEchelone'] += ['Tres bas']
#             case 1:
#                 dict_data['QuantityEchelone'] += ['bas']
#             case 2:
#                 dict_data['QuantityEchelone'] += ['moyen']
#             case 3:
#                 dict_data['QuantityEchelone'] += ['haut']
     
     
def DataToexcel(dataf) -> None:
    logging.info('Génération du fichier xlsx')
    dataf.to_excel(xlsx_file)  
     
    
def main() -> int:

    lDates = pd.date_range(start='1/1/2018', periods=nbJourGenere, freq='D').tolist()

    for d in products:
        for i in range(nbJourGenere):
            transactions.append(transaction(lDates[i], d.productCB))



    # for obj in products:
    #     generateDate()
    #     quantityEOD = generateQuantity()
    #     QuantityBuy = CalcQuantityBuy(quantityEOD)
    #     CalcPrice(QuantityBuy, obj.basePrice)
    #     addProductId(obj.productCB)
    
    # quantityToCategorie()
    
    logging.info('Génération du dataframe')
   
    df = pd.DataFrame.from_records([t.to_dict() for t in transactions])
   
    # df = pd.DataFrame(transactions)
    
    logging.info('Fin de la génération de %s transaction', len(df.index))
    
    DataToexcel(df)
    return 0

if __name__ == '__main__':
    sys.exit(main())