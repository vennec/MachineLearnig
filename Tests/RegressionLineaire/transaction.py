import math
import random
import pandas as pd

class transaction:
    def __init__(self, Date : pd.DatetimeIndex, ProductId = 0, ProductBasePrice = 0, QuantitySOD = 100,IdShop = 1, QuantityEOD = 0, Price = 0, QuantityBuy = 0, QuantityEchelone = 0, QuantityEcheloneLibelle = ''):
        self.Date = Date
        self.QuantityEOD = QuantityEOD
        self.QuantitySOD = QuantitySOD
        self.Price = Price
        self.ProductBasePrice = ProductBasePrice
        self.ProductId = ProductId
        self.QuantityBuy = QuantityBuy
        self.QuantityEchelone = QuantityEchelone
        self.QuantityEcheloneLibelle = QuantityEcheloneLibelle
        self.IdShop = IdShop
    
    def to_dict(self):
        return {
            'Date': self.Date.strftime('%d-%m-%Y'),
            'QuantityEOD': self.QuantityEOD,
            'QuantitySOD': self.QuantitySOD,
            'Price': self.Price,
            'ProductId': self.ProductId,
            'QuantityBuy': self.QuantityBuy,
            'QuantityEchelone': self.QuantityEchelone,
            'QuantityEcheloneLibelle': self.QuantityEcheloneLibelle,
            "IdShop" : self.IdShop
        }
    
    def generateQuantity(self):
        match self.Date.day_name(locale ='French'):
            case 'Lundi':
                self.QuantityEOD = random.randint(40, 70)
            case 'Mardi':
                self.QuantityEOD = random.randint(40, 70)
            case 'Mercredi':
                self.QuantityEOD = random.randint(30, 60)
            case 'Jeudi':
                self.QuantityEOD = random.randint(40, 70)
            case 'Vendredi':
                self.QuantityEOD = random.randint(40, 70)
            case 'Samedi':
                self.QuantityEOD = random.randint(10, 40)
            case 'Dimanche':
                self.QuantityEOD = random.randint(40, 70)

    def generateQuantityBuy(self):
        self.QuantityBuy = self.QuantitySOD - self.QuantityEOD
        return self.QuantityBuy
    
    def CalcPrice(self, lastQuantity):
        augmentation = (((lastQuantity * 20)/100)/100)+1
        self.Price = self.ProductBasePrice*augmentation
    
    def quantityToCategorie(self):
        self.QuantityEchelone = math.floor((self.QuantityEOD * 4)/100)
        match self.QuantityEchelone:
            case 0:
                self.QuantityEcheloneLibelle = 'Tres bas'
            case 1:
                self.QuantityEcheloneLibelle = 'Bas'
            case 2:
                self.QuantityEcheloneLibelle = 'Moyen'
            case 3:
                self.QuantityEcheloneLibelle = 'Haut'
            case 4:
                self.QuantityEcheloneLibelle = 'Tres haut'