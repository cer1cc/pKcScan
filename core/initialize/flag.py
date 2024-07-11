# pKcScan © 2024.7.11 by cer1cc is licensed under CC BY-NC-SA 4.0 
from core.initialize.color import color
import random

banner_1 = color.green("""
____________________________________________________________
                       
         ||   |||          |||||                          
         ||   ||          ||||||                          
         ||  ||           ||   ||                         
|||||    || ||     ||||   ||   ||   ||||    ||||   |||||  
||| ||   || ||    || ||   |||      || ||   || ||   ||| || 
||  ||   ||||     ||  ||   ||||    ||  ||  || ||   ||  || 
||  ||   |||||    ||        |||||  ||         ||   ||  || 
||  ||   || |||   |            ||  |       |||||   ||  || 
||  ||   ||  ||   ||  ||  ||   ||  ||  ||  || ||   ||  || 
||  ||   ||  |||  ||  ||  ||   ||  ||  || ||  ||   ||  || 
||||||   ||   ||  || ||   |||||||  || ||   || ||   ||  || 
|||||    ||    ||  ||||    |||||    ||||   ||| ||  ||  || 
||                                                        
||                                                        
-------------------------------------------------------------
                        """)

banner_2 = color.yellow(r'''
                                +---------------+
 How to find vulnerabilities?   |     pKcscan   |
                                +---------------+ 
    (╯▔＾▔)╯                        \ (•◡ •) / 
     \   |                            |   /
￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣''')


def banner():
    ddddxbx = random.choice(range(10))
    banners = {
        0: banner_1,
        1: banner_1,
        2: banner_1,
        3: banner_1,
        4: banner_1,
        5: banner_1,
        6: banner_1,
        7: banner_1,
        8: banner_1,
        9: banner_2
    }
    return banners.get(ddddxbx, banner_1)