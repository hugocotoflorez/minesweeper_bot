'''
VERSION 5.0

CAMBIOS:
-patrones
-implementacion del algoritmo de interdependencia entre numeros por Hugo Coto Florez
'''
######################################################## modules #################################################
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
from datetime import datetime
from threading import Thread
from time import sleep
import numpy as np
import random
import sys
import os

############################ MAIN METHOD ###########################
def main():
    ######################## WEBDRIVER DATA ########################
    path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    ############################## VPN ############################
    VPN = True
    if VPN:
        PROXY_STR = "8.219.97.248:80" #https://sslproxies.org/
        options.add_argument('--proxy-server=%s' % PROXY_STR)
    
    ########################### INCOGNITO ########################
    INCOGNITO = False
    if INCOGNITO:
        options.add_argument('--incognito')
        
    ############################## LOGIN ##########################
    LOGIN = False
    credentials = {
        'username' : 'hugo coto',
        'password' : '10031003'    
    }
    ######################### SET DRIVER #############################
    driver = webdriver.Chrome(service=Service(path),options=options)
    action = ActionChains(driver)
    
    if LOGIN:
        driver.get('https://minesweeper.online')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/nav/div/div/button')))
        driver.find_element(By.XPATH, '//*[@id="header"]/nav/div/div/button').click()
        sleep(1)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/ul/li[17]/a').click()
        sleep(1)
        driver.find_element(By.XPATH, '//*[@id="sign_in_username"]').send_keys(credentials['username'])
        sleep(0.1)
        driver.find_element(By.XPATH, '//*[@id="sign_in_password"]').send_keys(credentials['password'])
        sleep(1)
        driver.find_element(By.XPATH,'//*[@id="S66"]/div/div/form/div[3]/button[2]').click()

    ######################################### METHODS ###################################
    def set_board():
        l = 0
        for i,elem in enumerate(driver.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div[21]/table/tbody/tr/td[1]/div/div[1]/div[4]/div[2]/div')):
            if i%(sizeX+1) != sizeX:
                elements[l] = elem
                l+=1
     
    def get_board():
        for index,elem in enumerate(elements):
            if board_closed_cells[index]:
                k = elem.get_attribute('class')[-2::]
                match k:
                    case '10':
                        global MINE
                        MINE = True
                    case 'ed':
                        pass
                    case 'ag':
                        pass
                    case _:
                        board[index] = int(k[-1])   
                        board_closed_cells[index] = 0 
    
    def decide():
        global last_action
        last_action = 0
        #print('decide')
        clicks = 0
        for index, num in enumerate(board):
            if board_closed_cells[index]:continue#closed cell
            elif num ==0:continue#empty cell/flag
            vecinos = set()
            x,y = invconv(index)
            n = num + board_flag_change[index]
            if x!=0 and y!=0: 
                vecinos.add(conv(x-1,y-1))
                vecinos.add(conv(x-1,y))
                vecinos.add(conv(x,y-1))
            elif x!=0:
                vecinos.add(conv(x-1,y))
            elif y!=0:
                vecinos.add(conv(x,y-1))
            if x!=sizeX-1 and y!=sizeY-1:
                vecinos.add(conv(x+1,y+1))
                vecinos.add(conv(x+1,y))
                vecinos.add(conv(x,y+1))
            elif x!=sizeX-1:
                vecinos.add(conv(x+1,y))
            elif y!=sizeY-1:
                vecinos.add(conv(x,y+1))  
            if x!=0 and y!=sizeY-1:
                vecinos.add(conv(x-1,y+1))   
            if x!=sizeX-1 and y!=0:
                vecinos.add(conv(x+1,y-1))

            vecinos = [i for i in vecinos if board_closed_cells[i]]
            if n == 0 and len(vecinos):
                
                for a in vecinos:
                    b,c = invconv(a)
                    #print(f'Click (normal) n=0 &len(vec) in {a}:({b}:{c})')
                    elements[a].click()
                clicks+=1
                
            elif len(vecinos) == n and n: 
                for i in vecinos:
                    if i not in to_right_click:
                        to_right_click.append(i)
                        board_closed_cells[i] = 0
                        board[i] = 0
                        vecinos = set()
                        x,y = invconv(i)
                        if x!=0 and y!=0: 
                            vecinos.add(conv(x-1,y-1))
                            vecinos.add(conv(x-1,y))
                            vecinos.add(conv(x,y-1))
                        elif x!=0:
                            vecinos.add(conv(x-1,y))
                        elif y!=0:
                            vecinos.add(conv(x,y-1))
                        if x!=sizeX-1 and y!=sizeY-1:
                            vecinos.add(conv(x+1,y+1))
                            vecinos.add(conv(x+1,y))
                            vecinos.add(conv(x,y+1))
                        elif x!=sizeX-1:
                            vecinos.add(conv(x+1,y))
                        elif y!=sizeY-1:
                            vecinos.add(conv(x,y+1))  
                        if x!=0 and y!=sizeY-1:
                            vecinos.add(conv(x-1,y+1))   
                        if x!=sizeX-1 and y!=0:
                            vecinos.add(conv(x+1,y-1))
                        for vi in vecinos:
                            board_flag_change[vi]-=1  
                        clicks+=1

        if not clicks:

            for pibotindex, pibot in enumerate(board):
                if pibot ==0 or board_closed_cells[pibotindex]:continue
                pibot += board_flag_change[pibotindex]
                brk = True
                x, y = invconv(pibotindex)
                px,py = x,y
                
                
                pibot_linear_vecinos = set()#no diagonals
                if x!=0 and y!=0: 
                    pibot_linear_vecinos.add(conv(x-1,y-1))
                    pibot_linear_vecinos.add(conv(x-1,y))
                    pibot_linear_vecinos.add(conv(x,y-1))
                elif x!=0:
                    pibot_linear_vecinos.add(conv(x-1,y))
                elif y!=0:
                    pibot_linear_vecinos.add(conv(x,y-1))
                if x!=sizeX-1 and y!=sizeY-1:
                    pibot_linear_vecinos.add(conv(x+1,y+1))
                    pibot_linear_vecinos.add(conv(x+1,y))
                    pibot_linear_vecinos.add(conv(x,y+1))
                elif x!=sizeX-1:
                    pibot_linear_vecinos.add(conv(x+1,y))
                elif y!=sizeY-1:
                    pibot_linear_vecinos.add(conv(x,y+1))  
                if x!=0 and y!=sizeY-1:
                    pibot_linear_vecinos.add(conv(x-1,y+1))   
                if x!=sizeX-1 and y!=0:
                    pibot_linear_vecinos.add(conv(x+1,y-1))
                #print(f'>> PLV: {pibot_linear_vecinos}',file=f)
                pibot_linear_vecinos_numericos = [plv for plv in pibot_linear_vecinos if pibot<=board[plv]]
                #print(f'>> PLVN: {pibot_linear_vecinos_numericos}',file=f)
                pibot_linear_vecinos = [i for i in pibot_linear_vecinos if board_closed_cells[i]]
                #print(f'>> PLV: {pibot_linear_vecinos}',file=f)
                if not pibot_linear_vecinos:continue
                for vecino in pibot_linear_vecinos_numericos:
                    vecinos_del_vecino = set()
                    x,y = invconv(vecino)
                    
                    if x!=0 and y!=0: 
                        vecinos_del_vecino.add(conv(x-1,y-1))
                        vecinos_del_vecino.add(conv(x-1,y))
                        vecinos_del_vecino.add(conv(x,y-1))
                    elif x!=0:
                        vecinos_del_vecino.add(conv(x-1,y))
                    elif y!=0:
                        vecinos_del_vecino.add(conv(x,y-1))
                    if x!=sizeX-1 and y!=sizeY-1:
                        vecinos_del_vecino.add(conv(x+1,y+1))
                        vecinos_del_vecino.add(conv(x+1,y))
                        vecinos_del_vecino.add(conv(x,y+1))
                    elif x!=sizeX-1:
                        vecinos_del_vecino.add(conv(x+1,y))
                    elif y!=sizeY-1:
                        vecinos_del_vecino.add(conv(x,y+1))
                    if x!=0 and y!=sizeY-1:
                        vecinos_del_vecino.add(conv(x-1,y+1))   
                    if x!=sizeX-1 and y!=0:
                        vecinos_del_vecino.add(conv(x+1,y-1))
                    vecinos_del_vecino = [i for i in vecinos_del_vecino if board_closed_cells[i]]
                    vecinos_del_vecino.append(vecino)
                    #print(f'>>>> VecVec : {vecinos_del_vecino}',file=f)  
                    #print(f'>>>> CHECK: {len([a for a in pibot_linear_vecinos if a in vecinos_del_vecino]) == len(pibot_linear_vecinos) and len(vecinos_del_vecino)>1}',file=f)
                    if len([a for a in pibot_linear_vecinos if a in vecinos_del_vecino]) == len(pibot_linear_vecinos) and len(vecinos_del_vecino)>1:
                        vecinos_del_vecino.remove(vecino)
                        n = board[vecino] + board_flag_change[vecino] - pibot
                        vecinos = [a for a in vecinos_del_vecino if a not in pibot_linear_vecinos]
                        #print(f'>>>> Num:{n} :: vec:{vecinos}')
                        
                        
                        if n == 0 and len(vecinos):
                            #print('-'*20)
                            #print('PATTERN 1')
                            #print(f'[$] PIBOT:{pibot} ({px},{py}) -> ({pibotindex}) v:{pibot_linear_vecinos}')
                            #print(f'[>] VECINO:{board[vecino]} ({x},{y}) -> ({vecino}) v:{vecinos_del_vecino}')
                            #printarr(board);printarr(board_flag_change)
                            for a in vecinos:
                                x,y = invconv(a)
                                
                                if board_closed_cells[a]:elements[a].click()#print(f'Click in {a}:({x}:{y})')
                                
                            break
                            
                        elif len(vecinos) == n and n: 
                            #print('-'*20)
                            #print('PATTERN 2')
                            #print(f'[$] PIBOT:{pibot} ({px},{py}) -> ({pibotindex}) v:{pibot_linear_vecinos}')
                            #print(f'[>] VECINO:{board[vecino]} ({x},{y}) -> ({vecino}) v:{vecinos_del_vecino}')
                            #printarr(board);printarr(board_flag_change)
                            for i in vecinos:
                                x,y = invconv(i)
                                if i not in to_right_click:
                                    #print(f'RClick in {i}:({x}:{y})')
                                    to_right_click.append(i)
                                    board_closed_cells[i] = 0
                                    board[i] = 0
                                    vecinos = set()
                                    x,y = invconv(i)
                                    if x!=0 and y!=0: 
                                        vecinos.add(conv(x-1,y-1))
                                        vecinos.add(conv(x-1,y))
                                        vecinos.add(conv(x,y-1))
                                    elif x!=0:
                                        vecinos.add(conv(x-1,y))
                                    elif y!=0:
                                        vecinos.add(conv(x,y-1))
                                    if x!=sizeX-1 and y!=sizeY-1:
                                        vecinos.add(conv(x+1,y+1))
                                        vecinos.add(conv(x+1,y))
                                        vecinos.add(conv(x,y+1))
                                    elif x!=sizeX-1:
                                        vecinos.add(conv(x+1,y))
                                    elif y!=sizeY-1:
                                        vecinos.add(conv(x,y+1))  
                                    if x!=0 and y!=sizeY-1:
                                        vecinos.add(conv(x-1,y+1))   
                                    if x!=sizeX-1 and y!=0:
                                        vecinos.add(conv(x+1,y-1))
                                    for vi in vecinos:
                                        board_flag_change[vi]-=1
 
                                                
                                

                            
                            break
                else:
                    brk = False
                if brk:break
            else:
                #print('ranodm')
                last_action = 1
                elements[random.choice([i for i,a in enumerate(board) if board[i] == 9])].click()  #RANDOM CLICK
    
        #input('CONTINUE?')
        
    def conv(x,y):
        return x*sizeY + y
          
    def invconv(i):
        return i//(sizeY), i%sizeY
    
    def perform():
        while not MINE and any(board==9):
            clk = [a for a in to_right_click]
            for a in clk:
                action.context_click(elements[a])
                to_right_click.remove(a)
            action.perform()
    
    def get_size(mode):
        match(mode):
            case '1':
                return (9,9)
            case '2':
                return (16,16)
            case '3':
                return (30,16)   
            
    def printarr(arr):
        print('-'*2*sizeY)
        print('\n'.join([' '.join([str(a) for a in arr[b*sizeY:b*sizeY+sizeY]]) for b in range(sizeX)]))     
        print('-'*2*sizeY)
    ####################################### PLAY #########################################

    while True:#main loop
        ################### GAME OPTIONS ###########################
        automode = 0
        if automode:
           gamemode = str(automode) 
        else:gamemode = input('[>] SELECT GAME MODE (1,2,3): ')#1- easy, 2-intermediate, 3-expert, 4 custom
        reference = f'https://minesweeper.online/start/{gamemode}' 
        
            
        sizeX,sizeY = get_size(gamemode)
        elements = np.empty((sizeX*sizeY,),dtype=object)
        board = np.empty((sizeX*sizeY,),dtype=np.int8)
        board[:] = 9
        board_closed_cells = np.ones((sizeX*sizeY,),dtype=np.int8)#-> 0:open, 1:closed
        board_flag_change = np.zeros((sizeX*sizeY,),dtype=np.int8)#-> -1 each cell afected by one flag, -2 if 2 flags...
        to_right_click = []
        driver.get(reference)
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))#wait until page is ready to play
        global MINE
        MINE = False
        global last_action 
        last_action = 0
        FLAGS = True
        os.system('cls' if sys.platform == 'win32' else 'clear')
        ####################### GAME LOOP #########################        
        set_board()
        if FLAGS:perform_thread = Thread(target=perform,daemon=True);perform_thread.start()
        
        while not MINE and any(board==9):
            decide()
            get_board()
        
        if MINE and not last_action: input()
        #elif MINE:input()
        if FLAGS:perform_thread.join()
        
            
        #################### SAVE IN LOG FILE ###################
        STATUS = 'COMPLETED' if not np.count_nonzero(board==9) else 'FAILED' if MINE else 'UNKNOWN'
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.5 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s :: STATUS: {STATUS}\n')      


if __name__ == '__main__': 
    main()
        







        
        

    



    



