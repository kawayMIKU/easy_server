# easy_server 3.12
# 一个超级轻量而强大的Python语言HTTP服务器框架
import socket
from threading import Thread, RLock
from urllib import parse
from time import strftime, sleep
import re
from traceback import print_exc

class Tool_Rules: #自带的一些规则，可以投入使用，也可以供学习使用
        def Watch_Goose(event):
                '''一只专咬访问过快IP的大鹅'''
                conn = event.conn
                addr = event.addr
                global watch_goose_dict
                addr = addr[0]
                try:
                        time.time
                except:
                        import time
                try:
                        watch_goose_dict
                except:
                        watch_goose_dict = {}
                now = time.time()
                for i in list(watch_goose_dict.keys()):
                        if (now - watch_goose_dict[i]['time'] >= 3):
                                del watch_goose_dict[i]
                if addr in watch_goose_dict:
                        watch_goose_dict[addr]['time'] = now
                        watch_goose_dict[addr]['times'] += 1
                        if watch_goose_dict[addr]['times'] > 20:
                                print('[看门鹅]异常地址：{}！！！'.format(addr))
                                cps = round(watch_goose_dict[addr]['times']/(now-watch_goose_dict[addr]['start'])*100)/100
                                sending = '''<title>看门鹅！！！</title><h1>看门鹅！！！<br>你访问的太快了！！！</h1><h2>你在{}秒内访问了{}次！！！<br>你的访问频率是{}/秒！！！<br>3秒内不访问解除封禁！！！</h2>'''
                                sending = sending.format(round((now-watch_goose_dict[addr]['start'])*100)/100,watch_goose_dict[addr]['times'],cps)
                                conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                conn.sendall(sending.encode('utf-8'))
                                return True
                else:
                        watch_goose_dict[addr] = {
                                'start': now,
                                'time': now,
                                'times': 1
                                }
        class SN_Manager:
                def SN_Rule(event):
                        f = event.get
                        conn = event.conn
                        global SN_Flag
                        global SN_List
                        try:
                                SN_Flag
                        except:
                                SN_Flag = '[需要序列号]'
                        try:
                                SN_List
                        except:
                                SN_List = []
                        if SN_Flag in f[0]:
                                if 'SN' in f[1]:
                                        if f[1]['SN'] in SN_List:
                                                SN_List.remove(f[1]['SN'])
                                        else:
                                                conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                                conn.sendall('''<title>序列号管理器</title>
<h1>输入的序列号不正确或已被使用！</h1>'''.encode('utf-8'))
                                                conn.close()
                                else:
                                        conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                        conn.sendall('''<title>序列号管理器</title>
<h1>请输入序列号
<form method="get">
<input type="password" id="SN" name="SN" required>
<input type="submit" value="确认">
</form>
</h1>'''.encode('utf-8'))
                                        return True
                def creat_SN(SN:str=None):
                        global SN_List
                        try:
                                SN_List
                        except:
                                SN_List = []
                        try:
                                time.strftime
                        except:
                                import time
                        try:
                                random.randint
                        except:
                                import random
                        if SN == None:
                                now = time.strftime('%Y%H%M%S')
                                SN = now+str(random.randint(0,100))
                        SN_List.append(SN)
        class API_Keys_Manager:
                def Keys_Rule(event):
                        f = event.get
                        conn = event.conn
                        global Keys_list
                        global need_Keys
                        try:
                                Keys_list
                        except:
                                Keys_list = []
                        try:
                                need_Keys
                        except:
                                need_Keys = []
                        if f[0] in need_Keys:
                                if 'key' in f[1]:
                                        if not f[1]['key'] in Keys_list:
                                                conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                                conn.sendall('API密钥错误'.encode('utf-8'))
                                                return True
                                else:
                                        conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                        conn.sendall('此API需要密钥'.encode('utf-8'))
                                        return True

class Fittings:
        class Encoders:
                def utf_8_encoder(str):
                        return str.encode('utf-8')
                def utf_8_decoder(bytes):
                        return bytes.decode('utf-8')
        class Dict_spliters:
                def dict_spliter(str_data):
                        try:
                                get_ = re.match(r'[^/]*/+([^ ]*)\s+',str_data).group(1).split('?')
                                txt = ''
                                for i in get_[1:]:
                                        txt += i + '?'
                        except:
                                txt = ''
                        a = {}
                        try:
                                for i in txt[:-1].split('&'):
                                        i = i.split('=')
                                        a[parse.unquote(i[0])] = parse.unquote(i[1])
                        except:
                                pass
                        try:
                                get = (parse.unquote(get_[0]),a)
                        except:
                                get = ('',{})
                        return get
                def add_space_convert(str_data):
                        try:
                                get_ = re.match(r'[^/]*/+([^ ]*)\s+',str_data).group(1).split('?')
                                txt = ''
                                for i in get_[1:]:
                                        txt += i + '?'
                        except:
                                txt = ''
                        a = {}
                        try:
                                for i in txt[:-1].split('&'):
                                        i = i.split('=')
                                        a[parse.unquote(i[0])] = parse.unquote(i[1].replace('+',' '))
                        except:
                                pass
                        try:
                                get = (parse.unquote(get_[0]),a)
                        except:
                                get = ('',{})
                        return get

class Server:
        
        '''
服务器对象
'''
        
        sendings = {'':'<h1>html服务器主页面（未定义）</h1>'}
        max_conn = 128
        
        listen = 128
        single_thread_mode = False
        timeout = 1
        full_loop_wait = 0.05
        connect_rules = []
        requests_rules = []
        timeout_rules = []
        encoder = None
        decoder = None
        dict_spliter = None
        max_recv = 67108864
        recv_buffer_size = 4096
        none = None
        error = None
        default_error_code = 'HTTP/1.1 500 Internal Server Error\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
        default_html_code = 'HTTP/1.1 404 Not Found\r\nContent-Type:text/html; charset=utf-8\r\n\r\n'
        running = False
        server = None
        host_port = None
        conn_list = []
        lock = None
        log = 3

        def printlog(self,str = 'None',type = 'i'):
                time = strftime('%m-%d %H:%M:%S')
                tp = type.lower()
                if tp == 's':
                        print('\033[32m{}\033[0m [\033[32mSECCESS\033[0m] | {}'.format(time,str))
                elif tp == 'i':
                        print('\033[32m{}\033[0m [\033[38mINFO\033[0m] | {}'.format(time,str))
                elif tp == 'w':
                        print('\033[32m{}\033[0m [\033[33mWARING\033[0m] | {}'.format(time,str))
                elif tp == 'e':
                        print('\033[32m{}\033[0m [\033[31mERROR\033[0m] | {}'.format(time,str))
                else:
                        print('\033[32m{}\033[0m [\033[38m{}\033[0m] | {}'.format(time,type,str))
                        
        def __init__(self):
                self.encoder = Fittings.Encoders.utf_8_encoder
                self.decoder = Fittings.Encoders.utf_8_decoder
                self.dict_spliter = Fittings.Dict_spliters.dict_spliter
                self.none = lambda server,event: '''<h1>页面/文件没了qwq</h1><h2>找不到 {} qwq</h2>'''.format(str(event.get))
                self.error = lambda server,event: '<h1>页面没了qwq</h1>'
        
        class Event:
                def __init__(self):
                        pass
                        
        def http(self,conn,addr):
                self.lock.acquire()
                self.conn_list.append((conn,addr))
                self.lock.release()
                if self.log >= 3:
                        self.printlog('接受连接，对方IP: '+str(addr))

                lasts = []
                for rule in self.connect_rules:
                        
                        try:
                                event = self.Event()
                                event.conn = conn
                                event.addr = addr
                                event.lasts = lasts
                                lasts.append(rule(event))
                                
                        except Exception as err:
                                if self.log >= 1:
                                        self.printlog('连接处理规则: '+str(rule)+' 遇到错误: '+str(err),'w')
                                        print_exc()
                        
                ori_data=b''
                while True:
                        temp = conn.recv(self.recv_buffer_size)
                        if not temp:
                                break
                        ori_data += temp
                        if (self.encoder('\r\n\r\n') in ori_data) or (len(ori_data) >= self.max_recv):
                                break
                found = False
                for i in range(len(ori_data)):
                        if ori_data[i:i+4] == b'\r\n\r\n':
                                data = ori_data[:i]
                                excess_received_data = ori_data[i:]
                                found = True
                                break
                if not found:
                        data = ori_data
                        excess_received_data = b''
                str_data = self.decoder(data)
                try:
                        http_dict = str_data.split('\r\n')
                        index_count = 1
                        for i in range(0,len(http_dict)):
                                if not ': ' in http_dict[i]:
                                        http_dict[i] = 'INFO{}: '.format(index_count)+http_dict[i]
                                        index_count += 1
                        temp = {}
                        for i in http_dict[:-2]:
                                i = i.split(': ')
                                temp[i[0]] = i[1]
                        http_dict = temp
                except:
                        http_dict = {}

                get = self.dict_spliter(str_data)
                
                if self.log >= 3:
                        self.printlog('{} 的请求: {}'.format(addr,get))
                
                
                c = None
                byte = None
                lasts = []
                event = self.Event()
                event.get = get
                event.conn = conn
                event.addr = addr
                event.http_dict = http_dict
                event.lasts = lasts
                event.data = data
                event.excess_received_data = excess_received_data
                event.str_data = str_data
                try:
                        for rule in self.requests_rules:
                                try:
                                        ret = rule(event)
                                        lasts.append(ret)
                                        try:
                                                if ret != None:
                                                        if type(ret) == tuple:
                                                                byte = ret[0]
                                                                c = ret[1]
                                                        else:
                                                                byte = ret
                                                                c = self.encoder('HTTP/1.1 404 Not Found\r\nContent-Type:text/html; charset=utf-8\r\n\r\n')
                                        except Exception as err:
                                                if self.log >= 1:
                                                        self.printlog('在处理请求处理规则： '+str(rule)+' 的返回值时遇到错误：'+err,'w')
                                                        print_exc()
                                        event = self.Event()
                                        event.get = get
                                        event.conn = conn
                                        event.addr = addr
                                        event.http_dict = http_dict
                                        event.lasts = lasts
                                        event.data = data
                                        event.excess_received_data = excess_received_data
                                        event.str_data = str_data
                                        
                                except Exception as err:
                                        if self.log >= 1:
                                                self.printlog('请求处理规则: '+str(rule)+' 遇到错误: '+str(err),'w')
                                                print_exc()
                                
                                if byte == None:
                                        ret = self.none(self,event)
                                        if type(ret) == tuple:
                                                byte = ret[0]
                                                c = ret[1]
                                        else:
                                                byte = ret
                                if c == None:
                                        c = self.default_html_code
                        try:
                                if not type(c) == bytes:
                                        c = self.encoder(c)
                                conn.sendall(c)
                                if not type(byte) == bytes:
                                        byte = self.encoder(byte)
                                conn.sendall(byte)
                                conn.close()
                        except Exception as err:
                                if self.log >= 1:
                                        self.printlog('在发送数据时遇到错误： '+str(err),'w')
                                        print_exc()

                except Exception as err:
                        if self.log >= 2:
                                self.printlog('遇到错误: '+str(err),'w')
                                print_exc()
                        try:
                                ret = self.error(self,event)
                                if type(ret) == tuple:
                                        text = ret[0]
                                        head = ret[1]
                                else:
                                        text = ret
                                        head = self.default_error_code
                                if type(text) != byte:
                                        text = self.encoder(text)
                                if type(head) != byte:
                                        head = self.encoder(head)
                                conn.sendall(text)
                                conn.sendall(head)
                                conn.close()
                        except Exception as err2:
                                if self.log >= 2:
                                        self.printlog('在处理错误 '+str(err)+' 时遇到错误: '+str(err2),'w')
                                        print_exc()
                                try:
                                        conn.close()
                                except:
                                        pass
                try:
                        self.lock.acquire()
                        self.conn_list.remove((conn,addr))
                        self.lock.release()
                except:
                        try:
                                self.lock.release()
                        except:
                                pass
                if self.log >= 3:
                        self.printlog('已断开与 {} 的连接'.format(addr))

        
        def run(self,host_port='127.0.0.1'):
                '''
运行服务器
'''
                
                if not self.running:
                        self.server = socket.socket()
                        self.conn_list = []
                        self.lock = RLock()
                        try:
                                if type(host_port) == str:
                                        split = host_port.split(':')
                                else:
                                        split = host_port
                                if len(split) >= 2:
                                        host__port = (split[0],int(split[1]))
                                else:
                                        host__port = (split[0],80)
                                self.server.bind(host__port)
                                self.host_port = host__port
                                self.server.listen(self.listen)
                                if self.timeout != None:
                                        self.server.setblocking(False)
                                else:
                                        self.server.setblocking(True)
                                self.server.settimeout(self.timeout)
                                self.running = True
                                if self.log >= 1:
                                        self.printlog('启动服务器成功','s')
                                        self.printlog('开始在 {}:{} 上运行服务器'.format(host__port[0],host__port[1]),'s')
                        except Exception as err:
                                raise err
                        while self.running:
                                try:
                                        if len(self.conn_list) < self.max_conn:
                                                conn,addr = self.server.accept()
                                                if self.single_thread_mode:
                                                        self.http(conn,addr)
                                                else:
                                                        Thread(target=lambda:self.http(conn,addr)).start()
                                        else:
                                                sleep(self.full_loop_wait)
                                except Exception as err:
                                        if self.log >= 2 and str(err) != 'timed out':
                                                self.printlog('遇到错误: '+str(err),'w')
                                                print_exc()
                                        if str(err) == 'timed out':
                                                lasts = []
                                                for rule in self.timeout_rules:
                                                        
                                                        try:

                                                                event = self.Event()
                                                                event.lasts = lasts
                                                                
                                                                lasts.append(rule(event))
                                                                
                                                        except Exception as err:
                                                                if self.log >= 1:
                                                                        self.printlog('超时处理规则: '+str(rule)+' 遇到错误: '+str(err),'w')
                                                                        print_exc()
                        self.lock.acquire()
                        for i in self.conn_list:
                                if self.log >=3:
                                        self.printlog('已断开与 {} 的连接'.format(i[1]))
                                i[0].close()
                        self.conn_list = []
                        self.server.close()
                        self.lock.release()
                        if self.log >= 1:
                                self.printlog('已停止服务器','s')
        def stop(self):
                '''
停止服务器
'''
                self.running = False
        def disconn(self,conn):
                '''
断开连接
'''
                try:
                        found = False
                        self.lock.acquire()
                        for i in self.conn_list:
                                if i[0] == conn:
                                        found = True
                                        i[0].close()
                                        self.conn_list.remove(i)
                                        if self.log >=3:
                                                self.printlog('已断开与 {} 的连接'.format(i[1]))
                                        break
                        self.lock.release()
                except Exception as err:
                        try:
                               self.lock.release()
                        except:
                                pass
                        raise err
                if not found:
                        raise RuntimeError('连接不存在')
        def disconn_ip(self,addr):
                '''
断开地址与服务器的所有连接
addr可以是ip、端口，或(ip,端口)，用于寻找匹配的连接
'''
                count = 0
                try:
                        self.lock.acquire()
                        for i in self.conn_list:
                                right = False
                                if type(addr) == str:
                                        if i[1][0] == addr:
                                                right = True
                                elif type(addr) == int:
                                        if i[1][1] == addr:
                                                right = True
                                else:
                                        if i[1] == addr:
                                                right = True
                                if right:
                                        i[0].close()
                                        self.conn_list[self.conn_list.index(i)] = None
                                        if self.log >=3:
                                                self.printlog('已断开与 {} 的连接'.format(i[1]))
                                count += 1
                        try:
                                while True:
                                        self.conn_list.remove(None)
                        except:
                                pass
                        self.lock.release()
                except Exception as err:
                        try:
                                self.lock.release()
                        except:
                                pass
                        raise err
                if self.log >=3:
                        self.printlog('已断开 {} 个连接'.format(count))
                return count
        def disconn_all(self):
                self.lock.acquire()
                for i in self.conn_list:
                        if self.log >=3:
                                self.printlog('已断开与 {} 的连接'.format(i[1]))
                        i[0].close()
                count = len(self.conn_list)
                self.conn_list = []
                self.lock.release()
                if self.log >=3:
                        self.printlog('已断开 {} 个连接'.format(count))
                return count
server = Server

if __name__ == '__main__':
        from json import dumps
        from threading import *
        from time import *
        
        s = server()
        
        def rule(event):
                f = event.get
                dict = event.http_dict
                a = '<title>测试</title><h1>测试</h1><h2>你的请求是：{}</h2><h3>你的请求头是：<br>{}<h3/>'.format(f[0]+str(f[1]),dumps(dict,ensure_ascii=False,indent=0).replace('\n','<br>')).encode('utf-8')
                return a
            
        def infinity(event):
                f = event.get
                conn = event.conn
                file = ('鸡你太美'*512).encode('utf-8')
                if f[0].lower() == 'infinity':
                        conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:application/octet-stream\r\n\r\n')
                        while True:
                                conn.sendall(file)
                                sleep(0.5)
                                
        s.requests_rules = [
            infinity,
            rule,
        ]
        
        s.run()
