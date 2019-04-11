# 时间前进
def TimeCome(i):
    global NowTime
    NowTime = NowTime + i

# 零元素所在位置
def GetZeros(List):
    count = 0
    number = 0
    while count < len(List):
        if List[count] == 0:
            List[number] = count
            number = number + 1
        count = count + 1
    Zeros = List[0:number]
    return Zeros

# RGV从当前移动到指定位置所用时间
def GetTime_Move(Now,End):
    distance=abs(Now-int(End/2))
    time=RGV_MOVE_TIME[distance]
    return time

#CNC等待时间后剩余时间
def VoidTimeCome_CNC(nowtime,time):
    Newnowtime=nowtime - time
    if Newnowtime<0:
        Newnowtime=0
    return Newnowtime

global NowTime
NowTime = 0
EndTime = 28800  # 8*60*60
RGV_MOVE_TIME = [0, 20, 33, 46]  # RGV移动下标个单位距离所用时间
CNC_WORK_TIME = 560  # CNC加工物料所用时间
RGV_IMPORT_CNC_TIME = [28, 31, 28, 31, 28, 31,28,31]  # RGV为CNC上下料所用时间
RGV_CLEAR_TIME = 25  # RGV清洗物料所用时间
WORKS=['UP-DOWN','CLEAR','MOVE']

CNC_Carry_State = [0, 0, 0, 0, 0, 0, 0, 0]
CNC_Min_EndTimes = [0, 0, 0, 0, 0, 0, 0, 0]
RGV_Carry_State = [0, 0]
RGV_Locat = 0 # 0,1 2,3 4,5 6,7



CNC_Min_EndTimes=[0, 200, 400, 50, 70, 4, 0, 0]
RGV_Carry_State = [1, 1]
Zeros_CNC=GetZeros(CNC_Min_EndTimes) # 得到闲置CNC位置
print(Zeros_CNC)
Times_RGV_Move=[0 for _ in range(len(Zeros_CNC))]
#Times_RGV_Move=[-1,-1,-1,-1,-1,-1,-1,-1]
for count in range(len(Zeros_CNC)):
#for count in Times_RGV_Move:
    time=GetTime_Move(RGV_Locat,Zeros_CNC[count])# RGV从当前移动到指定位置所用时间
    Times_RGV_Move[count]=time
print(Times_RGV_Move)
CNC_Min_EndTimes[0]=100
Times_CNC_Updown=[0 for _ in range(len(Zeros_CNC))]
for Zero_CNC in range(len(Zeros_CNC)):
    if CNC_Carry_State[Zero_CNC]==0 & CNC_Min_EndTimes[Zero_CNC]==0 :
        Times_CNC_Updown[Zero_CNC]=Times_CNC_Updown[Zero_CNC]+RGV_IMPORT_CNC_TIME[Zero_CNC]
print(Times_CNC_Updown)

Time_Clear=0
if RGV_Carry_State[0]!=0:
    if RGV_Carry_State[1]==1:
        Time_Clear=RGV_CLEAR_TIME
print(Time_Clear)



Times_Works=[0 for _ in range(len(Zeros_CNC))]
for count in range(len(Zeros_CNC)):
    Times_Works[count]=Times_RGV_Move[count]+Times_CNC_Updown[count]
print(Times_Works)

CNC_Min_Time_1=[0 for _ in range(len(Zeros_CNC)*len(CNC_Min_EndTimes))]
for count_0 in range(len(Zeros_CNC)):
    for count_1 in range(len(CNC_Min_EndTimes)):
        #CNC_Min_Time_1[count_1+count_0*len(CNC_Min_EndTimes)]=VoidTimeCome_CNC(CNC_Min_EndTimes[count_1],Times_Works[count_0])
        CNC_Min_Time_1[count_1 + count_0 * len(CNC_Min_EndTimes)] = CNC_Min_EndTimes[count_1]-Times_Works[count_0]
        print(CNC_Min_EndTimes[count_1],Times_Works[count_0])
print(CNC_Min_Time_1)