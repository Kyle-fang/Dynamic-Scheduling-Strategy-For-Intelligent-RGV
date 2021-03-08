import function as fun
import optimal_path as OP
from settings import Settings

import break_down as BD



def main():
    # 创建一个对象
    ai_settings = Settings()
    ai_settings.move_one_step_time = 18#int(input("请输入移动一步的时间："))
    ai_settings.move_two_step_time = 32#int(input("请输入移动两步的时间："))
    ai_settings.move_three_step_time = 46#int(input("请输入移动三步的时间："))
    ai_settings.CNC_work_time_1 = 455#int(input("请输入CNC的工作时间："))
    ai_settings.CNC_work_time_2 = 182
    ai_settings.RGV_up_even_time = 27 #int(input("请输入RGV给奇数CNC上下料的时间："))
    ai_settings.RGV_up_odd_time = 32 #int(input("请输入RGV给偶数CNC上下料的时间："))
    ai_settings.RGV_clear_time = 25 #int(input("请输入RGV清洗的时间："))

    # 调试
    CNC_number = []  # 每次上物料CNC的编号
    OP1 = []  # 每一步所花的时间
    NP = []
    RL = []
    take_time = []
    give_time = []
    second_CNC_num = fun.Decision_Ratio(ai_settings, ai_settings.CNC_work_time_1, ai_settings.CNC_work_time_2)
    #ai_settings.CNC_type = [1, 1, 2, 2, 2, 2, 1, 1]
    print('~', ai_settings.CNC_type)
    if second_CNC_num == 4:
        CNC_number = [1, 3, 5, 7]  # 每次上物料CNC的编号
        OP1 = [28, 48, 48, 48]  # 每一步所花的时间
        NP = [1, 2, 3, 4]
        RL = [1, 2, 3, 4]
        take_time = [0, 0, 0, 0]
        give_time = [0, 0, 0, 0]
    elif second_CNC_num == 5:
        CNC_number = [1, 5, 6]  # 每次上物料CNC的编号
        OP1 = [30, 71, 35]  # 每一步所花的时间
        NP = [1, 3, 3]
        RL = [1, 3, 3]
        take_time = [0, 0, 0]
        give_time = [0, 0, 0]
    elif second_CNC_num == 2:
        CNC_number = [1, 2, 3, 6, 7, 8]  # 每次上物料CNC的编号
        OP1 = [27, 32, 45, 50, 45, 32]  # 每一步所花的时间
        NP = [1, 1, 2, 3, 4, 4]
        RL = [1, 1, 2, 3, 4, 4]
        take_time = [0, 0, 0, 0, 0, 0]
        give_time = [0, 0, 0, 0, 0, 0]
    total_time = sum(OP1)
    print('&&&&&', total_time)
    number = 1       #初始化8小时加工物料的个数
    # 随机产生一个0~100的数
    ai_settings.Break_num = BD.BreakDown_number()
    ai_settings.Break_num_record.append(ai_settings.Break_num)
    print(ai_settings.Break_num)
    while total_time<=28800:
        # 判断是否有CNC的物料加工数为之前生成随机数的倍数
        for X in range(1, 9):
            if (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num) \
                    | (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num + 100) \
                    | (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num + 200):
                BD.BreakDown(ai_settings, X)
                ai_settings.CNC_BreakDown_time[X - 1] = ai_settings.CNC_BreakDown_time[X - 1] + 1
        #搜索局部最优路径
        [optimal_time, next_CNC, next_place, F_CNC, Take_time, Give_time] = OP.Optimal_Path(ai_settings)

        #统计CNC工作的次数
        ai_settings.CNC_TimesOfWork[next_CNC-1] = ai_settings.CNC_TimesOfWork[next_CNC-1] + 1
        ai_settings.CNC_TimesOfWork[F_CNC-1] = ai_settings.CNC_TimesOfWork[F_CNC-1] + 1

        #将以上变量封装到列表中去，方便显示
        CNC_number.append(F_CNC)
        CNC_number.append(next_CNC)
        OP1.append(optimal_time)
        NP.append(next_place)
        take_time.append(Take_time)
        give_time.append(Give_time)

        #总时间
        total_time = total_time + optimal_time
        #print('**',total_time)
        #更新状态
        fun.update_status(ai_settings, next_place, next_CNC, optimal_time, F_CNC)

        RL.append(ai_settings.Locate_RGV)
        #当该物料是第二道工序，则number+1

        number = number + 1

    print('*************输出**************')
    print('8小时内加工物料的总个数',number-1)
    print('每一步要处理的CNC编号', CNC_number)
    print('每一步的总时间', OP1)
    print('每一步取料的时间', take_time)
    print('每一步上料的时间', give_time)
    print('每一步要去的位置', RL)
    print(NP)
    print('总时间', total_time)
    print('CNC加工个数',ai_settings.CNC_TimesOfWork)
    print('CNC故障次数',ai_settings.CNC_BreakDown_time)
    print('随机故障历史记录',ai_settings.Break_num_record)

if __name__ == '__main__':
    main()