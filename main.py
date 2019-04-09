
import function as fun
from settings import Settings


global min

def main():
    #创建一个对象
    ai_settings = Settings()


    ai_settings.move_one_step_time = int(input("请输入移动一步的时间："))
    ai_settings.move_two_step_time = int(input("请输入移动两步的时间："))
    ai_settings.move_three_step_time = int(input("请输入移动三步的时间："))
    ai_settings.CNC_work_time = int(input("请输入CNC的工作时间："))
    ai_settings.RGV_up_even_time = int(input("请输入RGV给奇数CNC上下料的时间："))
    ai_settings.RGV_up_odd_time = int(input("请输入RGV给偶数CNC上下料的时间："))
    ai_settings.RGV_clear_time = int(input("请输入RGV清洗的时间："))

    min = 10000000
    while True:
        for one_step in range(1,8):
            T1 = fun.one_step_time()
            for two_step in range(1,8):
                T2 = fun.one_step_time()
                for three in range(1,8):
                    T3 = fun.one_step_time()
                    T = T1 + T2 + T3
                    if T<min:
                        min = T
                        if one_step == 1 or 2:
                            L = 1
                        elif one_step == 3 or 4:
                            L = 2
                        elif one_step == 5 or 6:
                            L = 3
                        else:
                            L = 4
                        ai_settings.Locate_RGV = L


if __name__ == '__main__':
    main()