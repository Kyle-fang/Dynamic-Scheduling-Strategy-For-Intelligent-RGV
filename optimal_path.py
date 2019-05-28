
import function as fun
from settings import Settings

bi_settings = Settings()
bi_settings.move_one_step_time = 18 # int(input("请输入移动一步的时间："))
bi_settings.move_two_step_time = 32  # int(input("请输入移动两步的时间："))
bi_settings.move_three_step_time = 46  # int(input("请输入移动三步的时间："))
bi_settings.CNC_work_time = 545  # int(input("请输入CNC的工作时间："))
bi_settings.RGV_up_even_time = 27 # int(input("请输入RGV给奇数CNC上下料的时间："))
bi_settings.RGV_up_odd_time = 32 # int(input("请输入RGV给偶数CNC上下料的时间："))
bi_settings.RGV_clear_time = 25
'''
ai_settings = Settings()
ai_settings.Locate_RGV = 1
ai_settings.CNC_remaining_processing_time = [0,0,0,0,0,0,0,0]
'''
def Optimal_Path(ai_settings):
    T1_out = 0
    one_step_out = 0
    RGV_L = 0
    min = 10000

    #print(bi_settings.CNC_remaining_processing_time)
    for one_step in range(1, 9):
        #初始化刚开始时的状态
        bi_settings.Locate_RGV = ai_settings.Locate_RGV
        for num in range(1,9):
            bi_settings.CNC_remaining_processing_time[num-1] = ai_settings.CNC_remaining_processing_time[num-1]
        #print(bi_settings.Locate_RGV, bi_settings.CNC_remaining_processing_time)

        #判断下一步的位置
        if one_step < 3 and one_step > 0:
            L1 = 1
        elif one_step < 5 and one_step > 2:
            L1 = 2
        elif one_step < 7 and one_step > 4:
            L1 = 3
        else:
            L1 = 4
        T1 = fun.one_step_time(bi_settings, one_step)
        fun.update_status(bi_settings, L1, one_step, T1)
        #
        locate_RGV1 = bi_settings.Locate_RGV
        CRPT = []
        for C in bi_settings.CNC_remaining_processing_time:
            CRPT.append(C)
        for two_step in range(1, 9):
            #初始化为第一步更新的状态
            bi_settings.Locate_RGV = locate_RGV1
            for num1 in range(1,9):
                bi_settings.CNC_remaining_processing_time[num1-1] = CRPT[num1-1]
            #print('*********************')
            #print(bi_settings.Locate_RGV, bi_settings.CNC_remaining_processing_time)
            #判断下一步的位置
            if two_step < 3 and two_step > 0:
                L2 = 1
            elif two_step < 5 and two_step > 2:
                L2 = 2
            elif two_step < 7 and two_step > 4:
                L2 = 3
            else:
                L2 = 4
            #print(bi_settings.Locate_RGV,bi_settings.CNC_remaining_processing_time)
            T2 = fun.one_step_time(bi_settings, two_step)
            fun.update_status(bi_settings, L2, two_step, T2)
            for three_step in range(1,9):
                T3 = fun.one_step_time(bi_settings, three_step)
                T = T1 + T2 + T3
                if T < min:
                    min = T
                    T1_out = T1
                    one_step_out = one_step
                    RGV_L = L1
                #print(T3)
    #print(one_step_out, RGV_L, T1_out)
    return [T1_out, one_step_out, RGV_L]
#Optimal_Path(ai_settings)
