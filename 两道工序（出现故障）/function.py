import set_CNC_position as SCP

#根据第一道工序和第二道工序所需的时间来决定CNC的位置上和两种CNC的比例
def Decision_Ratio(ai_settings, first_process_time, second_process_time):
    second_CNC_number = int((second_process_time / (first_process_time + second_process_time)) * 8)
    #second_CNC_number = (second_process_time / (first_process_time + second_process_time)) * 8
    #得到B类CNC位置以时间长短排序的列表
    L = SCP.Set_CNC_Position(ai_settings)
    print('&', L)
    ai_settings.CNC_type = [1, 1, 1, 1, 1, 1, 1, 1]
    '''
    if first_CNC_number == 1:
        L1 = L[0:7]
        for i in L1:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 2:
        L2 = L[0:6]
        for i in L2:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 3:
        L3 = L[0:5]
        for i in L3:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 4:
        L4 = L[0:4]
        for i in L4:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 5:
        L5 = L[0:3]
        for i in L5:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 6:
        L6 = L[0:2]
        for i in L6:
            ai_settings.CNC_type[i - 1] = 2
    elif first_CNC_number == 7:
        L7 = L[0:1]
        for i in L7:
            ai_settings.CNC_type[i - 1] = 2
    '''
    if (second_CNC_number+1) == 4:
        for i in [1,3,5,7]:
            ai_settings.CNC_type[i] = 2

        ai_settings.Locate_RGV = 4
        ai_settings.CNC_remaining_processing_time = [256, 0, 304, 0, 352, 0, 400, 0]
        return second_CNC_number

    elif second_CNC_number == 5:
        for i in [1, 2, 3, 6, 7]:
            ai_settings.CNC_type[i] = 2

        ai_settings.Locate_RGV = 3
        ai_settings.CNC_remaining_processing_time = [174, 0, 0, 0, 245, 280, 0, 0]
        print('!!!!!')
        return second_CNC_number
    elif second_CNC_number == 2:
        for i in [3, 4]:
            ai_settings.CNC_type[i] = 2
        ai_settings.Locate_RGV = 4
        ai_settings.CNC_remaining_processing_time = [251, 283, 328, 0, 0, 378, 423, 455]
        return second_CNC_number



#RGV走下一步所需要的时间（即从上一个物料上完后 到下一个物料上完时 这段时间）
def oneStep_time(ai_settings, step):
    [T2,F_CNC, Take_time, Give_time] = second_process_move_time(ai_settings, step)
    #print('##',T2)
    return [T2 + ai_settings.RGV_clear_time, F_CNC, Take_time, Give_time]


#第二道工序RGV移动的时间,分两个阶段：（1）到第一道工序的CNC取料 （2）到第二道工序的CNC下料
def second_process_move_time(ai_settings, step):
    if step < 3 and step > 0:
        L = 1
    elif step < 5 and step > 2:
        L = 2
    elif step < 7 and step > 4:
        L = 3
    else:
        L = 4
    #选出一条最优路线
    min1 = 10000
    F_CNC = 0
    Take_time = 0
    Give_time = 0
    for index1 in range(1,9):
        if ai_settings.CNC_type[index1-1] == 1:
            if index1 < 3 and index1 > 0:
                M = 1
            elif index1 < 5 and index1 > 2:
                M = 2
            elif index1 < 7 and index1 > 4:
                M = 3
            else:
                M = 4

            if ai_settings.Locate_RGV - M == 0:
                F1 = 0
            elif abs(ai_settings.Locate_RGV - M) == 1:
                F1 = ai_settings.move_one_step_time
            elif abs(ai_settings.Locate_RGV - M) == 2:
                F1 = ai_settings.move_two_step_time
            else:
                F1 = ai_settings.move_three_step_time

            L_UL_time1 = loading_and_unloading_time(ai_settings, index1)
            if ai_settings.CNC_remaining_processing_time[index1 - 1] >= F1:
                FT = ai_settings.CNC_remaining_processing_time[index1 - 1] + L_UL_time1
            else:
                FT = F1 + L_UL_time1

            if  (L- M) == 0:
                S1 = 0
            elif abs(L - M) == 1:
                S1 = ai_settings.move_one_step_time
            elif abs(L - M) == 2:
                S1 = ai_settings.move_two_step_time
            else:
                S1 = ai_settings.move_three_step_time

            L_UL_time2 = loading_and_unloading_time(ai_settings, step)
            if ai_settings.CNC_remaining_processing_time[step - 1] - FT >= F1:
                ST = ai_settings.CNC_remaining_processing_time[step - 1] - FT + L_UL_time2
            else:
                ST = S1 + L_UL_time2

            if (ST + FT)<min1:
                min1 = ST + FT
                F_CNC = index1
                Take_time = FT
                Give_time = ST
                #print('**' ,min1)
    return [min1, F_CNC, Take_time, Give_time]



def loading_and_unloading_time(ai_settings, step):
    if step%2 == 0:
        time = ai_settings.RGV_up_odd_time
    else:
        time = ai_settings.RGV_up_even_time

    return time

#更新整个系统的工作状态
def update_status(ai_settings, next_place, next_CNC, optimal_time, F_CNC):
    ai_settings.Locate_RGV = next_place
    #ai_settings.CNC_status[next_CNC-1] = 1
    for num in range(1,9):
        ai_settings.CNC_remaining_processing_time[num-1] = ai_settings.CNC_remaining_processing_time[num-1]\
                                                           - optimal_time
        if ai_settings.CNC_remaining_processing_time[num-1] < 0:
            ai_settings.CNC_remaining_processing_time[num-1] = 0
    if ai_settings.CNC_type[next_CNC-1] == 2:
        ai_settings.CNC_remaining_processing_time[next_CNC-1] = ai_settings.CNC_work_time_2
        ai_settings.CNC_remaining_processing_time[F_CNC-1] = ai_settings.CNC_work_time_1