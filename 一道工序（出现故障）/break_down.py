import random
#在1~100之间随机产生一个数，作为每个CNC每加工100个物料出现故障的那个物料
def BreakDown_number():
    Random_Num = random.randint(0, 100)
    return Random_Num
#随机产生一个介于10~20分钟的故障时间
def BreakDown(ai_settings, CNC_num):
    '''CNC_num为出现故障的CNC编号'''
    Random_time = BreakDown_time()
    ai_settings.CNC_remaining_processing_time[CNC_num-1] = ai_settings.CNC_remaining_processing_time[CNC_num-1]\
                                                           + Random_time
    print('该CNC故障后剩余加工时间',ai_settings.CNC_remaining_processing_time[CNC_num-1])
    # 随机产生一个0~100的数
    ai_settings.Break_num = BreakDown_number()
    ai_settings.Break_num_record.append(ai_settings.Break_num)
    print(ai_settings.Break_num)

#产生一个10~20分钟的时间
def BreakDown_time():
    Random_time = random.randint(600, 1200)
    return Random_time
