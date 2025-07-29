
r"""
# Name

 jjcli - python module for (unix-like) command-line filter

# Synopsis

as ascript:

    jjcli skel myscript ## writes an initial filter skeleton in myscript
    jjcli skel          ## initial filter skeleton 
    jjcli               ## manual

as a module: 

    ''' ... add the documentation here '''

    from jjcli import *        ## re.* functions also imported
    cl=clfilter(opt="do:t:*", man=__doc__)   ## script -d -o arg -t arg1 -t arg2
                               ## options in cl.opt  (...if "-d" in cl.opt:)
                               ## autostrip         (def=True)
                               ## inplace=True      (def=False) 
                               ## fs (for csvrow()) (def=",")
                               ## longopts=["opt1", ...] (def=[])
                               ## doc=__doc__   for "--help" (def="FIXME no doc provided")

    for line in cl.input():... ## process one rstriped line at the time
    for txt in cl.text():...   ## process one striped text at the time (alias: cl.slurp)
       ## process txt          ##   (\r and spaces at the end of line or removed)
    for par in cl.paragraph(): ## process one striped paragraph at the time
    for tup in cl.csvrow():... ## process one csv row at the time
    for tup in cl.tsvrow():... ## process one tsv row at the time

    cl.lineno()                ## line number
    cl.filelineno()
    cl.parno()                 ## paragraph number
    cl.fileparno()
    cl.filename()              ## filename or "<stdin>"
    cl.nextfile()
    cl.isfirstline()
    cl.args  cl.opt             ## command line arguments and options (after clfilter())

# Description

__jjcli__ is a opinioned Python module to simplify the creation of
__unix__ filters. It is based on:

- getopt  (for command line options and args)   
- fileinput (for [files/stdin] arguments)
- re (regular expressions should be native)
- glob (glob.glob should be native)
- csv  (to deal with csv and tsv inputs)
- urllib.request (to deal with input argumens that are url)
- subprocess (see bellow qx, qxlines, qxsystem, qxerr)

## Regular expressions

We want to have all re.* functions available (as if they were native
functions).

In order to enable __re__ flags, use: re.I re.X re.S  

## Subprocesses   (qx, qxlines, qxsystem)

    a=qx( "ls" )
    for x in qxlines("find | grep '\.jpg$'"): 
      ...
    qxsystem("vim myfile")

### Execute command return its stdout

    qx(*x)      →  returns    subprocess.getoutput(x)

### Execute command return its stdout lines

    qxlines(*x) →  returns    qx(x).splitlines()

### Execute command -- system

    qxsystem(*x) →  calls     subprocess.call(x,shell=True)

### Execute command return its stdout and stderr

    out,err = qxerr(*x)  →  returns    communicate(...)

## STDERR - warn, die

    warn(*args)  → print to stderr
    die(*args)   → warn and exit 1

## Documentation from docstrings

    

## Other functions

    slurpurlutf8(self,url) 

    filename    = lambda s : F.filename()      # inherited from fileinput
    lineno      = lambda s : F.lineno()        # line number (acumulated)
    filelineno  = lambda s : F.filelineno()    # line number
    parno       = lambda s : s.parno_          # paragraph number
    fileparno   = lambda s : s.fileparno_
    nextfile    = lambda s : F.nextfile()      # jump to next file
    isfirstline = lambda s : F.isfirstline()   # true if new file
    isfirstpar  = lambda s : s.fileparno == 1
    close       = lambda s : F.close()

## Inplace flag  -- FIXME

if the keyword argument *inplace=True* is passed to jjcli.clfilter the file
is moved to a backup file and standard output is directed to the input
file. This makes it possible to write a filter that rewrites its input
file in place. By default, the extension is '.bak' and it is deleted when
the output file is closed. In-place filtering is disabled when standard
input is read.

"""

import subprocess 
import inspect
from subprocess import PIPE, Popen
import re
from glob import glob
from re import match, fullmatch, search, sub, subn, split, findall, finditer, compile 
                    ## all re functions are imported!
                    ## and re.I re.S re.X 
import fileinput as F, getopt, sys
import urllib.request as ur, csv
import os

## execute external comands

# execute command return its stdout
def qxerr(*x)   : 
    """ out, err = qxerr("ls \n date\n xxxxx") """
    process = Popen(str.join(" ",x), stdout=PIPE, stderr=PIPE, encoding="utf8", shell=True)
    return process.communicate()

# execute command return its stdout
def qx(*x)      : return subprocess.getoutput(str.join(" ",x))

# execute command return its stdout lines
def qxlines(*x) : return subprocess.getoutput(str.join(" ",x)).splitlines()

# execute command -- system
def qxsystem(*x): subprocess.call(str.join(" ",x),shell=True)

# execute command -- popen
# def qxopen(cmd, mode="r"): 
#     if mode == "w":
#        proc = subprocess.Popen(cmd, shell=True,text=True, encoding="utf-8", stdin=PIPE)
#        return proc.stdin
#     else:
#        proc = subprocess.Popen(cmd, shell=True,text=True, encoding="utf-8", stdout=PIPE)
#        return proc.stdout

def die(*s,**kwargs):
    warn(*s,**kwargs)
    sys.exit(1)

def warn(*a,**kwargs):
    print(*a,file=sys.stderr,**kwargs)

## Command line filters
class clfilter:
   '''csfilter - Class for command line filters'''
   
   def __init__(self,opt="",
                     longopts=[],
                     rs="\n",
                     fs=",",
                     autostrip=True,
                     files=[],
                     doc=None,
                     man=None,
                     inplace=False):
       opcs=[]
       if man:
           usage = doc or sub(r'\n#*\s*description.*',r'',man,flags=re.I | re.S)
       else:
           usage = doc or "FIXME: no doc provided"
           man = usage
       
       if isinstance( files, str): files = [files]
       if isinstance(opt,dict):
           self.opt, self.args = (opt, files)
       else:
           multipleopt = re.findall(r'(\w):\*', opt)
           opt = re.sub(r':\*', r':', opt)
           try:
               opts, args = getopt.gnu_getopt(sys.argv[1:],opt,longopts+["help","man"])
           except Exception as err:
               die(err,"\n   Try option --help or --man")  
               sys.exit(1)
           self.opt=dict(opts)
           for m in multipleopt:
               optm= '-'+m
               if optm in self.opt:
                   self.opt[optm] = [v for (x, v) in opts if optm == x ]
           self.args=args + files
       if "--man" in self.opt :
           # print(__import__(caller_name[1]).__doc__ )
           print(man.strip())
           sys.exit(0)
       if "--help" in self.opt :
           # print(__import__(caller_name[1]).__doc__ )
           print(usage.strip())
           sys.exit(0)
       self.rs=rs
       self.fs=fs
       self.autostrip=autostrip
       self.inplace=inplace
       if inplace: 
           self.backup = ".bak"
       else:
           self.backup = ''
       self.text=self.slurp
       if os.name == "nt":   ### linux, mac = posix; windows = nt
           sys.stderr.reconfigure(encoding="utf-8")
           sys.stdout.reconfigure(encoding="utf-8")
#       self.enc=F.hook_encoded("utf-8")
 
   def input(self,files=None): 
       files = files or self.args
       if self.autostrip:
           return map(str.rstrip,F.input(files=files,inplace=self.inplace,backup=self.backup, encoding="utf-8"))
       else:
           return F.input(files=files,inplace=self.inplace,backup=self.backup, encoding="utf-8")

   def csvrow(self,files=None):
       files = files or self.args
       return csv.reader(F.input(files=files, encoding="utf-8"),
                         skipinitialspace=True, delimiter=self.fs)

   def tsvrow(self,files=None):
       files = files or self.args
       return csv.reader(F.input(files=files, encoding="utf-8"),
                         skipinitialspace=True, delimiter="\t")

   def paragraph(self,files=None):
       files = files or self.args or [None]
       self.parno_=0
       for f in files:
           t=""
           state=None
           self.fileparno_=0
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace,backup=self.backup, encoding="utf-8"):
               if search(r'\S', l) and state == "inside delim":
                   self.parno_+= 1
                   self.fileparno_+= 1
                   if self.autostrip:
                       yield self.cleanpar(t)
                   else:
                       yield t
                   state ="inside par"
                   t=l
               elif search(r'\S', l) and state != "inside delim":
                   t += l
                   state ="inside par"
               else:
                   state ="inside delim"
                   t += l
           if search(r'\S',t):             ## last paragraph
               self.parno_+= 1
               self.fileparno_+= 1
               if self.autostrip:
                   yield self.cleanpar(t)
               else:
                   yield t

   def off_slurp(self,files=None):
       files = files or self.args or [None]
       for f in files:
           t=""
           fs = [] if f == None else [f]
           for l in F.input(files=fs,inplace=self.inplace):
               t += l
           if self.autostrip:
               yield self.clean(t)
           else:
               yield t

   def slurp(self,files=None):
       files = files or self.args or [None]
       for f in files:
           t=""
           if f == None: fs=[]
           elif match(r'(https?|ftp|file)://',f):
               yield ur.urlopen(f).read().decode('utf-8')
               continue
           else: fs = [f]

           for l in F.input(files=fs,inplace=self.inplace,backup=self.backup, encoding="utf-8"):
               t += l
           if self.autostrip:
               yield self.clean(t)
           else:
               yield t

   def slurpurlutf8(self,f):
       t= ur.urlopen(f).read()
       try:  
           a = t.decode('utf-8')
           return a
       except Exception as e1:
           try:  
               a = t.decode('iso8859-1')
               return a
           except Exception as e:
               return t

   def clean(self,s):              # clean: normalise end-of-line spaces and termination
       return sub(r'[ \r\t]*\n','\n',s)

   def cleanpar(self,s):           # clean: normalise end-of-line spaces and termination
       return sub(r'\s+$','\n' ,sub(r'[ \r\t]*\n','\n',s))

   filename    = lambda s : F.filename()      # inherited from fileinput
   filelineno  = lambda s : F.filelineno()
   lineno      = lambda s : F.lineno()
   fileparno   = lambda s : s.fileparno_
   parno       = lambda s : s.parno_
   nextfile    = lambda s : F.nextfile()
   isfirstline = lambda s : F.isfirstline()
   isfirstpar  = lambda s : s.fileparno_ == 1
   close       = lambda s : F.close()

#   filename    = F.filename()      # não funciona assim...

__version__ = "0.1.29"
__docformat__ = 'markdown'

def main():
   if   len(sys.argv)==1: 
      print("Name\n jjcli - ",__doc__.lstrip())

   elif len(sys.argv)==3 and sys.argv[1] == "skel":
      scri = sys.argv[2]
      if not os.path.exists(scri):
          f = open(scri,"w")
      else:
          f = sys.stdout
      print( f"""#!/usr/bin/python3
'''
NAME
   {scri} - ...

SYNOPSIS
   {scri} ...

Description'''

from jjcli import * 
cl=clfilter(opt="do:", doc=__doc__)  ## option values in cl.opt dictionary

for line in cl.input():    ## process one line at the time
    pass                   ## process line

""", file = f)  

   elif sys.argv[1] == "skel":
      print( f"""#!/usr/bin/python3
'''
NAME
    myscript - ...

SYNOPSIS
    myscript ...

Description'''

from jjcli import * 
cl=clfilter(opt="do:", doc=__doc__)     ## option values in cl.opt dictionary

for line in cl.input():    ## process one line at the time
    pass                   ## process line

#for txt in cl.text(): ...     ## process one file at the time
#for par in cl.paragraph():... ## process one paragraph at the time
#for txt in cl.cvsrow(): ...   ## process one csv row at the time
#for txt in cl.tvsrow(): ...   ## process one tsv row at the time
""") 

if __name__ == "__main__": main()
