from __future__ import print_function

import urllib
import urllib2
#import urllib3
import re
import serial
import time
import httplib




class Functor(object):
    def __init__(self, *_args, **_kargs):
        self._args_list = _args
        if("own_args" in _kargs):
          self._own_args = _kargs["own_args"]
        else:
          if len(_args) > 0:
              self._own_args = True
          else:
              self._own_args = False
        self.args_list = [ ]
        self.debug = True
        self.called = False
    def my_print(self, *args):
        if self.debug:
          print(*args)
    def do_expr(self):
        pass
    def do_expr_iter(self):
        self.my_print( self, "Got called with args: ", self._args_list)
        lst = []
        for i in self._args_list:
          if i is self:
            continue
          if isinstance(i, Functor) and not i is self and not i.called:
            self.my_print( i, " is instance of Functor")
            res = None
            if(i._own_args == True):
              self.my_print( "Calling ",i," with its own args")
              res = i.__call__()
              if res != None:
                self.my_print("Appending result ", res)
                lst.append(res)
            else:
              self.my_print( "Calling ",i," with our args")
              res = i.__call__(*(self._args_list))
              if res != None:
                args_list = [ ]
                for j in i.args_list:
                  args_list.append(res)
                _args_list = [ n for n in self._args_list if isinstance(n, Functor) ]
                _args_list.extend(args_list)
                self._args_list = _args_list
                self.args_list = args_list
                self.my_print( self,"'s new arg list: ", self._args_list)
                self.my_print( self,"'s new arg list without functors: ", self.args_list)
        args_list = [ i for i in self._args_list if not isinstance(i, Functor) ]

        self.args_list = args_list
        #self.args_list.extend(lst)

        self.my_print( "Final argument list:", self.args_list)
        self.called = True
        return self.do_expr()
    def __call__(self, *_args):
        if self.called:
          return self._res
        self.my_print( "__call__:", _args, len(_args))
        functors = [ n for n in self._args_list if isinstance(n, Functor) ]
        l = [ i for i in functors if not i._own_args ]
        self.my_print( "fillowing elements do not have args: ", l)
        is_all_own_args = len(l) == 0
        if len(_args) > 0:
          if is_all_own_args == False:
            lst = [ i for i in self._args_list if isinstance(i, Functor) ]
            self._args_list = lst
            for j in _args:
              self._args_list.append(j)
          else:
            self._args_list = _args
        self.my_print( "__call__ calling with:", self._args_list)
        self._res = self.do_expr_iter()
        return self._res

class Add(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        self.my_print( "add", self.args_list)
        if len(self.args_list) == 0:
          return 0
        return sum(self.args_list)


class Mul(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        self.my_print( "mul", self.args_list)
        if len(self.args_list) == 0:
          return 0
        return reduce(lambda x,y: x*y, self.args_list)

class Div(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        self.my_print( "div", self.args_list)
        if len(self.args_list) == 0:
          return 0
#        print self._args_list
        return reduce(lambda x,y: x/y, self.args_list)

class Print(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        print( "Print:", self.args_list)

def func(*lst):
    mul = 1
    for i in lst:
      mul = mul * i
    return mul

class FastHTTPResponse(httplib.HTTPResponse): 
    def __init__(self, sock, debuglevel=0, strict=0): 
        httplib.HTTPResponse.__init__(self, sock, debuglevel, strict) 
        self.fp = sock.makefile('rb', 8192) 

# Tell the httplib that we want to use our hack. 



if __name__ == "__main__":
    print ("HELLO")
    exit(0)
    #httplib.HTTPConnection.response_class = FastHTTPResponse
    i=0
    url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
    data = {"clear": "FErArg"}
    data = urllib.urlencode(data)
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    #request = urllib2.Request(url + '?' + data)
    #response = urllib2.urlopen(request)
    #page = response.read()
    while(True):
        i = i + 1
        print("fdfdfd ", i)
        print("sending request")
        http = urllib3.PoolManager(10)
        #request = urllib2.Request(url)
        #response = urllib2.urlopen(request)
        response = http.request('GET',url)
        r = re.compile('"[a-zA-Z0-9]+":"[a-zA-Z0-9]+"')
        page = response.data #response.read()
        print("end")
        print(page)
        res = r.findall(page)
        print( res)
        print(str(res).replace('[','{').replace(']','}'))
        d = eval(str(res).replace('[','{').replace(']','}').replace('\'',''))
        print(d)
        #time.sleep(0.02)
        if 'command' in d:
            if d['command'] != "prev":
                print ("writing "+ d['command'])
                ser.write(d["command"])
                time.sleep(.5)
                #ser.write(d["command"])
                print("reading")
                resp = ser.read(20)
                resp = resp.replace('pulse','')
                resp = resp.replace(d['command'],'')
                resp = resp.replace("Pong",'')
                ser.flushInput()
                ser.flushOutput()
                time.sleep(.1)
                print("end")
                print(resp)
                print("sending request")
                response = http.request('GET', url + '?' + data)
                #request = urllib2.Request(url + '?' + data)
                #response = urllib2.urlopen(request)
                page = response.data #response.read()
                print("end")
                if len(resp) > 0:
                    data2 = { "add": "FErArg", "command": "prev", "reply" : resp } 
                    data2 = urllib.urlencode(data2)
                    print("sending request")
                    #request2 = urllib2.Request(url + '?' + data2)
                    response = http.request('GET', url + '?' + data2)
                    #response = urllib2.urlopen(request2)
                    page = response.data#response.read()
                    print("end")