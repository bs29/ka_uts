# coding=utf-8

import numpy


class Numpy_:
    """ Manage Numpy Ojects
    """
    @staticmethod
    def write(prof, path_file):
        """ Write profile in numpy format
        """
        numpy.save(path_file, prof)
