'''
PCount= [0 for _ in range(10)]
j=0
for j in range(10):
    #PCount[j]=random
    random= divmod(j*100+j*10+j,11)
    print(random)
    PCount[j] = random[1]
print(PCount)
i=0
while i<20:
    k = PCount.index(min(PCount))
    print(i,PCount,k)
    PCount[k]=PCount[k]+17
    print(i, PCount)

    i=i+1

def GetMinIndex(List):
    Min = [0] * len(List)
    MIN = [0, 0]
    for i in range(len(List)):
        Min[i] = min(List[i])
    MIN[0] = Min.index(min(Min))
    MIN[1] = List[MIN[0]].index(min(List[MIN[0]]))
    return MIN

lista=[[1,2,3,4,5,6],[9,9,0,9,99,999],[1,2,3,4,5,6]]
Min=[0,0,0]
for i in range(3):
    Min[i]=min(lista[i])
print("Min",Min)
MIN_X =Min.index(min(Min))
print(MIN_X)
MIN_Y=lista[MIN_X].index(min(lista[MIN_X]))
print(MIN_Y)
print(len(lista[0]))
print(GetMinIndex(lista))

# RGV从当前移动到指定位置所用时间
RGV_MOVE_TIME = [0, 20, 33, 46]
def GetTime_Move(Now, End):
    time = -1
    distance = abs(int(Now / 2) - int(End / 2))
    try:
        time = RGV_MOVE_TIME[distance]
    except:
        print("distance",distance)
    return time
for i in range(8):
    for j in range(8):
        try:
            print("OK",i,j,GetTime_Move(i,j))
        except:
            print(i,j)
'''
for i in range(8):
    print(i)