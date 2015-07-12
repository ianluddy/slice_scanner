import abc
from time import time

class Product():
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.vendor = kwargs["vendor"]
        self.name = kwargs["name"]
        self.price = kwargs["price"]
        self.description = kwargs["description"] if kwargs.get("description") else None
        self.img = kwargs.get("img")
        self.quantity = kwargs.get("quantity", 1)

    def to_dict(self):
        if self._valid():
            product_dict = {}
            product_dict["vendor"] = self.vendor
            product_dict["name"] = self.name
            product_dict["price"] = self.price
            product_dict["description"] = self.description
            product_dict["img"] = self.img
            product_dict["stamp"] = time()
            product_dict["hash"] = self._hash()
            product_dict["score"] = self._score()
            return product_dict
        return None

    def _valid(self):
        for required in ["name", "price", "vendor"]:
            if getattr(self, required) is None:
                return False
        return True

    @staticmethod
    def _normalise_data(normaliser, data):

        if data in normaliser:
            return data

        lower_case = data.lower()

        for key, values in normaliser.iteritems():
            for value in values:
                if value in lower_case:
                    return key

        return data

    @abc.abstractmethod
    def _hash(self):
        """ Get product hash """

    @abc.abstractmethod
    def _score(self):
        """ Get product hash """