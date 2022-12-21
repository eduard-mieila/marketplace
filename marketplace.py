"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from collections import defaultdict
from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        # Date Producatori
        self.prod = defaultdict(list)
        self.prod_lock = Lock()
        self.prod_id = 1
        self.prod_id_lock = Lock()

        # Date Consumatori
        self.cons_id = 1
        self.cons_id_lock = Lock()

        # Date Cosuri
        self.carts = {}
        self.carts_lock = Lock()
        self.carts_max_cap = queue_size_per_producer


    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        # Incrementam counter-ul pentru id-ul producatorilor safe
        self.prod_id_lock.acquire()
        self.prod_id += 1
        self.prod_id_lock.release()

        return self.prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # Deoarece vom modifica detalii despre producatori, vom bloca dictionarul acestora
        self.prod_lock.acquire()

        # Extragem lista de produse a producatorului
        product_list = self.prod.get(producer_id)

        dim = 0
        if product_list is not None:
            for elem in product_list:
                dim = len(product_list)
        else:
            product_list = []

        if dim < self.carts_max_cap:
            # Daca nu s-a atins capacitatea maxima, adaugam produsul, eliberam lock-ul si
            # returnam True
            if dim != 0:
                self.prod.get(producer_id).append(product)
            else:
                self.prod[producer_id] = [product]
            self.prod_lock.release()
            return True

        # Daca s-a atins capacitatea maxima, eliberam lock-ul si returnam False
        self.prod_lock.release()
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # Incrementam counter-ul pentru id-ul consumatorilor safe
        self.cons_id_lock.acquire()
        self.cons_id += 1
        self.cons_id_lock.release()
        return self.cons_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """


        producer_index = -1

        # Vom cauta un producator care are acest produs, asadar vom itera prin dictionarul
        # de producatori(vom marca acest lucru, blocand lock-ul corespunazator)
        self.prod_lock.acquire()
        for prod_id, prod_list in self.prod.items():
            for prod in prod_list:
                if product == prod:
                    # Daca am gasit acest produs, stim care producator il are
                    producer_index = prod_id
                    break

        if producer_index == -1:
            # Nu am gasit niciun producator care sa aiba acest produs, asadar eliberam
            # lock-ul blocat si intoarcem rezultatul
            self.prod_lock.release()
            return False

        # Vom modifica dictionarul cu cosurile de cumparaturi, asadar blocam lock-ul
        # corespunzator
        self.carts_lock.acquire()
        cart = self.carts.get(cart_id)
        if cart is not None:
            self.carts.get(cart_id).append([producer_index, product])
        else:
            self.carts[cart_id] = [[producer_index, product]]

        self.prod.get(producer_index).remove(product)
        # eliberam lock-urile
        self.prod_lock.release()
        self.carts_lock.release()
        return True



    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.carts_lock.acquire()

        producer_index = -1

        # Cautam produsul dorit in cosul corespunzator
        cart = self.carts.get(cart_id)
        for prod in cart:
            if product == prod[1]:
                producer_index = prod[0]
                break

        if producer_index == -1:
            # Daca nu am gasit produsul in cosul dorit, eliberm lock-ul si abandonam
            self.carts_lock.release()
            return

        # Stergem produssul din cos
        cart.remove([producer_index, product])

        # Vom efectua modificari asupra stocurilor producatorilor, asa ca vom
        # bloca lock-ul acestora
        self.prod_lock.acquire()
        self.prod.get(producer_index).append(product)

        # Eliberam lock-urile
        self.prod_lock.release()
        self.carts_lock.release()


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        # Pentru a ne asigura ca intre timp nu se mai dauaga produse in cos, vom bloca
        # dictionarul de cosuri
        self.carts_lock.acquire()

        ret_list = []
        for prod in self.carts.get(cart_id):
            ret_list.append(prod[1])

        # Deblocam lock-ul
        self.carts_lock.release()

        return ret_list
