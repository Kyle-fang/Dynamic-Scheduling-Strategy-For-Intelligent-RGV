'''
    当时长足够大时，RGV去到四个位置的可能性相等，依次将8个CNC选为加工第二道工序的CNC，计算出RGV在其余7个CNC取料时到这个CNC所需要的时间
    和，将这八个时间和由小到大依次排序，需要有几个B类CNC，就取前几个，相对来说这几个B类CNC的位置分布比较合理
'''

#每种情况的总时间
def Set_CNC_Position(ai_settings):
    move_time = []
    for index1 in range(1, 9):
        L1 = Determine_Location(index1)
        list = [1, 2, 3, 4, 5, 6, 7, 8]
        T = 0
        list.remove(index1)
        for index2 in list:
            L2 = Determine_Location(index2)
            if L1 - L2 == 0:
                t = 0
            elif abs(L1 - L2) == 1:
                t = ai_settings.move_one_step_time
            elif abs(L1 - L2) == 2:
                t = ai_settings.move_two_step_time
            else:
                t = ai_settings.move_three_step_time
            T = T + t

        move_time.append(T)
    #print('^',move_time)
    L = Sort(move_time)
    #print('%%%',L)
    return L


def Sort(move_time):
    L = [1, 2, 3, 4, 5, 6, 7, 8]
    for m in range(1,8):
        for n in range(1,8):
            if move_time[n-1] > move_time[n]:
                x = move_time[n-1]
                move_time[n-1] = move_time[n]
                move_time[n] = x

                y = L[n-1]
                L[n-1] = L[n]
                L[n] = y
    #print('^^', move_time)
    #print('%%',L)
    return L


def Determine_Location(step):
    if step < 3 and step > 0:
        L = 1
    elif step < 5 and step > 2:
        L = 2
    elif step < 7 and step > 4:
        L = 3
    else:
        L = 4
    return L
