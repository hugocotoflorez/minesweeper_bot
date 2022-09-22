'''
VERSION 4.0

CAMBIOS:
-numpy
    volvemos a las np arrays
    optimizacion de arrays
-cambio del punto de vista de las banderas
-opcion para registrarse
-optimizacion
-codigo mas ordenado
-correccion de errores al completar el tablero
-deteccion de mina con ruptura del bucle principal
- en esta version no se hace estudio
'''
######################################################## modules #################################################
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
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
    path = '.\\chromedriver.exe' 
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path,options=options)
    action = ActionChains(driver)
    class impossible_to_find_chromedriver(Exception):pass
    if not  'chromedriver.exe' in os.listdir(): raise impossible_to_find_chromedriver('[!] CHROMEDRIVER.exe have to be in the same path as this program.')
    ############################## VPN ############################
    VPN = False
    if VPN:
        PROXY_STR = "20.81.62.32:3128" #https://sslproxies.org/
        options.add_argument('--proxy-server=%s' % PROXY_STR)
        
    ############################## LOGIN ##########################
    LOGIN = True
    credentials = {
        'username' : 'hugo coto',
        'password' : '10031003'    
    }
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
            if board[index] == 9:
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
        clicks = 0
        for index, num in enumerate(board):
            if num == 9:continue#closed cell
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
                elements[index].click() #doble click on the element 
                elements[index].click()
                clicks+=1
                
            elif len(vecinos) == n and n: 
                for i in vecinos:
                    if i not in to_right_click:to_right_click.append(i)
                    
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
            print('RANDOM!')
            elements[random.choice([i for i,a in enumerate(board) if board[i] == 9])].click()
        
    def conv(x,y):
        return x*sizeX + y
          
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
    ####################################### PLAY #########################################

    while True:#main loop
        ################### GAME OPTIONS ###########################
        #gamemode = input('[>] SELECT GAME MODE (1,2,3): ')#1- easy, 2-intermediate, 3-expert, 4 custom
        gamemode = '3'
        reference = f'https://minesweeper.online/start/{gamemode}' 
        
            
        sizeX,sizeY = get_size(gamemode)
        elements = np.empty((sizeX*sizeY,),dtype=object)
        board = np.empty((sizeX*sizeY,),dtype=np.int8)
        board[:] = 9
        board_closed_cells = np.ones((sizeX*sizeY,),dtype=np.int8)#-> 0:open, 1:closed
        board_flag_change = np.zeros((sizeX*sizeY,),dtype=np.int8)#-> -1 each cell afected by one flag, -2 if 2 flags...
        to_right_click = []
        driver.get(reference)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))#wait until page is ready to play
        global MINE
        MINE = False
        
        ####################### GAME LOOP #########################        
        set_board()
        #elements[random.randint(0,sizeX*sizeY-1)].click()
        perform_thread = Thread(target=perform,daemon=True);perform_thread.start()
        while not MINE and any(board==9):
            decide()
            get_board()
        perform_thread.join()
            
        #################### SAVE IN LOG FILE ###################
        STATUS = 'COMPLETED' if not np.count_nonzero(board==9) else 'FAILED' if MINE else 'UNKNOWN'
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.4 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s :: STATUS: {STATUS}\n')      


if __name__ == '__main__': 
    main()
        







        
        

    



    



