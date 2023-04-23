"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


import uuid
import time
import logging
import unittest
import threading
from logging import handlers
from tema.product import Tea, Coffee

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

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.formatter.converter = time.gmtime
        self.handler = handlers.RotatingFileHandler("marketplace.log",
                                                    maxBytes=60000, backupCount=5)
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger('marketplace.log')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.logger.info("Producer started to register")
        producer_id = str(uuid.uuid4())
        self.producer_queue_size[producer_id] = 0
        self.lock_modify_sizes[producer_id] = threading.Lock()
        self.logger.info("Producer registered")
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
        self.logger.info("Producer %s started to publish product %s", producer_id, product.name)
        if self.producer_queue_size[producer_id] >= self.queue_size_per_producer:
            self.logger.warning("Producer %s has its queue full", producer_id)
            return False

        if product.name not in self.product_pool:
            self.product_pool[product.name] =(product, [producer_id])
        else:
            self.product_pool[product.name][1].append(producer_id)
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
            self.logger.info("Producer %s published product %s", producer_id, product.name)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.logger.info("Consumer started to create a new cart")
        cart_id = int(uuid.uuid4())
        self.cart_list[cart_id] = {}
        self.logger.info("Consumer created a new cart")
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
        self.logger.info("Consumer started to add product %s to cart %s", product.name, cart_id)
        if product.name not in self.product_pool or len(self.product_pool[product.name][1]) == 0:
            self.logger.warning("Product %s is not in the marketplace", product.name)
            return False

        producer_id = self.product_pool[product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] -= 1

        if product.name not in self.cart_list[cart_id]:
            self.cart_list[cart_id][product.name] = (product, [producer_id])
        else:
            self.cart_list[cart_id][product.name][1].append(producer_id)
        self.logger.info("Consumer added product %s to cart %s", product.name, cart_id)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.logger.info("Consumer started to remove product %s from cart %s",
                        product.name, cart_id)
        producer_id = self.cart_list[cart_id][product.name][1].pop()
        with self.lock_modify_sizes[producer_id]:
            self.producer_queue_size[producer_id] += 1
        self.product_pool[product.name][1].append(producer_id)
        self.logger.info("Consumer removed product %s from cart %s", product.name, cart_id)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Consumer started to place order for cart %s", cart_id)
        cart_products = []
        for (_,(product_cart, producer_id_list)) in self.cart_list[cart_id].items():
            for _ in producer_id_list:
                cart_products.append(product_cart)
        self.logger.info("Consumer placed order for cart %s", cart_id)
        return cart_products

class TestMarketplace(unittest.TestCase):
    """
    Test class for Marketplace

    Args:
        unittest (TestCase): TestCase class from unittest
    """
    def setUp(self):
        """
        Initial setup
        """
        self.marketplace = Marketplace(3)
        self.cofee = Coffee("Cappucino", 10, "medium", "burned")
        self.tea = Tea("Earl Grey", 5, "black")

    def test_register_producer(self):
        """
        Test registering a producer
        """
        producer_id = self.marketplace.register_producer()
        self.assertIsNotNone(producer_id)

    def test_register_producer_unique_id(self):
        """
        Test that the producer id is unique
        """
        producer_id1 = self.marketplace.register_producer()
        producer_id2 = self.marketplace.register_producer()
        self.assertNotEqual(producer_id1, producer_id2)

    def test_publish(self):
        """
        Test publishing
        """
        producer_id = self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish(producer_id, self.cofee))

    def test_publish_full_queue(self):
        """
        Test publishing with a full queue
        """
        producer_id = self.marketplace.register_producer()
        self.assertTrue(self.marketplace.publish(producer_id, self.cofee))
        self.assertTrue(self.marketplace.publish(producer_id, self.tea))
        self.assertTrue(self.marketplace.publish(producer_id, self.cofee))
        self.assertFalse(self.marketplace.publish(producer_id, self.tea))

    def test_new_cart(self):
        """
        Test new cart
        """
        cart_id = self.marketplace.new_cart()
        self.assertIsNotNone(cart_id)

    def test_new_cart_unique_id(self):
        """
        Test new cart unique id
        """
        cart_id1 = self.marketplace.new_cart()
        cart_id2 = self.marketplace.new_cart()
        self.assertNotEqual(cart_id1, cart_id2)

    def test_add_to_cart(self):
        """
        Test add to cart a product that is in marketplace
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, self.cofee)
        cart_id = self.marketplace.new_cart()
        self.assertTrue(self.marketplace.add_to_cart(cart_id, self.cofee))

    def test_add_to_cart_not_in_marketplace(self):
        """
        Test add to cart a product that is not in marketplace
        """
        cart_id = self.marketplace.new_cart()
        self.assertFalse(self.marketplace.add_to_cart(cart_id, self.cofee))

    def test_remove_from_cart(self):
        """
        Test remove one element from cart
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, self.cofee)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, self.cofee)
        self.marketplace.remove_from_cart(cart_id, self.cofee)
        self.assertEqual(self.marketplace.cart_list[cart_id][self.cofee.name][1], [])

    def test_place_order(self):
        """
        Test place order
        """
        producer_id = self.marketplace.register_producer()
        self.marketplace.publish(producer_id, self.cofee)
        cart_id = self.marketplace.new_cart()
        self.marketplace.add_to_cart(cart_id, self.cofee)
        self.assertEqual(self.marketplace.place_order(cart_id), [self.cofee])

if __name__ == '__main__':
    unittest.main()
