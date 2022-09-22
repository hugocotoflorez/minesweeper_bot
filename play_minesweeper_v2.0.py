'''
VERSION 2.0

POTENTIAL UPDATES:
-arrays
    numpy arrays

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
import numpy as np
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
    NOINDEX = 90
    VPN = 0
    gamemode = input('[>] SELECT GAME MODE (1,2,3): ')#1- easy, 2-intermediate, 3-expert, 4 custom
    reference = f'https://www.minesweeper.online/start/{gamemode}' 
    path = '.\\chromedriver.exe'
    options = webdriver.ChromeOptions()
    if VPN:
        PROXY_STR = "8.219.97.248:80" #https://sslproxies.org/
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
    board_elems = np.empty([sizeX,sizeY],dtype=object)
    board_items = np.full([8,sizeX*sizeY],fill_value=NOINDEX,dtype=np.int32) #value 90 is out of range
    board_emp = np.zeros([sizeX*sizeY],dtype=np.int32)#d
    board_flag= np.zeros([sizeX*sizeY],dtype=np.int32)#g
    driver.get(reference)

    ######################################################## methods #################################################
    def set_board():
        l = 0
        for i,elem in enumerate(driver.find_elements(By.XPATH,'/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div[21]/table/tbody/tr/td[1]/div/div[1]/div[4]/div[2]/div')):
            if i%(sizeX+1) != sizeX:
                x,y = invconv(l)
                board_elems[x,y] = elem
                l+=1
        
        
            
    def get_board():
        t= perf_counter()
        
        for a in range(board_elems.shape[0]):
            for b in range(board_elems.shape[1]):
                elem = board_elems[a,b]
                i = conv(a,b)
                l,m = invconv(i)
                k=elem.get_attribute('class')[-1]
                if k ==  'd':
                   board_emp[i] = i
                        
                elif k == 'g':
                    board_flag[i] = i
                    board_emp[i] = 0
                         
                else:
                    arr_add(board_items,int(k),i,i)
                    board_emp[i] = 0
                        

        
        times['gb'].append(perf_counter()-t)
       
    def list_add(l:list,item):
        t = perf_counter()
        if item not in l: 
            l.append(item)
        times['la'].append(perf_counter()-t)
        
    def arr_add(arr,index1,index2,item):
        t = perf_counter()
        if item not in arr: 
            arr[index1,index2] = item
        times['la'].append(perf_counter()-t)
        
    def rclick(element,c=[]):
        t = perf_counter() 
        if element not in c:
            action.context_click(on_element=element)
            c.append(element)
        times['rc'].append(perf_counter()-t)
        
    def decide():
        t = perf_counter()
        for num in range(board_items.shape[0]):
            brk = False
            if num == 0:continue
            for index in board_items[num]:
                if index == NOINDEX:continue
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
                    if i in board_flag:
                        n-=1
                vecinos = [ix for ix in vecinos if ix in board_emp]

                if n == 0 and len(vecinos):
                    for a in vecinos:
                        l,m = invconv(a)
                        board_elems[l,m].click()
                        board_emp[a] = 0
                    brk = True
                    
 
                elif len(vecinos) == n and n: 
                    for a in vecinos:
                        l,m = invconv(a)
                        rclick(board_elems[l,m])
                        board_flag[a] = a
                        board_emp[a] = 0
                    brk = True
            if brk:break
        else:
            random.choice(board_elems.flat).click()

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
    board_elems[random.randint(0,sizeX-1),random.randint(0,sizeY-1)].click()

    try:
        while True:
            get_board()
            decide()
            t= perf_counter() 
            action.perform() 
            times['ap'].append(perf_counter()-t)
        
        
    except: pass

    
    ############################# SAVE #################################
   
    try:
        time = sum([int(e)*(10**i) for i,e in enumerate([element.get_attribute('class')[-1] for element in driver.find_elements(By.XPATH,'//*[@id="top_area"]/div[2]/div[4]/div[2]/div')][-1::-2])if e in [str(n) for n in range(10)]])    
        with open('MINESWEEPER_LOG.txt','a') as f:
            f.write(f'GAME v.2 (mode={gamemode}) on {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")} :: time: {time}s (program run time: {perf_counter()-t1})\n')      
    except:pass

    
    ############################# STUDY #################################
    for name,t in times.items():
        print(f'{Fore.GREEN} {name} TIME STUDY: Avg:{sum(t)/len(t)/10**9}. Max:{max(t)}. Total time:{sum(t)/10**9}. Total relative:{sum(t)/(perf_counter()-t1)*100}%.{Fore.RESET}')
    
if __name__ == '__main__': 
    while True: main()
        







        
        

    



    



