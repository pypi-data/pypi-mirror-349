import pytest
import jjcli
import sys
import re

# cl = jjcli.clfilter()
testdir = re.sub(r'(.*)/.*', r'\1', __file__)
multipleopt = testdir+'/ex-multipleopt.py'
    ## clfilter("abc:d:*", doc=__doc__)

def test_multipleopt():
    a = jjcli.qx(f"python3 {multipleopt} -a -c arg1 -d arg2 -d arg3") 
    opt = eval(a)
    assert opt["-a"]  == ""
    assert "-a" in opt
    assert "-b" not in opt
    assert opt["-c"]  == "arg1"
    assert len(opt["-d"])  == 2
    assert opt["-d"][1]  == "arg3"

def test_helpoption():
    b = jjcli.qx(f"python3 {multipleopt} --help") 
    assert "Usage" in b

def test_glob():
    l = jjcli.glob(f'{testdir}/ex*.py')
    assert len(l) >= 1

def test_qx():
    if sys.platform == 'linux':
        a = int(jjcli.qx(f"grep -c test_qx {__file__} "))
        assert  a >= 2

def test_qxlines():
    b = jjcli.qxlines(f"python3 {multipleopt} --help") 
    assert "Where options" in b[2]
