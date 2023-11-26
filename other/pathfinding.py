from random import choice

def min_turns1(starting_direction, target_direction):
    cw_dircs=['north','east','south','west']
    acw_dircs=['south','west','south','east']
    cw_turns=cw_dircs.index(target_direction)-cw_dircs.index(starting_direction)
    acw_turns=acw_dircs.index(target_direction)-acw_dircs.index(starting_direction)
    if abs(cw_turns)<abs(acw_turns):
        return cw_turns,'right'
    elif abs(cw_turns)==abs(acw_turns):
        print(cw_turns,acw_turns)
        if cw_turns>acw_turns:
            return cw_turns,'right'
        else:
            return acw_turns,'left'
    else:
        return acw_turns,'left'
def min_turns(starting_direction, target_direction):
    dircs=['north','east','south','west']
    turns=dircs.index(target_direction)-dircs.index(starting_direction)
    return turns
def get_path(starting_pos, starting_direction, target_pos):
    diff_pos=target_pos[0]-starting_pos[0], target_pos[1]-starting_pos[1]
    tm=[]
    if diff_pos[0]>0:
        t=min_turns(starting_direction,'east')
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
        for i in range(diff_pos[0]):
            tm.append('forward')
        t=min_turns('east',starting_direction)
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
    elif diff_pos[0]<0:
        t=min_turns(starting_direction,'west')
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
        for i in range(abs(diff_pos[0])):
            tm.append('forward')
        t=min_turns('west',starting_direction)
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
    if diff_pos[1]>0:
        t=min_turns(starting_direction,'south')
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
        for i in range(diff_pos[1]):
            tm.append('forward')
        t=min_turns('south',starting_direction)
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
    elif diff_pos[1]<0:
        t=min_turns(starting_direction,'north')
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
        for i in range(abs(diff_pos[1])):
            tm.append('forward')
        t=min_turns('north',starting_direction)
        for i in range(abs(t)):
            if t<0:
                tm.append('left')
            else:
                tm.append('right')
    return tm

if __name__=='__main__':
    print(get_path((4,10),'south',(10,9)))