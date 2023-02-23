import pandas as pd
class produit:
    def __init__(self, IdProduct, productCB, name, basePrice, QuantityTotal, IdShop):
        self.IdProduct = IdProduct
        self.productCB = productCB
        self.name = name
        self.basePrice = basePrice
        self.QuantityTotal = QuantityTotal
        self.IdShop = IdShop

    def to_dict(self):
        return {
            "IdProduct" : self.IdProduct,
            "codeBarre" : self.productCB,
            "name" : self.name,
            "basePrice" : self.basePrice,
            "QuantityBase" : self.QuantityTotal,
            "IdShop" : self.IdShop,
        }