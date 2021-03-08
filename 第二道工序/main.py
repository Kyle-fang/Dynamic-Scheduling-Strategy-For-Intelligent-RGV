import function as fun
import optimal_path as OP
from settings import Settings

CNC_number = []         #每次上物料CNC的编号

#调试
OP1 = []        #每一步所花的时间
NP = []
RL = []

def main():
    # 创建一个对象
    ai_settings = Settings()

    ai_settings.move_one_step_time = 20 #int(input("请输入移动一步的时间："))
    ai_settings.move_two_step_time = 33 #int(input("请输入移动两步的时间："))
    ai_settings.move_three_step_time = 46 #int(input("请输入移动三步的时间："))
    ai_settings.CNC_work_time_1 = 400 #int(input("请输入CNC的工作时间："))
    ai_settings.CNC_work_time_2 = 378
    ai_settings.RGV_up_even_time = 28 #int(input("请输入RGV给奇数CNC上下料的时间："))
    ai_settings.RGV_up_odd_time = 31 #int(input("请输入RGV给偶数CNC上下料的时间："))
    ai_settings.RGV_clear_time = 25 #int(input("请输入RGV清洗的时间："))

    fun.Decision_Ratio(ai_settings, ai_settings.CNC_work_time_1, ai_settings.CNC_work_time_2)
    #ai_settings.CNC_type = [1, 1, 2, 2, 2, 2, 1, 1]
    print('~', ai_settings.CNC_type)
    total_time = 0
    number = 0      #初始化8小时加工物料的个数

    while total_time<=28800:
        #搜索局部最优路径
        [optimal_time, next_CNC, next_place] = OP.Optimal_Path(ai_settings)

        #将以上变量封装到列表中去，方便显示
        CNC_number.append(next_CNC)
        OP1.append(optimal_time)
        NP.append(next_place)
        #总时间
        total_time = total_time + optimal_time
        #print('**',total_time)
        #更新状态
        fun.update_status(ai_settings, next_place, next_CNC, optimal_time)

        RL.append(ai_settings.Locate_RGV)
        #当该物料是第二道工序，则number+1
        if ai_settings.CNC_type[next_CNC-1] == 2:
            number = number + 1

    print('*************输出**************')
    print(number-1)
    print(CNC_number)
    print(OP1)
    print(RL)
    print(NP)
    print(total_time)

if __name__ == '__main__':
    main()