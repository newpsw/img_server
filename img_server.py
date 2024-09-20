import socket
from _thread import *
import time
import urllib.request
import requests
import os
import os.path
from PIL import Image


def t_client(conn, addr, IpS, connections, c_sockets, secretcode):
    
    mjoin = "[Info] Join chat: "+str(addr[0])+"\n"
    sjoin = "[Info] Connected!: "+str(addr[0])+"\n"
    
    print(mjoin)
    
    if len(c_sockets) > 0 :
        for i in c_sockets:
            if conn != i:
                i.sendall(mjoin.encode("utf-8"))
            else:
                i.sendall(sjoin.encode("utf-8"))
            
            continue
    
    while True:
        try :
            d = conn.recv(1024)
        except Exception as e:
            print(str(e)+'\n')
            
            if conn in c_sockets:
                c_sockets.remove(conn)
            
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            connections -= 1
            break
        
        if not d:
            lclistr = "[Info] Disconnect chat: "+str(addr[0])+"\n"
            print(lclistr)
            if conn in c_sockets:
                c_sockets.remove(conn)
            
            for i in c_sockets:
                i.sendall(lclistr.encode("utf-8"))
                continue
            
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            connections -= 1
            break
        
        DDecode = ''
        
        try:
            DDecode = d.decode("utf-8")
        except Exception as e:
            print(str(e)+'\n')
            lclistr = "[Info] Disconnect chat: "+str(addr[0])+"\n"
            
            if conn in c_sockets:
                c_sockets.remove(conn)
            
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            connections -= 1
            break
        
        if IpS != addr[0]:
            print(('('+addr[0]+') : '+DDecode+'\n'))
        else:
            print(DDecode+'\n')
        
        if len(c_sockets) > 0 :
            if IpS != addr[0]:
                if len(DDecode) > 3:
                    if DDecode[-len(secretcode):] != secretcode :
                        lclistr = "[Info] Disconnect chat: "+str(addr[0])+"\n"
                        print(lclistr)
                        if conn in c_sockets:
                            c_sockets.remove(conn)
                        
                        for i in c_sockets:
                            i.sendall(lclistr.encode("utf-8"))
                            continue
                        
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()
                        connections -= 1
                        break
                    else:
                        for i in c_sockets:
                            i.sendall(('('+addr[0]+') : '+DDecode[:-len(secretcode)]+'\n').encode("utf-8"))
                            continue
                else:
                    lclistr = "[Info] Disconnect chat: "+str(addr[0])+"\n"
                    print(lclistr)
                    
                    if conn in c_sockets:
                        c_sockets.remove(conn)
                        
                    for i in c_sockets:
                        i.sendall(lclistr.encode("utf-8"))
                        continue
                    
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()
                    connections -= 1
                    break
            else:
                if '#!DP-' in DDecode[:5] :
                    
                    Urlinfo = DDecode[6:].replace(' ', '')
                    
                    if Urlinfo != '' :
                        reqcount = 0
                        while True :
                            ierror = 0
                            try :
                                urllib.request.urlretrieve(Urlinfo, os.getcwd()+"\\0.png")
                                ierror = 0
                            except Exception as Emsg :
                                print("Img down failed: "+str(Emsg))
                                ierror = 1
                            
                            if ierror != 1  :
                                break
                        
                            reqcount += 1
                            if reqcount < 2 :
                                time.sleep(0.6)
                                continue
                        
                            break
                    
                    if os.path.isfile(os.getcwd()+"\\0.png") :
                        
                        # 이미지 경로
                        image_path = os.getcwd()+"\\0.png"
                        NandE = os.path.splitext(image_path)
                        
                        # 이미지를 흑백으로 변환
                        image = Image.open(image_path)
                        grayscale_image = image.convert("L")
                        width, height = image.size
                        
                        # 이미지의 해상도 수정
                        if width != 240 or height != 160 :
                            grayscale_image = grayscale_image.resize((240, 160))
                            width = 240
                            height = 160
                    
                        grayscale_image.save(NandE[0]+".png", 'png')
                        rgb_im = grayscale_image.convert('RGB')
                        
                        color_values = []
                        for y in range(height):
                            lineValue = []
                            for x in range(width):
                                if y < 5 or y > 154 or x < 7 or x > 232 :
                                    continue
                                r, g, b = rgb_im.getpixel((x, y))
                                if r > 220 :
                                    #lineValue.append([255, 255, 255]) #흰색
                                    lineValue.append(1)
                                elif r > 140 :
                                    #lineValue.append([130, 130, 130])
                                    lineValue.append(2)
                                else :
                                    #lineValue.append([0, 0, 0]) #검은색
                                    lineValue.append(3)
                                
                                if x != 232 :
                                    continue
                                
                                color_values.append(lineValue)
                                continue
                            
                            continue
                        
                        Sgroup = 44
                        icount = 0
                        re_values = "Dc_"+DDecode[5]+"-"+str(icount)
                        for y in range(0, height-10, 2):
                            for x in range(0, width-14, 2):
                                Fpixels = str(color_values[y][x])+str(color_values[y][x+1])+str(color_values[y+1][x])+str(color_values[y+1][x+1])
                                
                                if Fpixels == '1111' or Fpixels == '2222' or Fpixels == '3333':
                                    if Fpixels != '3333' :
                                        if Fpixels != '2222' :
                                            Fpixels = '5'
                                        else :
                                            Fpixels = '6'
                                    else :
                                        Fpixels = '7'
                                
                                if icount != 8474 :
                                    if icount != Sgroup : 
                                        re_values = re_values+"-"+Fpixels
                                    else :
                                        re_values = re_values+"-"+Fpixels
                                        conn.sendall(re_values.encode("utf-8"))
                                        re_values = "Dc_"+DDecode[5]+"-"+str(icount+1)
                                        Sgroup += 45
                                else :
                                    
                                    re_values = re_values+"-"+Fpixels
                                    
                                    conn.sendall(re_values.encode("utf-8"))
                                
                                icount += 1
                                continue
                            
                            continue
                        
                        image.close()
                    else :
                        print(" '0.png' file have to be in below path\n File path: "+os.getcwd()+'\n')
                        ReZero = 'Re0'
                        conn.sendall(ReZero.encode("utf-8"))
                else :
                    for i in c_sockets:
                        if conn != i:
                            i.sendall((DDecode+"\n").encode("utf-8"))
                        continue
                
                continue

def Server_Main() :
    
    IpS = ''
    port = 8999
    c_sockets = []
    connections = 0
    secretcode = ''
    
    while True :
        try:
            Ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            Ss.connect(("10.255.255.255", 1))
            IpS = Ss.getsockname()[0]
            Ss.shutdown(socket.SHUT_RDWR)
            Ss.close()
        except:
            print("[Info] Failed to get IP...")
            IpS = '127.0.0.1'
        
        print('Server IP: '+ IpS)
        
        while True :
            inputport = input('Port?: ')
            
            if len(inputport) < 1 :
                break
            
            if len(inputport) > 5 :
                print('Maximum length is 5!')
                continue
            
            if str.isdigit(inputport) != True :
                print('Please input only integers!')
                continue
            
            if int(inputport) > 65535 :
                print('Maximum port number is 65535')
                continue
            
            port = int(inputport)
            break
        
        print('Port: '+str(port)+'\n')
        
        try:
            Ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Ss.bind((IpS, port))
            Ss.listen()
        except socket.error as e:
            print(str(e))
            continue
        
        while True :
            secretcode = input('Please set secret code of message: ')
            if len(secretcode) < 1 :
                continue
            
            surecheck = input("\nYour secret code is: "+secretcode+"\n If correct, please enter 'y'or'Y'.\n")
            
            if surecheck != 'y' and surecheck != 'Y' :
                continue
            
            print("\n[!]If secret code is not attached to the end of the message, connection will be close.\n")
            
            break
        
        break
    
    print("[Info] Waiting for a connection\n")
    
    while True :
        try:
            conn, addr = Ss.accept()
            if len(c_sockets) < 6:
                if len(c_sockets) < 1 :
                    c_sockets.append(conn)
                    connections += 1
                    print("[Info] Chat connected: "+str(len(c_sockets))+"\n")
                    start_new_thread(t_client, (conn, addr, IpS, connections, c_sockets, secretcode))
                else :
                    soci = 0
                    for i in c_sockets :
                        if soci != len(c_sockets)-1 :
                            #print("1번"+str(soci)+" "+str(len(c_sockets)-1))
                            if "raddr=('"+addr[0] not in str(i) :
                                soci += 1
                                continue
                
                            conn.shutdown(socket.SHUT_RDWR)
                            conn.close()
                            print("[Info] Same IP connection closed\n")
                            soci += 1
                            break
                        else :
                            #print("2번"+str(soci)+" "+str(len(c_sockets)-1))
                            if "raddr=('"+addr[0] not in str(i) :
                                c_sockets.append(conn)
                                connections += 1
                                print("[Info] Chat connected: "+str(len(c_sockets))+"\n")
                                start_new_thread(t_client, (conn, addr, IpS, connections, c_sockets, secretcode))
                            else :
                                conn.shutdown(socket.SHUT_RDWR)
                                conn.close()
                                print("[Info] Same IP connection closed\n")
                            break
            else :
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                
        except Exception as e:
            print(str(e)+'\n')
        
        time.sleep(1.0)
        continue
    
    return

Server_Main()
