class Client(object):
    def __init__(self, nom, ville):
        self.nom = nom
        self.ville = ville


class Prod(object):
    def __init__(self, nom, prix, quant):
        self.nom = nom
        self.prix = prix
        self.quant = quant