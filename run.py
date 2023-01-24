import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def check_pe_area(pe_area):
    
    x,y = pe_area.shape
    
    for i in range(x):
        for j in range(y):
            if pe_area[i][j] > 1:
                return False
    return True

# make 16 by 19 array of zeros
pe_area = np.zeros((16, 19))

block_a = np.ones((3, 3))
block_b = np.ones((2, 2))
block_c = np.ones((1, 5))
block_d = np.ones((2, 5))
block_e = np.ones((3, 4))
block_f = np.ones((6, 1))

import_block_list = [
    [block_a, block_d, block_e],
    [block_b, block_b, block_c],
    [block_e, block_c, block_c],
    [block_e, block_e, block_b],
    [block_b, block_b, block_e],
    [block_a, block_a, block_b],
    [block_b, block_a, block_b],
    [block_b, block_c, block_d],
    [block_b, block_c, block_a],
    [block_e, block_d, block_e]
]

export_block_schedule_list = [
    [3, 6, 5], [8, 10, 7], [11, 12, 9],
    [12, 12, 13], [15, 17, 15],
    [16, 18, 17], [19, 20, 19], [20, 21, 22],
    [22, 21, 23], [23, 23, 24]
]

days = 30

export_block_list = [ [] for _ in range(days)]
pe_height, pe_width = pe_area.shape
temp_pe_area = None
flag = False
for day in range(days):    
    try:
        block_list = import_block_list[day]
        block_duration_days = export_block_schedule_list[day]
    except IndexError:
        block_list = []
        block_duration_days = [] 
    
    
    
    if len(export_block_list[day]) > 0:
        for block, (y, x) in export_block_list[day]:
            pe_area[y:y+block.shape[0], x:x+block.shape[1]] = \
                pe_area[y:y+block.shape[0], x:x+block.shape[1]] - block
            sns.heatmap(pe_area, annot=True,  linewidths=.5, cmap="YlGnBu")
            plt.show()
        
    
    for block, duraction_day in zip(block_list, block_duration_days):
        block_size_y, block_size_x = block.shape 
        for y in range(pe_height-block_size_y+1):
            for x in range(pe_width-block_size_x+1):
                temp_pe_area = pe_area.copy()
                temp_pe_area[y:y+block_size_y, x:x+block_size_x] = \
                    temp_pe_area[y:y+block_size_y, x:x+block_size_x] + block
                if check_pe_area(temp_pe_area):
                    pe_area = temp_pe_area.copy()
                    export_block_list[duraction_day].append((block, (y, x)))
                    flag = True
                    break
                else:
                    continue
            if flag:
                flag = False
                break
       
        sns.heatmap(pe_area, annot=True,  linewidths=.5, cmap="YlGnBu")
        plt.show()
            
        
        
        