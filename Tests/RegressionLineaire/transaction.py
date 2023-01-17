import pandas as pd
class transaction:
    def __init__(self, Date : pd.DatetimeIndex, ProductId = 0, QuantitySOD = 100, QuantityEOD = 0, Price = 0, QuantityBuy = 0, QuantityEchelone = 0, Lat = 0, Long = 0):
        self.Date = Date.strftime('%d-%m-%Y')
        self.QuantityEOD = QuantityEOD
        self.QuantitySOD = QuantitySOD
        self.Price = Price
        self.Lat = Lat
        self.Long = Long
        self.ProductId = ProductId
        self.QuantityBuy = QuantityBuy
        self.QuantityEchelone = QuantityEchelone
    
    def to_dict(self):
        return {
            'Date': self.Date,
            'QuantityEOD': self.QuantityEOD,
            'QuantitySOD': self.QuantitySOD,
            'Price': self.Price,
            'Lat': self.Lat,
            'Long': self.Long,
            'ProductId': self.ProductId,
            'QuantityBuy': self.QuantityBuy,
            'QuantityEchelone': self.QuantityEchelone,
        }