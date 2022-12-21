"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs

    def run(self):
        id_c = self.marketplace.new_cart()
        for cart in self.carts:
            for cmd in cart:
                cmd_type = cmd.get("type")
                product = cmd.get("product")
                quantity = cmd.get("quantity")

                if cmd_type == "add":
                    for i in range(quantity):
                        wait = False
                        while not wait:
                            wait = self.marketplace.add_to_cart(id_c, product)
                            if not wait:
                                time.sleep(self.retry_wait_time)
                elif cmd_type == "remove":
                    for i in range(quantity):
                        self.marketplace.remove_from_cart(id_c, product)

        for prod in self.marketplace.place_order(id_c):
            print(self.name, "bought", prod)
