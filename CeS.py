from Funation import *

global NowTime


def GetNextMinTimeWorks(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat):
    Zeros_CNC_Time = GetZeros(CNC_Min_Time)
    Zeros_CNC_Carry = GetNORZeros(CNC_Carry_State)
    print("剩余操作时间为零的CNC及个数", Zeros_CNC_Time, len(Zeros_CNC_Time))
    print("带有物料的CNC及个数", Zeros_CNC_Carry, len(Zeros_CNC_Carry))
    Times_RGV_Move = [0 for _ in range(len(Zeros_CNC_Time))]
    for count in range(len(Zeros_CNC_Time)):
        time = GetTime_Move(RGV_Locat, Zeros_CNC_Time[count])  # RGV从当前移动到指定位置所用时间
        Times_RGV_Move[count] = time
    print("RGV从当前移动到指定CNC", Zeros_CNC_Time, "对应所需要时间", Times_RGV_Move)
    return Zeros_CNC_Time, Zeros_CNC_Carry, Times_RGV_Move


def GetZerosOfCNC(CNC_Carry_State, CNC_Min_Time):
    Zeros_CNC_Time = GetZeros(CNC_Min_Time)
    Zeros_CNC_Carry = GetNORZeros(CNC_Carry_State)
    print("剩余操作时间为零的CNC及个数", Zeros_CNC_Time, len(Zeros_CNC_Time))
    print("带有物料的CNC及个数", Zeros_CNC_Carry, len(Zeros_CNC_Carry))
    return Zeros_CNC_Time, Zeros_CNC_Carry


def StateRefresh(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat):
    # refresh CNC Carry State
    for i in range(len(CNC_Min_Time)):
        if CNC_Min_Time[i] != 0 & CNC_Carry_State[i] == 0:
            CNC_Carry_State[i] = 1


def ChooseNextWork():
    return 0


def CouldDownCarryCNC(Zeros_CNC_Carry, CNC_Min_Time):
    for i in Zeros_CNC_Carry:
        if CNC_Min_Time[i] == 0:
            return 0


def OneNextWorks(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat):
    Zeros_CNC_Time, Zeros_CNC_Carry, Times_RGV_Move = GetNextMinTimeWorks(CNC_Carry_State, CNC_Min_Time,
                                                                          RGV_Carry_State, RGV_Locat)
    NextMoves = [0 for _ in range(len(Zeros_CNC_Time))]
    for i in range(len(Zeros_CNC_Time)):
        NextMoves[i] = [Zeros_CNC_Time[i], Times_RGV_Move[i] + RGV_IMPORT_CNC_TIME[Zeros_CNC_Time[i]]]
    print("从当前位置移动到指定位置上下料时间", NextMoves)
    times = [0 for _ in range(len(NextMoves))]
    for i in range(len(NextMoves)):
        times[i] = NextMoves[i][1]
    MinTime = min(times)
    for i in range(len(NextMoves)):
        if MinTime == NextMoves[i][1]:
            count = i
            break
    print(MinTime, count)
    return [count, MinTime]


def CouldNextWorks(Zeros_CNC_Time, Zeros_CNC_Carry):
    return 0


while NowTime != EndTime:
    i = 1
    # for NowWork in WORKS:
    StateRefresh(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat)
    OneNextWorks(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat)
    if i == 1:
        # GetZerosOfCNC(CNC_Carry_State, CNC_Min_Time)
        # GetNextMinTimeWorks(CNC_Carry_State, CNC_Min_Time, RGV_Carry_State, RGV_Locat)

        NowTime = EndTime
    TimeCome(i)
