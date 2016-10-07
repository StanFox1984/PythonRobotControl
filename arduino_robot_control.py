from __future__ import print_function

import urllib
import urllib2
import re
import serial
import time
import httplib
import socket



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
          if isinstance(i, Functor) and not i is self:
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
        #self.called = True
        return self.do_expr()
    def __call__(self, *_args):
        #if self.called:
        #  return self._res
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

class LeftMotorOn(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        data = {"add": "FErArg", "command" : "LeftMotorOn", "reply" :""}
        data = urllib.urlencode(data)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(5)

class RightMotorOn(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        data = {"add": "FErArg", "command" : "RightMotorOn", "reply" :""}
        data = urllib.urlencode(data)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(5)

class RightMotorOff(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        data = {"add": "FErArg", "command" : "RightMotorOff", "reply" :""}
        data = urllib.urlencode(data)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(5)

class LeftMotorOff(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        data = {"add": "FErArg", "command" : "LeftMotorOff", "reply" :""}
        data = urllib.urlencode(data)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(5)

class ReadSensor(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        print (self.args_list)
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        if self.args_list[0] == 1:
            data = {"add": "FErArg", "command" : "Sensor0", "reply" :""}
        if self.args_list[0] == 2:
            data = {"add": "FErArg", "command" : "Sensor1", "reply" :""}
        data = urllib.urlencode(data)
        data2 = {"clear": "FErArg", "command" : "s", "reply" :""}
        data2 = urllib.urlencode(data2)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(2)
        d = {}
        while True:
            request = urllib2.Request(url + '?' + data)
            response = urllib2.urlopen(request)
            page = response.read()
            #time.sleep(1)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read()
            print(page)
            r = re.compile('"[a-zA-Z0-9]+":"[a-zA-Z0-9]+"')
            res = r.findall(page)
            print(str(res).replace('[','{').replace(']','}'))
            d = eval(str(res).replace('[','{').replace(']','}').replace('\'',''))
            print(d)
            if "reply" in d:
                break
            #else: time.sleep(1)
        print(d['reply'])
        time.sleep(2)
        request = urllib2.Request(url + '?' + data2)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(2)
        return int(d['reply'])

class ToggleSelfControl(Functor):
    def __init__(self, *_args, **_kargs):
        Functor.__init__(self,*_args, **_kargs)
    def do_expr(self):
        url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
        data = {"add": "FErArg", "command" : "SelfControl", "reply" :""}
        data = urllib.urlencode(data)
        request = urllib2.Request(url + '?' + data)
        response = urllib2.urlopen(request)
        page = response.read()
        time.sleep(5)

class FastHTTPResponse(httplib.HTTPResponse):
    def __init__(self, sock, debuglevel=0, strict=0, method="GET"):
        httplib.HTTPResponse.__init__(self, sock, debuglevel, strict)
        self.fp = sock.makefile('rb', 800)

# Tell the httplib that we want to use our hack..

class HubMessenger:
    def __init__(self, _name, _application, _url = \
"http://testst1984-test1984.rhcloud.com/hub.php"):
        self.url = _url
        self.name = _name
        self.application = _application
    def _send_message(self, receiver, data, delay = 1):
        message = { "add" : "", "receiver" : receiver, "data" : data, \
                    "sender" : self.name, "custom" : self.application }
        msg = urllib.urlencode(message)
        print(self.url+"?"+msg)
        request = urllib2.Request(self.url + "?" + msg)
        response = urllib2.urlopen(request)
        page = response.read()
        print(page)
        #time.sleep(delay)

    def _recv_message(self,  start_id=0, num_ids=100, delay = 1):
        message = { "self" : self.name, "show" : "ff", 
                    "start_id" : start_id, "num_ids" : num_ids }
        r = re.compile('[{][^{}]+[}]')
        msg = urllib.urlencode(message)
        print(msg)
        request = urllib2.Request(self.url + "?" + msg)
        response = urllib2.urlopen(request)
        page = response.read()
        print(page)
        res = r.findall(page)
        l = [ ]
        for i in res:
            i=i.replace('\0','')
            i=i.replace('\"','\'')
            i=i.replace('\'\'','\'')
            d = eval(i)
            l.append(d)
            #print(type(d))
        #print(l)
        #print(str(res).replace('[','{').replace(']','}'))
        #d = eval(str(res).replace('[','{').replace(']','}').replace('\'',''))
        #print(d)
        #self._clear_message()
        return l

    def _recv_message_any(self, start_id=0, num_ids=100, delay = 1):
        message = { "show" : "ff", "start_id" : start_id, "num_ids" : num_ids }
        #r = re.compile('([{] ("[a-zA-Z0-9]+" : "[a-zA-Z0-9]+"[, ]*)+[ ]*[}])')
        #r = re.compile('[{] ("[a-zA-Z0-9]+" : "[a-zA-Z0-9]+"[, ]{0,1})+ [}]')
        r = re.compile('[{][^{}]+[}]')
        msg = urllib.urlencode(message)
        print(msg)
        request = urllib2.Request(self.url + "?" + msg)
        response = urllib2.urlopen(request)
        page = response.read()
        print(page)
        res = r.findall(page)
        l = [ ]
        for i in res:
            i=i.replace('\0','')
            i=i.replace('\"','\'')
            i=i.replace('\'\'','\'')
            d = eval(i)
            l.append(d)
            #print(type(d))
        #print(l)
        #print(str(res).replace('[','{').replace(']','}'))
        #d = eval(str(res).replace('[','{').replace(']','}').replace('\'',''))
        #print(d)
        return l

    def _clear_message_all(self, delay = 1):
        message = { "clear" : "" }
        msg = urllib.urlencode(message)
        request = urllib2.Request(self.url + "?" + msg)
        response = urllib2.urlopen(request)
        page = response.read()
        #time.sleep(delay)

    def _clear_message(self, delay = 1):
        message = { "clear" : "", "self" : self.name }
        msg = urllib.urlencode(message)
        request = urllib2.Request(self.url + "?" + msg)
        response = urllib2.urlopen(request)
        page = response.read()
        #time.sleep(delay)



def func(*lst):
    mul = 1
    for i in lst:
      mul = mul * i
    return mul

if __name__ == "__main__":
    httplib.HTTPConnection.response_class = FastHTTPResponse
    #r = re.compile('(("[a-zA-Z0-9]+" : "[a-zA-Z0-9]+")[, ]{0,1})+')
    #r2 = re.compile('[{][^{}]+[}]')
    #page = '{ { "gfgfgfg" : "klkl", "klklkl" : "lklkllllll" },<BR><BR>{ "gfgfgfg1" : "klkl1", "klklkl1" : "lklkllllll1" }<BR><BR> }'
    #page = page.replace('<BR><BR>','')
    #res = r2.findall(page)   #findall(page)
    #for i in res:
#        s = eval(i)
#        print (s)
#    print(res)
#    exit(0)
    socket.setdefaulttimeout(2000)
    h = HubMessenger("arduino_cpu", "Tester")
    
    #while True:
    #    l = h._recv_message()[0]['data']

    h = HubMessenger("Stas" , "Tester")
    h2 = HubMessenger("Stas1" , "Tester")
    h._send_message("Stas1" , "This message for Stas1")
    h2._send_message("Stas" , "This message for Stas")
    l = str(h._recv_message()[0]['data'])
    l2 = str(h2._recv_message()[0]['data'])
    print(h.name+" got "+l)
    print(h2.name+" got "+l2)
    print("From all:")
    l = h._recv_message_any()
    print(l)
    h._clear_message_all()
    exit(0)
    #t=ToggleSelfControl()t
    #t()
    rmotoroff = RightMotorOff()
    lmotoroff = LeftMotorOff()
    lmotoron= LeftMotorOn()
    rmotoron = RightMotorOn()
    sensor = ReadSensor()
    rmotoroff()
    lmotoroff()
    while True:
        res = sensor(1)
        res2 = sensor(2)
        print(res)
        if res > (res2):
            print ("first won")
            lmotoron()
        else:
            print ("second won")
            rmotoron()
        time.sleep(1)
    exit(0)
    url = "http://stanfoxarduino-stanfoxarduino.rhcloud.com/index.php"
    data = {"clear": "FErArg"}
    data = urllib.urlencode(data)
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    #request = urllib2.Request(url + '?' + data)
    #response = urllib2.urlopen(request)
    #page = response.read()
    while(True):
        print("fdfdfd")
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        r = re.compile('"[a-zA-Z0-9]+":"[a-zA-Z0-9]+"')
        page = response.read()
        print(page)
        res = r.findall(page)
        print( res)
        print(str(res).replace('[','{').replace(']','}'))
        d = eval(str(res).replace('[','{').replace(']','}').replace('\'',''))
        print(d)
        time.sleep(0.2)
        if 'command' in d:
            print (d['command'])
            ser.write(d["command"])
            resp = ser.read(10)
            print(resp)
            request = urllib2.Request(url + '?' + data)
            response = urllib2.urlopen(request)
            page = response.read()
            if len(resp) > 0:
               data2 = { "add": "FErArg", "command": "prev_"+d['command'], "reply" : resp } 
               data2 = urllib.urlencode(data2)
               request2 = urllib2.Request(url + '?' + data2)
               response = urllib2.urlopen(request2)
               page = response.read()

#from __future__ import print_function

