RGV_MOVE_TIME = [0, 20, 33, 46]  # RGV移动下标个单位距离所用时间
CNC_WORK_TIME = 560  # CNC加工物料所用时间
RGV_IMPORT_CNC_TIME = [28, 31, 28, 31, 28, 31,28,31]  # RGV为CNC上下料所用时间
RGV_CLEAR_TIME = 25  # RGV清洗物料所用时间
WORKS=['UP-DOWN','CLEAR','MOVE']

CNC_Min_Time = [0, 0, 0, 0, 0, 0, 0, 0]
CNC_Carry_State = [0, 0, 0, 0, 0, 0, 0, 0]
RGV_Carry_State = [0, 0]
RGV_Locat = 0

NowTime = 0
EndTime = 28800  # 8*60*60

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
