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

# 时间前进
def TimeCome(TimeUnit, IsOutput):
    global NowTime
    NowTime = NowTime + TimeUnit
    if IsOutput == True:
        print("\033[1;36m时间节点：\033[0m", NowTime)


# 成品计数
def ProductAdd():
    global AllProduct
    AllProduct = AllProduct + 1


# 打印每次循环信息
def PrintLoop(NowTime, CNC_Min_Time, CNC_Carry_State, RGV_Locat, RGV_Min_Time, RGV_Carry_State):
    print("\033[1;36;40m当前工作时间节点：\033[0m", NowTime)
    print("CNC剩余加工时间【 CNC_Min_Time 】", CNC_Min_Time)
    print("CNC当前携带工件【 CNC_Carry_State 】", CNC_Carry_State)
    print("RGV当前所在位置【 RGV_Locat 】", RGV_Locat + 1, "号机")
    print("RGV剩余加工时间【 RGV_Min_Time 】", RGV_Min_Time)
    print("RGV当前携带工件【 RGV_Carry_State 】", RGV_Carry_State)


# 零元素所在位置
def GetZeros(List):
    count = 0
    number = 0
    TempList = [0 for _ in range(len(List))]
    while count < len(TempList):
        if List[count] == 0:
            TempList[number] = count
            number = number + 1
        count = count + 1
    Zeros = TempList[0:number]
    return Zeros


# 非零元素所在位置
def GetNORZeros(List):
    count = 0
    number = 0
    TempList = [0 for _ in range(len(List))]
    while count < len(TempList):
        if List[count] != 0:
            TempList[number] = count
            number = number + 1
        count = count + 1
    Zeros = TempList[0:number]
    return Zeros


# RGV从当前移动到指定位置所用时间
def GetTime_Move(Now, End):
    distance = abs(int(Now / 2) - int(End / 2))
    time = RGV_MOVE_TIME[distance]
    return time


# CNC等待时间后剩余时间
def VoidTimeCome_CNC(nowtime, time):
    Newnowtime = nowtime - time
    if Newnowtime < 0:
        Newnowtime = 0
    return Newnowtime


# CNC等待时间后剩余时间
def VoidTimeCome_RGV(nowtime, time):
    Newnowtime = nowtime - time
    if Newnowtime < 0:
        Newnowtime = 0
    return Newnowtime


def GetMinIndex(List):
    Min = [0] * len(List)
    MIN = [0, 0]
    for i in range(len(List)):
        Min[i] = min(List[i])
    MIN[0] = Min.index(min(Min))
    MIN[1] = List[MIN[0]].index(min(List[MIN[0]]))
    return MIN


def GetZerosOfCNC(CNC_Carry_State, CNC_Min_Time):
    Zeros_CNC_Time = GetZeros(CNC_Min_Time)
    Zeros_CNC_Carry = GetNORZeros(CNC_Carry_State)
    print("剩余操作时间为零的CNC及个数", Zeros_CNC_Time, len(Zeros_CNC_Time))
    print("带有物料的CNC及个数", Zeros_CNC_Carry, len(Zeros_CNC_Carry))


def LocalOptimalScheme(Judg,CNC_Min_Time,RGV_Locat):
    '''选择局部最优加工方案'''
    '''确定CNC的需求信号'''
    Time_All_Temp = [-1, -1, -1, -1, -1, -1, -1, -1]
    Times_RGV_Temp = 0
    Times_CNC_Temp = [0, 0, 0, 0, 0, 0, 0, 0]
    Times_RGV_Move = [0, 0, 0, 0, 0, 0, 0, 0]
    if Judg == True:
        print("——确定CNC的需求信号——")

    Zeros_CNC = GetZeros(CNC_Min_Time)  # 由剩余加工时间得到闲置CNC位置
    for Zero_CNC in Zeros_CNC:
        time = GetTime_Move(RGV_Locat, Zero_CNC)  # RGV从当前移动到指定位置所用时间
        Times_RGV_Move[Zero_CNC] = time

    if Judg == True:
        print("闲置CNC位置【 Zeros_CNC 】", Zeros_CNC)
        print("RGV从当前移动到指定位置所用时间【 Times_RGV_Move 】", Times_RGV_Move)
    '''确定CNC的上下料所需时间'''
    if Judg == True:
        print("——确定CNC的上下料及清洗所需时间——")

    for Zero_CNC in Zeros_CNC:
        if CNC_Carry_State[Zero_CNC] == 0:
            Times_CNC_Temp[Zero_CNC] = RGV_IMPORT_CNC_TIME[Zero_CNC]
            Time_All_Temp[Zero_CNC] = Times_CNC_Temp[Zero_CNC] + Times_RGV_Move[Zero_CNC]
        else:
            if CNC_Min_Time[Zero_CNC] == 0:
                Times_CNC_Temp[Zero_CNC] = RGV_IMPORT_CNC_TIME[Zero_CNC] + RGV_CLEAR_TIME
                Time_All_Temp[Zero_CNC] = Times_CNC_Temp[Zero_CNC] + Times_RGV_Move[Zero_CNC]

    if Judg == True:
        print("CNC的上下料及清洗所需时间【 Times_CNC_Temp 】", Times_CNC_Temp)

    for j in list(range(8)):
        if Time_All_Temp[j] == -1:
            Time_All_Temp[j] = 9999

    if Judg == True:
        print("预计步骤时间【 Time_All_Temp 】", Time_All_Temp)

    MinIndex = Time_All_Temp.index(min(Time_All_Temp))

    if Judg == True:
        print("MinIndex", MinIndex)

    return MinIndex


def OptimizingTimeParameters(Judg):
    if (RGV_Min_Time != 0) or (min(CNC_Min_Time) > 0):

        Min_Time = CNC_Min_Time + [RGV_Min_Time]
        for i in range(len(Min_Time)):
            if Min_Time[i] == 0:
                Min_Time[i] = 9999
        if Judg == True:
            print(Min_Time)
        TimeUnit = min(Min_Time)

        return TimeUnit
