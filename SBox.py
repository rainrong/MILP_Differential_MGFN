import math

# SBox = [0x1, 0xd, 0xf, 0x0, 0xe, 0x8, 0x2, 0xb, 0x7, 0x4, 0xc, 0xa, 0x9, 0x3, 0x5, 0x6]
SBox = [7,14,15,0,13,11,8,1,9,3,4,12,2,5,10,6]
Slen = len(SBox)
DDT = []
for i in range(0, Slen):
    temp = []
    for j in range(0, Slen):
        temp.append(0)
    DDT.append(temp)

for inputdiff in range(0, Slen):
    for x in range(0, Slen):
        y = SBox[x]
        xx = x ^ inputdiff
        yy = SBox[xx]
        outputdiff = yy ^ y
        DDT[inputdiff][outputdiff] += 1


def tobit(var, len):
    temp = []
    while(len > 0):
        temp.append(var % 2)
        var //= 2
        len -= 1
    temp.reverse()
    return temp

print(DDT)
for i in range(0, Slen):
    for j in range(0, Slen):
        if DDT[i][j] != 0:
            biti = tobit(i, math.log2(Slen))
            bitj = tobit(j, math.log2(Slen))
            ans = [s for s in biti]
            for s in bitj:
                ans.append(s)
            # if -math.log2(DDT[i][j] / Slen) == 0.0:
            #     ans.append(0)
            #     ans.append(0)
            # elif -math.log2(DDT[i][j] / Slen) == 2.0:
            #     ans.append(1)
            #     ans.append(0)
            # else:
            #     ans.append(0)
            #     ans.append(1)
            print(str(ans) + ',')
            # temp = tobit(i, 4) + tobit(j, 4)
            # print(temp)
