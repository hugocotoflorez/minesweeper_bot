'''
VERSION 5.0

CAMBIOS:
-patrones
-implementacion del algoritmo de interdependencia entre numeros por Hugo Coto Florez
'''
######################################################## modules #################################################
import webbrowser
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
from threading import Thread
from tkinter import ttk
from time import sleep
import tkinter as tk
import numpy as np
import random
import os


class main_window():
    
    def __init__(self):
        ######################## TKINTER WIDGETS ########################
        self.root = tk.Tk()
        self.root.title  ('Minesweeper Bot by Hugo Coto')
        self.Frame1 = tk.Frame(self.root);self.Frame1.pack()
        self.loop_mode_values = ['1 play','Until lose','Until failed movement','infinite']
        self.Combo = ttk.Combobox(self.Frame1, values = self.loop_mode_values)
        self.Combo.set("Loop mode")
        self.Combo.pack(padx = 5, pady = 5)
        self.mode_values = ['9x9','16x16','30x16']
        self.Combo2 = ttk.Combobox(self.Frame1, values = self.mode_values)
        self.Combo2.set("Size")
        self.Combo2.pack(padx = 5, pady = 5)
        self.username = tk.StringVar()
        username_entry = tk.Entry(self.Frame1,textvariable=self.username);username_entry.pack();username_entry.insert(tk.END,'Username')
        self.password = tk.StringVar()
        password_entry = tk.Entry(self.Frame1,textvariable=self.password,show="*");password_entry.pack();password_entry.insert(tk.END,'Password')
        
        MenuBttn = ttk.Menubutton(self.Frame1, text = "Options")
        
        self.VPN = tk.BooleanVar()
        self.INCOGNITO = tk.BooleanVar()
        self.LOGIN = tk.BooleanVar()
        
        Menu1 = tk.Menu(MenuBttn, tearoff = 0)
        
        Menu1.add_checkbutton(label = "use VPN", variable =self.VPN)
        Menu1.add_checkbutton(label = "Incognito mode", variable = self.INCOGNITO)
        Menu1.add_checkbutton(label = "Login", variable = self.LOGIN)
        
        MenuBttn["menu"] = Menu1
        
        MenuBttn.pack()
        self.FLAGS = tk.BooleanVar()
        tk.Checkbutton(self.Frame1,text='Flags',variable=self.FLAGS,onvalue=True,offvalue=False).pack()
        proxyframe = tk.Frame(self.Frame1);proxyframe.pack(padx=5,pady=5)
        self.ipaddress = tk.Entry(proxyframe);self.ipaddress.insert(tk.END,'IP Address');self.ipaddress.grid(row=0,column=0)
        self.port = tk.Entry(proxyframe);self.port.insert(tk.END,'Port');self.port.grid(row=0,column=1)
        tk.Button(proxyframe,text='Free Proxy List',command=lambda:webbrowser.open('https://sslproxies.org/')).grid(row=0,column=2)
        self.frame2 = tk.Frame(self.Frame1);self.frame2.pack()
        tk.Button(self.frame2,text='Start GAME',command=self.start).grid(padx=10,pady=10,row=0,column=0)
        tk.Button(self.frame2,text='Help',command=self.open_popup).grid(padx=10,pady=10,row=0,column=1)
        self.root.mainloop()
        
    def open_popup(self):
        top= tk.Toplevel(self.root)
        top.title('Help window')
        text = '''
        WELLCOME to Minesweeper Bot by Hugo Coto Florez.
        
        How to use:
            Change Loop mode. Options:  1 loop
                                        Until lose
                                        Until lose movement (fail when movement is not random)
                                        infinite. Stop when program crashes
            
            Change size. Options:   9x9. Beginner
                                    16x16. Intermediate
                                    30x16. Advanced. That gamemode is not optimiced
            
            VPN: Useful when they block your local ip. Slower than playing without vpn. Can cause errors, restart.
                    Write the ip address and port. You can select a free one from the list by clicking the button. 
            
            Incognito: Use if they block your local ip but not your account.                         
            
            lOGIN: select login in <Options> and write your username and password. It isnt neccesary
                    if you dont select login option.
            
            
            '''
        tk.Label(top, text= text, font=('Mistral 12')).pack()
        
    
    def start(self):
        
        ######################## WEBDRIVER DATA ########################
        path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
        options = webdriver.ChromeOptions()  
        self.loop_mode = self.loop_mode_values.index(self.Combo.get()) # 0-1 loop; 1- partida perdida; 2-partida perdida con movimiento no aleatorio; 3-infinito
        self.automode = self.mode_values.index(self.Combo2.get()) +1

        PROXY_STR = self.ipaddress.get() + ':' + self.port.get() #https://sslproxies.org/
        
        if self.VPN.get():
            options.add_argument('--proxy-server=%s' % PROXY_STR)
        
        if self.INCOGNITO.get():
            options.add_argument('--incognito')
        
        

        self.driver = webdriver.Chrome(service=Service(path),options=options)
        self.action = ActionChains(self.driver)
        
        if self.LOGIN.get():
            self.driver.get('https://minesweeper.online')
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/nav/div/div/button')))
            self.driver.find_element(By.XPATH, '//*[@id="header"]/nav/div/div/button').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/ul/li[17]/a').click()
            sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="sign_in_username"]').send_keys(self.username)
            sleep(0.1)
            self.driver.find_element(By.XPATH, '//*[@id="sign_in_password"]').send_keys(self.password)
            sleep(1)
            self.driver.find_element(By.XPATH,'//*[@id="S66"]/div/div/form/div[3]/button[2]').click()
            
        ################### GAME OPTIONS ###########################
        
        if self.automode:
           self.gamemode = str(self.automode) 
        else:self.gamemode = input('[>] SELECT GAME MODE (1,2,3): ')#1- easy, 2-intermediate, 3-expert, 4 custom
        self.reference = f'https://minesweeper.online/start/{self.gamemode}' 
           
        self.main_loop()

    ######################################### METHODS ###################################
    def set_board(self):
        l = 0
        for i,elem in enumerate(self.driver.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div[21]/table/tbody/tr/td[1]/div/div[1]/div[4]/div[2]/div')):
            if i%(self.sizeX+1) != self.sizeX:
                self.elements[l] = elem
                l+=1
     
    def get_board(self):
        for index,elem in enumerate(self.elements):
            if self.board_closed_cells[index]:
                k = elem.get_attribute('class')[-2::]
                match k:
                    case '10':
                        self.MINE = True
                    case 'ed':
                        pass
                    case 'ag':
                        pass
                    case _:
                        self.board[index] = int(k[-1])   
                        self.board_closed_cells[index] = 0 
    
    def decide(self):
        global last_action
        last_action = 0
        #print('decide')
        clicks = 0
        for index, num in enumerate(self.board):
            if self.board_closed_cells[index]:continue#closed cell
            elif num ==0:continue#empty cell/flag
            vecinos = set()
            x,y = self.invconv(index)
            n = num + self.board_flag_change[index]
            if x!=0 and y!=0: 
                vecinos.add(self.conv(x-1,y-1))
                vecinos.add(self.conv(x-1,y))
                vecinos.add(self.conv(x,y-1))
            elif x!=0:
                vecinos.add(self.conv(x-1,y))
            elif y!=0:
                vecinos.add(self.conv(x,y-1))
            if x!=self.sizeX-1 and y!=self.sizeY-1:
                vecinos.add(self.conv(x+1,y+1))
                vecinos.add(self.conv(x+1,y))
                vecinos.add(self.conv(x,y+1))
            elif x!=self.sizeX-1:
                vecinos.add(self.conv(x+1,y))
            elif y!=self.sizeY-1:
                vecinos.add(self.conv(x,y+1))  
            if x!=0 and y!=self.sizeY-1:
                vecinos.add(self.conv(x-1,y+1))   
            if x!=self.sizeX-1 and y!=0:
                vecinos.add(self.conv(x+1,y-1))

            vecinos = [i for i in vecinos if self.board_closed_cells[i]]
            if n == 0 and len(vecinos):
                
                for a in vecinos:
                    b,c = self.invconv(a)
                    #print(f'Click (normal) n=0 &len(vec) in {a}:({b}:{c})')
                    self.elements[a].click()
                clicks+=1
                
            elif len(vecinos) == n and n: 
                for i in vecinos:
                    if i not in self.to_right_click:
                        self.to_right_click.append(i)
                        self.board_closed_cells[i] = 0
                        self.board[i] = 0
                        vecinos = set()
                        x,y = self.invconv(i)
                        if x!=0 and y!=0: 
                            vecinos.add(self.conv(x-1,y-1))
                            vecinos.add(self.conv(x-1,y))
                            vecinos.add(self.conv(x,y-1))
                        elif x!=0:
                            vecinos.add(self.conv(x-1,y))
                        elif y!=0:
                            vecinos.add(self.conv(x,y-1))
                        if x!=self.sizeX-1 and y!=self.sizeY-1:
                            vecinos.add(self.conv(x+1,y+1))
                            vecinos.add(self.conv(x+1,y))
                            vecinos.add(self.conv(x,y+1))
                        elif x!=self.sizeX-1:
                            vecinos.add(self.conv(x+1,y))
                        elif y!=self.sizeY-1:
                            vecinos.add(self.conv(x,y+1))  
                        if x!=0 and y!=self.sizeY-1:
                            vecinos.add(self.conv(x-1,y+1))   
                        if x!=self.sizeX-1 and y!=0:
                            vecinos.add(self.conv(x+1,y-1))
                        for vi in vecinos:
                            self.board_flag_change[vi]-=1  
                        clicks+=1

        if not clicks:

            for pibotindex, pibot in enumerate(self.board):
                if pibot ==0 or self.board_closed_cells[pibotindex]:continue
                pibot += self.board_flag_change[pibotindex]
                brk = True
                x, y = self.invconv(pibotindex)
                px,py = x,y
                
                
                pibot_linear_vecinos = set()#no diagonals
                if x!=0 and y!=0: 
                    pibot_linear_vecinos.add(self.conv(x-1,y-1))
                    pibot_linear_vecinos.add(self.conv(x-1,y))
                    pibot_linear_vecinos.add(self.conv(x,y-1))
                elif x!=0:
                    pibot_linear_vecinos.add(self.conv(x-1,y))
                elif y!=0:
                    pibot_linear_vecinos.add(self.conv(x,y-1))
                if x!=self.sizeX-1 and y!=self.sizeY-1:
                    pibot_linear_vecinos.add(self.conv(x+1,y+1))
                    pibot_linear_vecinos.add(self.conv(x+1,y))
                    pibot_linear_vecinos.add(self.conv(x,y+1))
                elif x!=self.sizeX-1:
                    pibot_linear_vecinos.add(self.conv(x+1,y))
                elif y!=self.sizeY-1:
                    pibot_linear_vecinos.add(self.conv(x,y+1))  
                if x!=0 and y!=self.sizeY-1:
                    pibot_linear_vecinos.add(self.conv(x-1,y+1))   
                if x!=self.sizeX-1 and y!=0:
                    pibot_linear_vecinos.add(self.conv(x+1,y-1))
                #print(f'>> PLV: {pibot_linear_vecinos}',file=f)
                pibot_linear_vecinos_numericos = [plv for plv in pibot_linear_vecinos if pibot<=self.board[plv]]
                #print(f'>> PLVN: {pibot_linear_vecinos_numericos}',file=f)
                pibot_linear_vecinos = [i for i in pibot_linear_vecinos if self.board_closed_cells[i]]
                #print(f'>> PLV: {pibot_linear_vecinos}',file=f)
                if not pibot_linear_vecinos:continue
                for vecino in pibot_linear_vecinos_numericos:
                    vecinos_del_vecino = set()
                    x,y = self.invconv(vecino)
                    
                    if x!=0 and y!=0: 
                        vecinos_del_vecino.add(self.conv(x-1,y-1))
                        vecinos_del_vecino.add(self.conv(x-1,y))
                        vecinos_del_vecino.add(self.conv(x,y-1))
                    elif x!=0:
                        vecinos_del_vecino.add(self.conv(x-1,y))
                    elif y!=0:
                        vecinos_del_vecino.add(self.conv(x,y-1))
                    if x!=self.sizeX-1 and y!=self.sizeY-1:
                        vecinos_del_vecino.add(self.conv(x+1,y+1))
                        vecinos_del_vecino.add(self.conv(x+1,y))
                        vecinos_del_vecino.add(self.conv(x,y+1))
                    elif x!=self.sizeX-1:
                        vecinos_del_vecino.add(self.conv(x+1,y))
                    elif y!=self.sizeY-1:
                        vecinos_del_vecino.add(self.conv(x,y+1))
                    if x!=0 and y!=self.sizeY-1:
                        vecinos_del_vecino.add(self.conv(x-1,y+1))   
                    if x!=self.sizeX-1 and y!=0:
                        vecinos_del_vecino.add(self.conv(x+1,y-1))
                    vecinos_del_vecino = [i for i in vecinos_del_vecino if self.board_closed_cells[i]]
                    vecinos_del_vecino.append(vecino)
                    #print(f'>>>> VecVec : {vecinos_del_vecino}',file=f)  
                    #print(f'>>>> CHECK: {len([a for a in pibot_linear_vecinos if a in vecinos_del_vecino]) == len(pibot_linear_vecinos) and len(vecinos_del_vecino)>1}',file=f)
                    if len([a for a in pibot_linear_vecinos if a in vecinos_del_vecino]) == len(pibot_linear_vecinos) and len(vecinos_del_vecino)>1:
                        vecinos_del_vecino.remove(vecino)
                        n = self.board[vecino] + self.board_flag_change[vecino] - pibot
                        vecinos = [a for a in vecinos_del_vecino if a not in pibot_linear_vecinos]
                        #print(f'>>>> Num:{n} :: vec:{vecinos}')
                        
                        
                        if n == 0 and len(vecinos):
                            #print('-'*20)
                            #print('PATTERN 1')
                            #print(f'[$] PIBOT:{pibot} ({px},{py}) -> ({pibotindex}) v:{pibot_linear_vecinos}')
                            #print(f'[>] VECINO:{board[vecino]} ({x},{y}) -> ({vecino}) v:{vecinos_del_vecino}')
                            #printarr(board);printarr(board_flag_change)
                            for a in vecinos:
                                x,y = self.invconv(a)
                                
                                if self.board_closed_cells[a]:self.elements[a].click()#print(f'Click in {a}:({x}:{y})')
                                
                            break
                            
                        elif len(vecinos) == n and n: 
                            #print('-'*20)
                            #print('PATTERN 2')
                            #print(f'[$] PIBOT:{pibot} ({px},{py}) -> ({pibotindex}) v:{pibot_linear_vecinos}')
                            #print(f'[>] VECINO:{board[vecino]} ({x},{y}) -> ({vecino}) v:{vecinos_del_vecino}')
                            #printarr(board);printarr(board_flag_change)
                            for i in vecinos:
                                x,y = self.invconv(i)
                                if i not in self.to_right_click:
                                    #print(f'RClick in {i}:({x}:{y})')
                                    self.to_right_click.append(i)
                                    self.board_closed_cells[i] = 0
                                    self.board[i] = 0
                                    vecinos = set()
                                    x,y = self.invconv(i)
                                    if x!=0 and y!=0: 
                                        vecinos.add(self.conv(x-1,y-1))
                                        vecinos.add(self.conv(x-1,y))
                                        vecinos.add(self.conv(x,y-1))
                                    elif x!=0:
                                        vecinos.add(self.conv(x-1,y))
                                    elif y!=0:
                                        vecinos.add(self.conv(x,y-1))
                                    if x!=self.sizeX-1 and y!=self.sizeY-1:
                                        vecinos.add(self.conv(x+1,y+1))
                                        vecinos.add(self.conv(x+1,y))
                                        vecinos.add(self.conv(x,y+1))
                                    elif x!=self.sizeX-1:
                                        vecinos.add(self.conv(x+1,y))
                                    elif y!=self.sizeY-1:
                                        vecinos.add(self.conv(x,y+1))  
                                    if x!=0 and y!=self.sizeY-1:
                                        vecinos.add(self.conv(x-1,y+1))   
                                    if x!=self.sizeX-1 and y!=0:
                                        vecinos.add(self.conv(x+1,y-1))
                                    for vi in vecinos:
                                        self.board_flag_change[vi]-=1
 
                                                
                                

                            
                            break
                else:
                    brk = False
                if brk:break
            else:
                #print('ranodm')
                last_action = 1
                self.elements[random.choice([i for i,a in enumerate(self.board) if self.board[i] == 9])].click()  #RANDOM CLICK
    
        #input('CONTINUE?')
        
    def conv(self,x,y):
        return x*self.sizeY + y
          
    def invconv(self,i):
        return i//(self.sizeY), i%self.sizeY
    
    def perform(self):
        while not self.MINE and any(self.board==9):
            clk = [a for a in self.to_right_click]
            for a in clk:
                self.action.context_click(self.elements[a])
                self.to_right_click.remove(a)
            self.action.perform()
    
    def get_size(self,mode):
        match(mode):
            case '1':
                return (9,9)
            case '2':
                return (16,16)
            case '3':
                return (30,16)   
            
    ####################################### PLAY #########################################
    
    def main_loop(self):
        self.sizeX,self.sizeY = self.get_size(self.gamemode)
        self.elements = np.empty((self.sizeX*self.sizeY,),dtype=object)
        self.board = np.empty((self.sizeX*self.sizeY,),dtype=np.int8)
        self.board[:] = 9
        self.board_closed_cells = np.ones((self.sizeX*self.sizeY,),dtype=np.int8)#-> 0:open, 1:closed
        self.board_flag_change = np.zeros((self.sizeX*self.sizeY,),dtype=np.int8)#-> -1 each cell afected by one flag, -2 if 2 flags...
        self.to_right_click = []
        self.driver.get(self.reference)
        WebDriverWait(self.driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))#wait until page is ready to play
        self.MINE = False
        self.last_action = 0
        
        ####################### GAME LOOP #########################        
        self.set_board()
        if self.FLAGS.get():perform_thread = Thread(target=self.perform,daemon=True);perform_thread.start()
        
        while not self.MINE and any(self.board==9):
            self.decide()
            self.get_board()
            
        if self.FLAGS.get():perform_thread.join()    
        
        if self.loop_mode == 0:self.driver.quit(); return
        elif self.MINE and self.loop_mode == 1:self.driver.quit(); return
        elif self.MINE and not last_action and self.loop_mode == 2:self.driver.quit(); return
        else: self.main_loop()
    

if __name__ == '__main__': 
    main_window()
        







        
        

    



    



