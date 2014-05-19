"""Journal manipulation"""
from ..oeuo import UO


__author__ = 'Lai Tash'
__email__ = 'lai.tash@gmail.com'
__license__ = "GPL"


class Journal(object):
    def __init__(self, uo=UO):
        self.uo = uo

