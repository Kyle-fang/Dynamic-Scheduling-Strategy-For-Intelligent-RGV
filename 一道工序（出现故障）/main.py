import function as fun
import optimal_path as OP
from settings import Settings

import break_down as BD
CNC_number = []
up_start_time = []
down_start_time = []

#调试
OP1 = []
NP = []
RL = []

def main():
    # 创建一个对象
    ai_settings = Settings()

    ai_settings.move_one_step_time = 18#int(input("请输入移动一步的时间："))
    ai_settings.move_two_step_time = 32#int(input("请输入移动两步的时间："))
    ai_settings.move_three_step_time = 46#int(input("请输入移动三步的时间："))
    ai_settings.CNC_work_time = 560#int(input("请输入CNC的工作时间："))
    ai_settings.RGV_up_even_time = 27#int(input("请输入RGV给奇数CNC上下料的时间："))
    ai_settings.RGV_up_odd_time = 32#int(input("请输入RGV给偶数CNC上下料的时间："))
    ai_settings.RGV_clear_time = 25#int(input("请输入RGV清洗的时间："))

    total_time = 0
    number = 0

    # 随机产生一个0~100的数
    ai_settings.Break_num = BD.BreakDown_number()
    ai_settings.Break_num_record.append(ai_settings.Break_num)
    print(ai_settings.Break_num)

    while total_time<=28800:
        print('~',ai_settings.CNC_remaining_processing_time)
        # 判断是否有CNC的物料加工数为之前生成随机数的倍数
        for X in range(1, 9):
            if (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num) \
                    | (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num + 100) \
                    | (ai_settings.CNC_TimesOfWork[X - 1] == ai_settings.Break_num + 200):
                BD.BreakDown(ai_settings, X)
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~', ai_settings.CNC_remaining_processing_time)
                # 统计每个CNC故障的次数
                ai_settings.CNC_BreakDown_time[X - 1] = ai_settings.CNC_BreakDown_time[X - 1] + 1
        #搜索局部最优路径
        [optimal_time, next_CNC, next_place] = OP.Optimal_Path(ai_settings)
        # 统计CNC工作的次数
        ai_settings.CNC_TimesOfWork[next_CNC - 1] = ai_settings.CNC_TimesOfWork[next_CNC - 1] + 1

        print('~~~', ai_settings.CNC_remaining_processing_time)
        #将以上变量封装到列表中去，方便显示
        CNC_number.append(next_CNC)
        OP1.append(optimal_time)
        NP.append(next_place)
        #总时间
        total_time = total_time + optimal_time
        print('!!!!!!',ai_settings.CNC_remaining_processing_time)
        #更新状态
        fun.update_status(ai_settings, next_place, next_CNC, optimal_time)
        print('@@@@@@@@',ai_settings.CNC_remaining_processing_time)
        RL.append(ai_settings.Locate_RGV)
        #
        number = number + 1

    print('*************输出**************')
    print(number-1)
    print(CNC_number)
    print(OP1)
    print(RL)
    print(NP)
    print(total_time)
    print('CNC加工个数', ai_settings.CNC_TimesOfWork)
    print('CNC故障次数', ai_settings.CNC_BreakDown_time)
    print('随机故障历史记录', ai_settings.Break_num_record)

if __name__ == '__main__':
    main()