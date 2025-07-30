import unittest
import os
import sys

from pytest import raises

from daltools import mol
from . import tmpdir


class TestMol:

    def setup_method(self):
        dalton_bas = tmpdir(__file__)/"DALTON.BAS"
        self.bas = mol.readin(dalton_bas)
        self.maxDiff = None

    def test_pass(self):
        """
        Contains atom Z=37, which is not implemented
        """
        with raises(NotImplementedError):
            mol.occupied_per_atom(self.bas)
