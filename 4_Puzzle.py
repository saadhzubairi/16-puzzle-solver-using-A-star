from copy import deepcopy
import numpy as np
import time

# takes the input of current states and evaluvates the best path to goal state
def bestsolution(state):
    bestsol = np.array([], int).reshape(-1, 16)
    count = len(state) - 1
    while count != -1:
        bestsol = np.insert(bestsol, 0, state[count]['puzzle'], 0)
        print(bestsol.reshape(-1,4,4))
        count = (state[count]['parent'])
    
    return bestsol.reshape(-1, 4, 4)
       
# this function checks for the uniqueness of the iteration(it) state, weather it has been previously traversed or not.
def all(checkarray):
    set=[]
    for it in set:
        for checkarray in it:
            return 1
        else:
            return 0

def heuristic(puzzle, goal):
    a = abs(puzzle // 4 - goal // 4)
    b = abs(puzzle % 4 - goal % 4)
    mhcost = a + b
    return sum(mhcost[1:])

# will indentify the coordinates of each of goal or initial state values
def coordinates(puzzle):
    pos = np.array(range(16))
    for p, q in enumerate(puzzle):
        pos[q] = p
    return pos

def evaluate(puzzle, goal):
    
    #Array if you want to MOVE in that POSITION of the array, you need to add HEAD to the index of your 0
    #or whatever
    steps = np.array([('up', [0,  1,  2,  3], -4),
                    ('down', [12, 13, 14, 15],  4),
                    ('left', [0,  4,  8,  12], -1),
                   ('right', [3,  7,  11, 15],  1)],
                   dtype =  [('move',  str, 1),
                              ('position', list),
                              ('head', int)])


    costg = coordinates(goal)
    parent = -1
    gn = 0
    hn = heuristic(coordinates(puzzle), costg)
    
    #Dstate is some sort of our initial list, with keys and values, containing puzzle, parent, gn, and hn
    dtstate = [ ('puzzle',  list),('parent', int),('gn',  int),('hn',  int)]
    state = np.array([(puzzle, parent, gn, hn)], dtstate)
    
    print("\nthis is our state: {}\n".format(state))
    
    # We make use of priority queues with position as keys and fn as value.
    dtpriority = [('position', int),('fn', int)]
    priority = np.array( [(0, hn)], dtpriority)
    
    lmao = 0
    
    while 1:
        
        priority = np.sort(priority, kind='mergesort', order=['fn', 'position'])     
        position, fn = priority[0]                                                 
        priority = np.delete(priority, 0, 0)  
        
        # sort priority queue using merge sort,the first element is picked for exploring 
        # remove from queue what we are exploring                   
        puzzle, parent, gn, hn = state[position]
        puzzle = np.array(puzzle)
        
        # Identify the blank_zero square in input 
        blank_zero = int(np.where(puzzle == 0)[0])
        blank_one  = int(np.where(puzzle == 1)[0])

        gn = gn + 1                              
        c = 1
        start_time = time.time()
        
        for s in steps:
            c = c + 1
            if blank_zero not in s['position']:
                # generate new state as copy of current
                openstates = deepcopy(puzzle)                   
                openstates[blank_zero], openstates[blank_zero + s['head']] = openstates[blank_zero + s['head']], openstates[blank_zero]             
                # The all function is called, if the node has been previously explored or not
                if ~(np.all(list(state['puzzle']) == openstates, 1)).any():    
                    end_time = time.time()
                    if (( end_time - start_time ) > 2):
                        print(" The 8 puzzle is unsolvable ! \n")
                        exit 
                    
                    hn = heuristic(coordinates(openstates), costg)    

                    q = np.array([(openstates, position, gn, hn)], dtstate)         
                    state = np.append(state, q, 0)

                    fn = gn + hn                                        
            
                    q = np.array([(len(state) - 1, fn)], dtpriority)    
                    priority = np.append(priority, q, 0)
                    
                    if np.array_equal(openstates, goal):                              
                    
                        return state, len(priority)
            elif blank_one not in s['position']:
                # generate new state as copy of current
                openstates = deepcopy(puzzle)                   
                openstates[blank_one], openstates[blank_one + s['head']] = openstates[blank_one + s['head']], openstates[blank_one]             
                # The all function is called, if the node has been previously explored or not
                if ~(np.all(list(state['puzzle']) == openstates, 1)).any():    
                    end_time = time.time()
                    if (( end_time - start_time ) > 2):
                        print(" The 8 puzzle is unsolvable ! \n")
                        exit 
                    
                    hn = heuristic(coordinates(openstates), costg)    

                    q = np.array([(openstates, position, gn, hn)], dtstate)         
                    state = np.append(state, q, 0)

                    fn = gn + hn                                        
            
                    q = np.array([(len(state) - 1, fn)], dtpriority)    
                    priority = np.append(priority, q, 0)
                    
                    if np.array_equal(openstates, goal):                              
                    
                        return state, len(priority)
    print("and now: ",state)
    print("\n------------------------\n")                
    return state, len(priority)

def solve(puzzle, goal):
    state, visited = evaluate(puzzle, goal) 
    bestpath = bestsolution(state)
    totalmoves = len(bestpath) - 1
    visit = len(state) - visited
    return totalmoves, visit, len(state)


puzzle = [ 
    2,  3,  4,   5,
    6,  7,  8,   9,
    10, 11, 12, 0,
    14, 1,  15, 13
]

goal=[
    2,  3,  4,   5,
    6,  7,  8,   9,
    10, 11, 12,  13,
    14, 15, 0,   1
]

print("\n{}".format(solve(puzzle, goal)))