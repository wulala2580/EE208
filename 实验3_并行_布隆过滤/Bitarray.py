import math


# -*- coding: utf8 -*-
class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(math.ceil(size / 8.))

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = int(n / 8)
        position = int(n % 8)
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index = int(n / 8)
        position = int(n % 8)
        return (self.bitarray[index] & (1 << (7 - position))) > 0


