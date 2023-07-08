'''
VERSION 6
edition 2023
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
from threading import Thread
from time import sleep
import numpy as np
import random
import os


############################ MAIN METHOD ###########################
def main():
    ######################## WEBDRIVER DATA ########################
    path = '.\\chromedriver.exe' if 'chromedriver.exe' in os.listdir() else ChromeDriverManager().install()
    options = webdriver.ChromeOptions()
    ############################## VPN ############################
    VPN = False
    if VPN:
        PROXY_STR = "85.14.243.31:3128" #https://geonode.com/free-proxy-list/ http-https & google
        options.add_argument('--proxy-server=%s' % PROXY_STR)
    
    
    ########################### INCOGNITO ########################
    INCOGNITO = False
    if INCOGNITO:
        options.add_argument('--incognito')
        
    ############################## LOGIN ##########################
    LOGIN = False
    credentials = {
        'username' : 'hugo bot',
        'password' : '12341234'    
    }
    ######################### SET DRIVER #############################
    driver = webdriver.Chrome(service=Service(path),options=options)
    action = ActionChains(driver)
    
    if LOGIN:
        driver.get('https://minesweeper.online')
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/nav/div/div/button')))
        driver.find_element(By.XPATH, '//*[@id="header"]/nav/div/div/button').click()
        sleep(2)
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
        #print('getting board')
        with ThreadPool() as pool:
            pool.starmap(get_cell,[(index,elem) for index,elem in enumerate(elements)])
   
                      
    def get_cell(index,*a):
        if board_closed_cells[index]:
            sleep(0.05)
            k = elements[index].get_attribute('class')
            match k.split()[-1]:
                case 'hd_pressed':
                    return get_cell(index)
                
                case 'hd_type0':
                    board[index] = 0  
                    board_closed_cells[index] = 0
                    return 0 
                   
                case 'hd_type11' | 'hd_type10':
                    global hadMine
                    hadMine = True
                    return 1
                
                case 'hd_closed':
                    return 2,k
                
                case 'flag':
                    return 3
                
                case _:
                    board[index] = int(k[-1])   
                    board_closed_cells[index] = 0 
                    return 4 
        else:
            return 5
                        
                        
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
            for a in vecinos:
                b,c = invconv(a)
                elements[a].click()
                get_cell(a)
                

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
    
        
        
            
            
        
     
    #def decide_cell(index):
        
                     
         
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
                
       
    def random_click():
        
        global last_action_israndom
        last_action_israndom = 1
        l = [i for i,a in enumerate(board) if a == 9]
        if l:
            index = random.choice(l)
            elements[index].click()  #RANDOM CLICK
            if (g:=get_cell(index)) == 4:
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
                    if 0< board[vi] <9:
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
                    random_click()
                
        else:
            get_board()
            decide(index-sizeX-1)

             
    def conv(x,y):
        return y*sizeX + x
     
          
    def invconv(i):
        return i%sizeX, i//(sizeX)
    
    
    def perform():
        while not hadMine and any(board==9):
            clk = [a for a in to_right_click]
            for a in clk:
                
                action.context_click(elements[a])
                to_right_click.remove(a)
            action.perform()
    
    
    def get_size(mode):
        match(mode):
            case 1:
                return (9,9)
            case 2:
                return (16,16)
            case 3:
                return (30,16)   
    
            
    def printarr(arr):
        ...
        #print('-'*2*sizeX)
        #print('\n'.join([' '.join([str(a) for a in arr[b*sizeX:b*sizeX+sizeX]]).replace('0',' ').replace('9','#') for b in range(sizeY)]))     
        #print('-'*2*sizeX)
    
    #TODO: fix this    
    def save_screenshot(mode):
        files = [a for a in os.listdir('.\\screenshots') if a.startswith(str(mode))]
        filename = 'screenshots\\'+str(gamemode)+'_'+str(int(files[-1].split('_')[1].rstrip('.png'))+1)+'.png' if files else 'screenshots\\'+str(gamemode)+str(0)+'.png'
        #print('save_screenshot',filename)
        sleep(1)
        driver.save_screenshot(filename)
     
        
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
        FLAGS = True
        #os.system('cls' if sys.platform == 'win32' else 'clear')
        
        
        ####################### GAME LOOP #########################        
        set_board()
        if FLAGS:
            perform_thread = Thread(target=perform,daemon=True)
            perform_thread.start()
            
        random_click()
        
        while not hadMine and any(board==9):
            decide() 
            get_board()
        #################### after WIN / LOSE ###################### 
        if hadMine and not last_action_israndom: input('Continue?')
        if FLAGS:perform_thread.join()
        
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])
        
        
        capture_great_games = False
        if capture_great_games and not hadMine:
            #print('SHOULD CAPTURE')
            match gamemode:
                case 1:
                    if time == 0:
                        save_screenshot(gamemode)
                case 2:
                    if time <= 10:
                        save_screenshot(gamemode)
                case 3:
                    save_screenshot(gamemode)
                    
                case _:
                    #print(repr(gamemode),time)
                    ...
        
            
        #################### SAVE IN LOG FILE ###################
        STATUS = 'COMPLETED' if not np.count_nonzero(board==9) else 'FAILED' if hadMine else 'UNKNOWN'    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.6 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s :: STATUS: {STATUS}\n')  
            
        sleep(1)    
        reset_board()    
        sleep(2)

if __name__ == '__main__': 
    main()
        

