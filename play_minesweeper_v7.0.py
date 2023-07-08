'''
VERSION 7

optimizar:

Random elige la primera celda superior izquierda (evita random sobre una lista)
'''
#################################### modules #########################
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from datetime import datetime
from time import sleep
import numpy as np
import random
import os
import time


time_dict = {}
times_dict = {}

def timer(_func=None)->None:
    def decorator(func):
        def wrapper(*args, **kwargs):
            t1 = time.perf_counter_ns()
            value = func(*args,**kwargs)
            t2 = time.perf_counter_ns()      
            time_dict.update({func.__name__:t2-t1+time_dict.get(func.__name__,0)}) 
            times_dict.update({func.__name__:times_dict.get(func.__name__,0)+1})
                
            return value
        return wrapper
    
    if _func is None:
        return decorator
    else:
        return decorator(_func)


############################ MAIN METHOD ###########################
def main():
    ######################## WEBDRIVER DATA ########################
    path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
    options = webdriver.ChromeOptions()

    ######################### SET DRIVER #############################
    driver = webdriver.Chrome(service=Service(path),options=options)
    
    ######################################### METHODS ###################################
    @timer
    def set_board():
        l = 0
        for i,elem in enumerate(driver.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div[21]/table/tbody/tr/td[1]/div/div[1]/div[4]/div[2]/div')):
            if i%(sizeX+1) != sizeX:
                elements[l] = elem
                l+=1
   
    @timer 
    def get_board():
        with ThreadPool() as pool:
            pool.map(get_cell,range(sizeX*sizeY))
   
    @timer
    def get_elem(index):
        return elements[index].get_attribute('class')
    
    @timer                  
    def get_cell(index)->int:
        if board_closed_cells[index]:
            k = get_elem(index).split()[-1][-4:]
 
            if k == 'ssed':
                return get_cell(index) 
            
            elif k == 'ype0':
                board[index] = 0  
                board_closed_cells[index] = 0
                return 2
            
            elif k ==  'pe11' or k == 'pe10':
                global hadMine
                hadMine = True
                return 0
            
            elif k ==  'osed' or k == 'flag':
                return 0
            
            else:
                board[index] = int(k[-1])
                board_closed_cells[index] = 0 
                return 1
 
                        
    @timer                    
    def check_cell(index):
        num = board[index]
        if board_closed_cells[index]:
            index+=1;return#closed cell
            
        elif num ==0:
            index+=1;return#empty cell/flag
        
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

            def task(a):
                elements[a].click()
                if board_closed_cells[a]:
                    get_cell(a)
                    
            with ThreadPool() as pool:
                pool.map(task,vecinos)
                
            b,c = invconv(vecinos[-1])
            return index - conv(b-1,c-1)
                
                
        elif len(vecinos) == n and n: 
            for i in vecinos:
                if i not in to_right_click:
                    to_right_click.append(i)
                    b,c = invconv(i)
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

                    

            return index - conv(b-1,c-1)
        
        else:
            return False
        
    @timer    
    def check_patern(pibotindex):
        pibot = board[pibotindex]
        if pibot==0 or board_closed_cells[pibotindex]:
            return False
        pibot += board_flag_change[pibotindex]
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

        pibot_linear_vecinos_numericos = [plv for plv in pibot_linear_vecinos if pibot<=board[plv]]

        pibot_linear_vecinos = [i for i in pibot_linear_vecinos if board_closed_cells[i]]

        if not pibot_linear_vecinos:
            return False
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
 
            if len([a for a in pibot_linear_vecinos if a in vecinos_del_vecino]) == len(pibot_linear_vecinos) and len(vecinos_del_vecino)>1:
                vecinos_del_vecino.remove(vecino)
                n = board[vecino] + board_flag_change[vecino] - pibot
                vecinos = [a for a in vecinos_del_vecino if a not in pibot_linear_vecinos]

                
                
                if n == 0 and len(vecinos):

                    #print('PATTERN 1')

                    for a in vecinos:
                        x,y = invconv(a)
                        
                        if board_closed_cells[a]:elements[a].click()
                        
                    return True
                    
                elif len(vecinos) == n and n: 

                    #print('PATTERN 2')

                    for i in vecinos:
                        x,y = invconv(i)
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

                    return True
                    
    @timer     
    def decide(index = 0):
        #print('decide from',index)
        fi = index
        if hadMine: return
        global last_action_israndom
        last_action_israndom = 0
        clicks = 0

        while index < sizeX*sizeY:
            #print(index, sizeX*sizeY)
            c = check_cell(index)
            if c:
                index = c
                clicks+=1
                if clicks > 20: break
            
            else:
                index+=1

        if not clicks:
            #print('pattern mode')
            
            for pibotindex in range(len(board)):
                c = check_patern(pibotindex)
                if c:
                    break
            else:

                if not fi:
                    #print('calling random from decide')
                    random_click()
                
    @timer   
    def random_click():
        
        global last_action_israndom
        last_action_israndom = 1
        index = sizeX//2*(sizeY+1)
        while board[index] !=9:
            index+=1
            index%=sizeX*sizeY
        elements[index].click()  #RANDOM CLICK
        if (g:=get_cell(index)) == 1:
            vecinos = set()
            x,y = invconv(index)
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
                if board[vi] <9:
                    #if hadMine: break
                    
                    c = check_cell(index)
                    if c:
                        decide(c)
                        break
                    
                    for pibotindex in range(len(board)):
                        c = check_patern(pibotindex)
                        if c:
                            break
                        
                        
            else:
                #print('Random after random')
                random_click()
        
        elif g == 2:
            get_board()
            decide(index-sizeX-1)   

                
    @timer         
    def conv(x,y):
        return y*sizeX + x
     
    @timer      
    def invconv(i):
        return i%sizeX, i//(sizeX)
    
    @timer
    def get_size(mode):
        match(mode):
            case 1:
                return (9,9)
            case 2:
                return (16,16)
            case 3:
                return (30,16)   
    
    
    @timer    
    def reset_board():
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top_area_face"]')))#wait until page is ready to play
            driver.find_element(By.XPATH,'//*[@id="top_area_face"]').click()
        except TimeoutError:
            global reference
            driver.get(reference)
        finally:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))#wait until page is ready to play
    

    ################### GAME OPTIONS ###########################
    
    gamemode = 3
    reference = f'https://minesweeper.online/start/{gamemode}' 
    driver.get(reference)
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))#wait until page is ready to play
    
    while True:#main loop 
        sizeX,sizeY = get_size(gamemode)
        elements = np.empty((sizeX*sizeY,),dtype=object)
        global board,board_closed_cells
        board = np.empty((sizeX*sizeY,),dtype=np.int8)
        board[:] = 9
        board_closed_cells = np.ones((sizeX*sizeY,),dtype=np.int8)#-> 0:open, 1:closed
        board_flag_change = np.zeros((sizeX*sizeY,),dtype=np.int8)#-> -1 each cell afected by one flag, -2 if 2 flags...
        to_right_click = []
        global hadMine
        hadMine = False
        global last_action_israndom 
        last_action_israndom = 0
        global random_clicks
        random_clicks = 0

        
        
        ####################### GAME LOOP #########################        
        set_board()     
        random_click()
        
        while not hadMine and any(board==9):
            decide() 
            get_board()
        
        
        #################### Time debugging #######################
        if not hadMine:
            global time_dict, times_dict
            total_time = sum(time_dict.values())   
            for name, _time in time_dict.items():
                print(f"Func: {name:10} \tExec time: ({round(_time*100/total_time,2)}%)\t{(f'{_time:,}').rjust(20):20}\t Exec times: {times_dict.get(name,0)}")
  
        
        #################### SAVE IN LOG FILE ###################
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])
        STATUS = 'COMPLETED' if not np.count_nonzero(board==9) else 'FAILED' if hadMine else 'UNKNOWN'    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.6 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s :: STATUS: {STATUS}\n')  
            
        sleep(1)  
         
        reset_board()    
        sleep(2)

if __name__ == '__main__': 
    main()
        