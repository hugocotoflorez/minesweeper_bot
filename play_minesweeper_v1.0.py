'''
VERSION 1.0

PROBLEMAS:
-Ingame:
    solo reconoce patrones individuales
    
-Script:
    try - except to solve non issues problems
    bad optimization
    right click fk*** slow
'''
######################################################## modules #################################################
from time import perf_counter
t1 = perf_counter()
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from datetime import datetime
from colorama import Fore
import os
######################################################## data #################################################

times = {
   'gb' :[],
   'cl' :[],
   'la' :[],
   'rc' :[],
   'dc' :[],
   'ap' :[],
   'cv' :[]
}

def main():
    VPN = False
    gamemode = input('[>] SELECT GAME MODE (1,2,3): ')#1- easy, 2-intermediate, 3-expert, 4 custom
    reference = f'https://minesweeper.online/start/{gamemode}' 
    #reference = 'https://minesweeper.online/es/game/1481756002'
    path = '.\\chromedriver.exe'
    options = webdriver.ChromeOptions()
    if VPN:
        PROXY_STR = "35.230.142.201:8080" #https://sslproxies.org/
        options.add_argument('--proxy-server=%s' % PROXY_STR)
    driver = webdriver.Chrome(executable_path=path,options=options)
    action = ActionChains(driver)

    class impossible_to_find_chromedriver(Exception):pass
    if not  'chromedriver.exe' in os.listdir(): raise impossible_to_find_chromedriver('File have to be in the same path as this program is in')
        
    def get_size(mode):
        match(mode):
            case '1':
                return (9,9)
            case '2':
                return (16,16)
            case '3':
                return (30,16) 
            
    sizeX,sizeY = get_size(gamemode)
    board_elems = [None for n in range(sizeX*sizeY)]
    board_items = {n:list() for n in range(8,-1,-1)}#este 9 no es de tamano
    board_emp = {'d':list(), 'g':list()}

    driver.get(reference)

    ######################################################## methods #################################################
    def set_board():
        l = 0
        for i,elem in enumerate(driver.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div[21]/table/tbody/tr/td[1]/div/div[1]/div[4]/div[2]/div')):
            if i%(sizeX+1) != sizeX:
                board_elems[l] = elem
                l+=1
        
        
            
    def get_board():
        t= perf_counter()
        for i,elem in enumerate(board_elems):
    
            k= elem.get_attribute('class')[-1]
            if k not in ('d','g'):
                list_add(board_items[int(k)],i)
            else:list_add(board_emp[k],i)

        
        times['gb'].append(perf_counter()-t)
                
    def clear(d):
        t = perf_counter()
        for i,_ in d.items():d[i] = list()

        times['cl'].append(perf_counter()-t)
        
    def list_add(l:list,item):
        t = perf_counter()
        if item not in l: 
            l.append(item)
        
        times['la'].append(perf_counter()-t)
        
    def rclick(element,c=[]):
        t = perf_counter()
        if element not in c:
            action.context_click(on_element=element)
            c.append(element)
    
        times['rc'].append(perf_counter()-t)
        
    def decide():
        t = perf_counter()
        for num,posis in board_items.items():
            brk = False
            if num == 0:continue
            for index in posis:
                vecinos = []
                x,y = invconv(index)
                n = num
                if x!=0 and y!=0: 
                    list_add(vecinos,conv(x-1,y-1))
                    list_add(vecinos,conv(x-1,y))
                    list_add(vecinos,conv(x,y-1))
                elif x!=0:list_add(vecinos,conv(x-1,y))
                elif y!=0:list_add(vecinos,conv(x,y-1))
                if x!=sizeX-1 and y!=sizeY-1:
                    list_add(vecinos,conv(x+1,y+1))
                    list_add(vecinos,conv(x+1,y))
                    list_add(vecinos,conv(x,y+1))
                elif x!=sizeX-1:list_add(vecinos,conv(x+1,y))
                elif y!=sizeY-1:list_add(vecinos,conv(x,y+1))  
                if x!=0 and y!=sizeY-1:list_add(vecinos,conv(x-1,y+1))   
                if x!=sizeX-1 and y!=0:list_add(vecinos,conv(x+1,y-1))
                
                for i in vecinos:
                    if i in board_emp['g']:
                        n-=1
                vecinos = [i for i in vecinos if i in board_emp['d']]

                if n == 0 and len(vecinos):
                    for a in vecinos:
                        board_elems[a].click()
                    brk = True
                    
                elif len(vecinos) == n and n: 
                    for a in vecinos:
                        rclick(board_elems[a])
                    brk = True

            if brk:break
        
        else: 
            print('RANDOM MOVE')
            board_elems[random.choice(board_emp['d'])].click()
        
    
        times['dc'].append(perf_counter()-t)
        

    def conv(x,y):
        t=perf_counter()
        k = x*sizeX + y
        times['cv'].append(perf_counter()-t)
        return k
        
        
    def invconv(i):
        t=perf_counter()
        k = i//(sizeY), i%sizeY
        times['cv'].append(perf_counter()-t)
        return  k
    

    ############################################# PLAY ##############################################################
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cell_0_0"]')))
    set_board()
    board_elems[random.randint(0,sizeX*sizeY-1)].click()

    try:
        while True:
            get_board()
            decide()
            t= perf_counter() 
            action.perform() 
            times['ap'].append(perf_counter()-t)
            clear(board_emp)
    except: pass
    try:
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.1 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s (program run time: {perf_counter()-t1})\n')      
    except:pass
    
    ############################# STUDY #################################
    for name,t in times.items():
        print(f'{Fore.GREEN} {name} TIME STUDY: Avg:{sum(t)/len(t)/10**9}. Max:{max(t)}. Total time:{sum(t)/10**9}. Total relative:{sum(t)/(perf_counter()-t1)*100}%.{Fore.RESET}')
    
if __name__ == '__main__': 
    while True: main()
        







        
        

    



    



