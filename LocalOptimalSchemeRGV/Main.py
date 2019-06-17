# 全局变量初始化
global RGV_MOVE_TIME   # RGV移动下标个单位距离所用时间
global CNC_WORK_TIME   # CNC加工物料所用时间
global RGV_IMPORT_CNC_TIME   # RGV为CNC上下料所用时间
global RGV_CLEAR_TIME   # RGV清洗物料所用时间
global EndTime   # 工作期间时间单元个数 8*60*60s
global AllProduct
global NowTime
global TimeUnit  # 默认时间单元 1s
global CNC_Carry_State # 【0】没有工件在加工 【1】有工件在加工或加工完成
global CNC_Min_Time # 【0】加工完成 【X】正在加工
global RGV_Carry_State # 【0，X】不存在工件 【1，0】存在工件正在加工 【1，1】存在工件已加工完成
global RGV_Locat # 0,1 2,3 4,5 6,7
global RGV_Min_Time

from LocalOptimalSchemeRGV.Funation import *
from LocalOptimalSchemeRGV.ValueInit import *
from LocalOptimalSchemeRGV.Loop import *

Init()

FileSave = open("Log.txt", 'a', encoding='utf-8')

while NowTime < EndTime:
    TimeUnit = 1  # 设置时间单元
    Time_All_Temp = [-1, -1, -1, -1, -1, -1, -1, -1]

    Times_RGV_Temp = 0
    Times_CNC_Temp = [0, 0, 0, 0, 0, 0, 0, 0]
    Times_RGV_Move = [0, 0, 0, 0, 0, 0, 0, 0]

    PrintLoop(NowTime, CNC_Min_Time, CNC_Carry_State, RGV_Locat, RGV_Min_Time, RGV_Carry_State)

    FileSave.write("当前工作时间节点：" + str(NowTime) + '\n')
    '''选择局部最优加工方案'''
    MinIndex = LocalOptimalScheme(True,CNC_Min_Time,RGV_Locat)

    # 运行
    if RGV_Min_Time <= 0:
        FileSave.write(r"Move: % 2d -> % 2d UpDown: %2d %c" % (RGV_Locat, MinIndex, CNC_Carry_State[RGV_Locat], '\n'))

        if CNC_Carry_State[MinIndex] == 0: # 没有工件在CNC
            print("从CNC", RGV_Locat, "移动到CNC", MinIndex, "进行操作")
            CNC_Carry_State[MinIndex] = 1
            CNC_Min_Time[MinIndex] = CNC_WORK_TIME + Time_All_Temp[MinIndex]
            RGV_Min_Time = Time_All_Temp[MinIndex]
        else:
            if CNC_Min_Time[MinIndex] == 0: # 工件已加工完成
                CNC_Carry_State[MinIndex] = 0 # 先下料
                CNC_Carry_State[MinIndex] = 1 # 后上料
                RGV_Min_Time = Time_All_Temp[MinIndex]
                CNC_Min_Time[MinIndex] = CNC_WORK_TIME + Time_All_Temp[MinIndex]
                ProductAdd()
        RGV_Locat = MinIndex

    TimeUnit = OptimizingTimeParameters(True)
    if RGV_Min_Time != 0:
        print("对RGV进行等待", TimeUnit, "s 操作")
        FileSave.write(r"DelayS: %2d  On: %2d %c" % (TimeUnit, RGV_Locat, '\n'))

    # 时间前进
    for i in range(len(CNC_Min_Time)):
        CNC_Min_Time[i] = VoidTimeCome_CNC(CNC_Min_Time[i], TimeUnit)
    RGV_Min_Time = VoidTimeCome_RGV(RGV_Min_Time, TimeUnit)
    TimeCome(TimeUnit, True)

    if NowTime >= EndTime:
        break
print("\033[1;31;42mAllProduct", AllProduct)
FileSave.close()
