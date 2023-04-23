"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


import uuid
import threading

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        self.queue_size_per_producer = queue_size_per_producer
        self.product_pool = {}
        self.producer_queue_size = {}
        self.cart_list = {}
        self.lock_modify_sizes = {}
        self.lock_print = threading.Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = str(uuid.uuid4())
        self.producer_queue_size[producer_id] = 0
        self.lock_modify_sizes[producer_id] = threading.Lock()
        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if self.producer_queue_size[producer_id] >= self.queue_size_per_producer:
            return False

        if product.name not in self.product_pool:
            self.product_pool[product.name] =(product, [producer_id])
        else:
            self.product_pool[product.name][1].append(producer_id)
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        cart_id = int(uuid.uuid4())
        self.cart_list[cart_id] = {}
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        if product.name not in self.product_pool:
            return False

        if len(self.product_pool[product.name][1]) == 0:
            return False

        producer_id = self.product_pool[product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] -= 1

        if product.name not in self.cart_list[cart_id]:
            self.cart_list[cart_id][product.name] = (product, [producer_id])
        else:
            self.cart_list[cart_id][product.name][1].append(producer_id)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        producer_id = self.cart_list[cart_id][product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
        self.product_pool[product.name][1].append(producer_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        cart_products = []
        for (_,(product_cart, producer_id_list)) in self.cart_list[cart_id].items():
            for _ in producer_id_list:
                cart_products.append(product_cart)
        return cart_products
