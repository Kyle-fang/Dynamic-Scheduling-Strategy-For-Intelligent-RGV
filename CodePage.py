# 时间前进
def TimeCome(TimeUnit, IsOutput):
    global NowTime
    NowTime = NowTime + TimeUnit
    if IsOutput == True:
        print("\033[1;36m时间节点：\033[0m", NowTime)

# 成品计数
def ProductAdd():
    global AllProduct
    AllProduct=AllProduct+1

# 打印每次循环信息
def PrintLoop(NowTime,CNC_Min_Time,CNC_Carry_State,RGV_Locat,RGV_Min_Time,RGV_Carry_State):
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
    distance = abs(Now - int(End / 2))
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

# 常量初始化
RGV_MOVE_TIME = [0, 0, 20, 20, 33, 33, 46, 46]  # RGV移动下标个单位距离所用时间
CNC_WORK_TIME = 560  # CNC加工物料所用时间
RGV_IMPORT_CNC_TIME = [28, 31, 28, 31, 28, 31, 28, 31]  # RGV为CNC上下料所用时间
RGV_CLEAR_TIME = 25  # RGV清洗物料所用时间
WORKS = ['U', 'C']  # ['UP-DOWN','CLEAR']
EndTime = 28800  # 工作期间时间单元个数 8*60*60s

# 全局变量初始化
global AllProduct
global NowTime
AllProduct =0 # 起始成品个数
NowTime = 0  # 当前时间节点 起始时间 0s

# 变量初始化
TimeUnit = 1  # 默认时间单元 1s
CNC_Carry_State = [0, 0, 0, 0, 0, 0, 0, 0]
CNC_Min_Time = [0, 0, 0, 0, 0, 0, 0, 0]
RGV_Carry_State = [0, 0] # 【0，X】不存在工件 【1，0】存在工件正在加工 【1，1】存在工件已加工完成
RGV_Locat = 0  # 0,1 2,3 4,5 6,7
RGV_Min_Time = 0

# Main
EndTime = 1000
FileSave = open("Log.txt", 'a', encoding='utf-8')

while NowTime < EndTime:
    TimeUnit = 1  # 设置时间单元

    PrintLoop(NowTime, CNC_Min_Time, CNC_Carry_State, RGV_Locat, RGV_Min_Time, RGV_Carry_State)

    FileSave.write("当前工作时间节点：" + str(NowTime) + '\n')
    Zeros_CNC = GetZeros(CNC_Min_Time)  # 由剩余加工时间得到闲置CNC位置
    Time_All_Temp = [[-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1]]
    print("闲置CNC位置【 Zeros_CNC 】", Zeros_CNC)
    # 预测下一步工作所用时间
    for NowWork in WORKS:

        print("\033[1;31m   当前工作流程：\033[0m", NowWork)

        Times_RGV_Move = [0, 0, 0, 0, 0, 0, 0, 0]
        Times_CNC_Updown = [0, 0, 0, 0, 0, 0, 0, 0]

        if NowWork == 'U':
            for Zero_CNC in Zeros_CNC:
                time = GetTime_Move(RGV_Locat, Zero_CNC)  # RGV从当前移动到指定位置所用时间
                Times_RGV_Move[Zero_CNC] = time
            print("        Times_RGV_Move", Times_RGV_Move)
            for Zero_CNC in Zeros_CNC:
                if CNC_Carry_State[Zero_CNC] == 0 & CNC_Min_Time[Zero_CNC] == 0:
                    Times_CNC_Updown[Zero_CNC] = Times_CNC_Updown[Zero_CNC] + RGV_IMPORT_CNC_TIME[Zero_CNC]
            for i in range(len(Time_All_Temp[0])):
                Time_All_Temp[0][i] = Times_CNC_Updown[i] + Times_RGV_Move[i]

            print("        Times_CNC_Updown", Times_CNC_Updown)

        if NowWork == 'C':
            if RGV_Carry_State[0] != 0:
                if RGV_Carry_State[1] == 1:
                    for Zero_CNC in Zeros_CNC:
                        # for count in Times_RGV_Move:
                        time = GetTime_Move(RGV_Locat, Zero_CNC)  # RGV从当前移动到指定位置所用时间
                        Times_RGV_Move[Zero_CNC] = time
                    # GetZerosOfCNC(CNC_Carry_State, CNC_Min_Time)
                    Time_All_Temp[1] = Times_RGV_Move
                    print("        Times_RGV_Move", Times_RGV_Move)
                    Time_All_Temp[1][RGV_Locat] = Time_All_Temp[1][RGV_Locat] + RGV_CLEAR_TIME
                    print("        Time_All_Temp[1][RGV_Locat]", Time_All_Temp[1][RGV_Locat])

    # 决定下一步工作并运行
    print("预计加工时间【 Time_All_Temp 】", Time_All_Temp)

    for i in list(range(2)):
        for j in list(range(8)):
            if Time_All_Temp[i][j] == -1:
                Time_All_Temp[i][j] = 9999
            if CNC_Min_Time[j] != 0 & i == 0:
                Time_All_Temp[i][j] = 9999
    print("预计加工时间【 Time_All_Temp 】", Time_All_Temp)
    MinIndex = GetMinIndex(Time_All_Temp)
    print("MinIndex", MinIndex)

    # 运行下一步
    if RGV_Min_Time == 0:
        if MinIndex[0] == 0:
            # 操作为MoveUpDown
            print("Move:", RGV_Locat, "->", MinIndex[1], "UpDown:", CNC_Carry_State[RGV_Locat])
            # Text="Move: %2d -> %2d UpDown: %2d %c"%(RGV_Locat, MinIndex[1], CNC_Carry_State[RGV_Locat],'\n')

            FileSave.write(r"Move: % 2d -> % 2d UpDown: %2d %c"%(RGV_Locat, MinIndex[1], CNC_Carry_State[RGV_Locat],'\n'))
            RGV_Locat = MinIndex[1]
            RGV_Min_Time = GetTime_Move(RGV_Locat, MinIndex[1]) + RGV_IMPORT_CNC_TIME[RGV_Locat]
            if CNC_Carry_State[RGV_Locat] == 0:
                CNC_Carry_State[RGV_Locat] = 1
                CNC_Min_Time[RGV_Locat] = CNC_Min_Time[RGV_Locat] + CNC_WORK_TIME + RGV_IMPORT_CNC_TIME[RGV_Locat]
            else:
                CNC_Carry_State[RGV_Locat] = 0
                RGV_Carry_State[0] = 1
                RGV_Carry_State[1] = 1
                ProductAdd()

        if MinIndex[0] == 1:
            # 操作为MoveClear
            print("Move:", RGV_Locat, "->", MinIndex[1], "Clear")
            FileSave.write(r"Move: %2d -> %2d Clear %c" % (RGV_Locat, MinIndex[1], '\n'))
            RGV_Locat = MinIndex[1]
            RGV_Min_Time = GetTime_Move(RGV_Locat, MinIndex[1])
            RGV_Min_Time = RGV_CLEAR_TIME
    else:
        TimeUnit=RGV_Min_Time
    # 时间前进
    for i in range(len(CNC_Min_Time)):
        CNC_Min_Time[i] = VoidTimeCome_CNC(CNC_Min_Time[i], TimeUnit)
    RGV_Min_Time = VoidTimeCome_RGV(RGV_Min_Time, TimeUnit)
    TimeCome(TimeUnit, True)

    if NowTime >= EndTime:
        break
print(AllProduct)
FileSave.close()
