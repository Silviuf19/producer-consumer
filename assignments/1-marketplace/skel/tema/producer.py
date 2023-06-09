"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.producer_id = marketplace.register_producer()
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.products = products
        Thread.__init__(self, **kwargs)

    def run(self):
        while True:
            for product_props in self.products:
                [product, num_of_products, time_to_wait] = product_props
                index = 0
                while index < num_of_products:
                    # print("index: " + str(index), flush=True)
                    if not self.marketplace.publish(str(self.producer_id), product):
                        time.sleep(self.republish_wait_time)
                        index -= 1
                    else:
                        time.sleep(time_to_wait)
                    index += 1
