"""
Usage:
    ex-multipleopt [options]
    Where options:
      -a
      -b
      -c arg
      -d arg (repeatable)
"""
import jjcli

cl = jjcli.clfilter("abc:d:*", doc = __doc__)
print(cl.opt)
