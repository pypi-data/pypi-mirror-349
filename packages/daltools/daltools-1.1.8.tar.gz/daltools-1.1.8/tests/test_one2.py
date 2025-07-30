import unittest
import unittest.mock as mock
import sys

import numpy as np
from pytest import approx, raises

from daltools import one
from . import tmpdir


class TestOne:
    def setup_method(self):
        self.tmpdir = tmpdir(__file__)
        self.aooneint = self.tmpdir/"AOONEINT"
        self.aoproper = self.tmpdir/"AOPROPER"
        self.header = one.readhead(self.aooneint)
        self.maxDiff = None

    def test_header_title(self):
        assert "=" in self.header["ttitle"]

    def test_header_naos(self):
        assert self.header["naos"] == (7,)

    def test_header_nsym(self):
        assert self.header["nsym"] == 1

    def test_header_potnuc(self):
        assert self.header["potnuc"] == approx(9.343638157971)

    def test_isordk_nucdep(self):
        isordk = one.readisordk(self.aooneint)
        assert isordk["nucdep"] == 3

    def test_isordk_chrn(self):
        isordk = one.readisordk(self.aooneint)
        assert isordk["chrn"][:3] == (8.0, 1.0, 1.0)

    def test_isordk_cooo(self):
        isordk = one.readisordk(self.aooneint)
        cooo = isordk["cooo"]
        nucdep = isordk["nucdep"]
        mxcent = len(cooo) // nucdep
        np.testing.assert_almost_equal(cooo[0::mxcent], [0., 0., 0.])
        np.testing.assert_almost_equal(cooo[1::mxcent], [0, 1.4, 1.1])
        np.testing.assert_almost_equal(cooo[2::mxcent], [0, -1.4, 1.1])

    def test_scfinp(self):
        scfinp = one.readscfinp(self.aooneint)
        assert scfinp["nsym"] == 1
        coor_bohr = (
            0, 0, 0, 0, 1.4, 1.1, 0, -1.4, 1.1
        )
        np.testing.assert_almost_equal(scfinp["cooo"], coor_bohr)

    def test_overlap(self):
        Sref = np.loadtxt('tests/test_one2.d/ov.txt')

        S = one.read("OVERLAP", self.aooneint)
        np.testing.assert_almost_equal(np.array(S.subblock[0]), Sref)

    def test_main(self):
        sys.argv[1:] = [str(self.aooneint)]
        with mock.patch("daltools.one.print") as mock_print:
            one.main()
        mock_print.assert_not_called()

    def test_main_head(self, capsys):
        sys.argv[1:] = [str(self.aooneint), "--head"]
        ref_output = """\
Header on AOONEINT
ttitle                                                                                                                                                                                                         ====================================                                                                                                                                                                    
nsym 1
naos (7,)
potnuc    9.34364
int_fmt i
float_fmt d
"""

        one.main()
        # mock_print.assert_called_once_with(ref_output)
        captured = capsys.readouterr()
        assert ref_output == captured.out

    def test_main_isordk(self):
        sys.argv[1:] = [str(self.aooneint), "--isordk"]
        ref_output = """\
nucdep=3 mxcent=500

 (3,)
              Column   1
       1      8.00000000
       2      1.00000000
       3      1.00000000


 (3, 3)
              Column   1    Column   2    Column   3
       2      0.00000000    1.40000000   -1.40000000
       3      0.00000000    1.10000000    1.10000000
"""



        with mock.patch("daltools.one.print") as mock_print:
            one.main()
        calls = [mock.call(s) for s in ref_output.split("\n")]
        mock_print.assert_has_calls([])

    def test_main_scfinp(self, capsys):
        sys.argv[1:] = [str(self.aooneint), "--scfinp"]
        ref_output = """\
ttitle                                                                                                                                                                                                         ====================================                                                                                                                                                                    
nsym 1
naos (7,)
potnuc  9.343638
kmax 5
ncent (1, 1, 1, 2, 3)
nbasis 7
jtran (1, 1, 1, 1, 1, 1, 1)
itran (1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0)
ctran (1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
inamn (538976335, 538976335, 538976335, 538976335, 538976335, 538976328, 538976328)
iptyp (1, 1, 2, 3, 4, 1, 1)
dpnuc (0.0, 0.0, 2.2)
nucdep 3
cooo (0.0, 0.0, 0.0, 0.0, 1.4, 1.1, 0.0, -1.4, 1.1)
ifxyz (0, 0, 0)
dummy 1e+20
qpol (1e+20, 1e+20, 1e+20, 1e+20, 1e+20, 1e+20)
qq (1e+20, 1e+20, 1e+20)
jfxyz (-9999999, -9999999, -9999999)
"""


        one.main()
        captured = capsys.readouterr()
        assert ref_output == captured.out

    def test_main_label(self, capsys):
        sys.argv[1:] = [str(self.aooneint), "--label", "OVERLAP", "-v"]
        ref_output = """\
OVERLAP 
Block 1

    1.00000000
    0.23670394    1.00000000
    0.00000000    0.00000000    1.00000000
    0.00000000    0.00000000    0.00000000    1.00000000
    0.00000000    0.00000000    0.00000000    0.00000000    1.00000000
    0.05593492    0.48471843    0.00000000    0.31344559    0.24627868    1.00000000
    0.05593492    0.48471843    0.00000000   -0.31344559    0.24627868    0.26358601    1.00000000

"""

        one.main()
        captured = capsys.readouterr()
        assert  ref_output == captured.out

    def test_main_label_unpack(self, capsys):
        sys.argv[1:] = [str(self.aooneint), "--label", "OVERLAP", "-v", "-u"]
        ref_output = """\
OVERLAP 
 (7, 7)
              Column   1    Column   2    Column   3    Column   4    Column   5
       1      1.00000000    0.23670394    0.00000000    0.00000000    0.00000000
       2      0.23670394    1.00000000    0.00000000    0.00000000    0.00000000
       3      0.00000000    0.00000000    1.00000000    0.00000000    0.00000000
       4      0.00000000    0.00000000    0.00000000    1.00000000    0.00000000
       5      0.00000000    0.00000000    0.00000000    0.00000000    1.00000000
       6      0.05593492    0.48471843    0.00000000    0.31344559    0.24627868
       7      0.05593492    0.48471843    0.00000000   -0.31344559    0.24627868

              Column   6    Column   7
       1      0.05593492    0.05593492
       2      0.48471843    0.48471843
       4      0.31344559   -0.31344559
       5      0.24627868    0.24627868
       6      1.00000000    0.26358601
       7      0.26358601    1.00000000

"""

        one.main()
        captured = capsys.readouterr()
        assert ref_output == captured.out

    def test_read_wrong_file(self):
        with raises(RuntimeError):
            one.readhead(self.aoproper)

    def test_wrong_integer_format(self):
        class Dummy(object):
            reclen = 7

            def __len__(self):
                return self.reclen

        with raises(RuntimeError):
            i = one._get_integer_format(Dummy())
