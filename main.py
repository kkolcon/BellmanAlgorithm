__author__ = 'Virus'
import module

f = open('mapa.txt','r')
file = [line.strip('\n').split() for line in f.readlines()]
f.close()

height = int(file[0][1])
width = int(file[0][0])
columns = height * width
tabMap = []
tabV = []
gamma = 0.5

for line in file[2:]:
    if line:
        tabMap.append(line)
    else:
        break

for line in file[(2+height):]:
        if line:
            tabV.append(line)

print tabMap
print tabV

allElements = [[0 for x in range(width)] for y in range(height)]

rowIndex = 0
for row in tabMap:
    elIndex = 0
    for element in row:

        if element == '1':
            #ruch w gore
            probabUp = [[0]*width for i in range(height)]
            #ruch w prawo
            probabRight = [[0]*width for i in range(height)]
            #ruch w dol
            probabDown = [[0]*width for i in range(height)]
            #ruch w lewo
            probabLeft = [[0]*width for i in range(height)]

            if ((rowIndex - 1) < 0) or (tabMap[rowIndex-1][elIndex] == '0'):
                probabUp[rowIndex][elIndex] += 0.8
                probabRight[rowIndex][elIndex] += 0.1
                probabLeft[rowIndex][elIndex] += 0.1
            else:
                probabUp[rowIndex-1][elIndex] += 0.8
                probabRight[rowIndex-1][elIndex] += 0.1
                probabLeft[rowIndex-1][elIndex] += 0.1

            if ((elIndex - 1) < 0) or (tabMap[rowIndex][elIndex-1] == '0'):
                probabUp[rowIndex][elIndex] += 0.1
                probabDown[rowIndex][elIndex] += 0.1
                probabLeft[rowIndex][elIndex] += 0.8
            else:
                probabUp[rowIndex][elIndex-1] += 0.1
                probabDown[rowIndex][elIndex-1] += 0.1
                probabLeft[rowIndex][elIndex-1] += 0.8

            if ((elIndex + 1) >= width) or (tabMap[rowIndex][elIndex+1] == '0'):
                probabUp[rowIndex][elIndex] += 0.1
                probabRight[rowIndex][elIndex] += 0.8
                probabDown[rowIndex][elIndex] += 0.1
            else:
                probabUp[rowIndex][elIndex+1] += 0.1
                probabRight[rowIndex][elIndex+1] += 0.8
                probabDown[rowIndex][elIndex+1] += 0.1

            if((rowIndex + 1) >= height) or (tabMap[rowIndex+1][elIndex] == '0'):
                probabRight[rowIndex][elIndex] += 0.1
                probabDown[rowIndex][elIndex] += 0.8
                probabLeft[rowIndex][elIndex] += 0.1
            else:
                probabRight[rowIndex+1][elIndex] += 0.1
                probabDown[rowIndex+1][elIndex] += 0.8
                probabLeft[rowIndex+1][elIndex] += 0.1
        else:
            probabUp = 0
            probabRight = 0
            probabLeft = 0
            probabDown = 0

        probabs = [probabUp, probabRight, probabDown, probabLeft]
        allElements[rowIndex][elIndex] = module.Field(rowIndex, elIndex, probabs, float(tabV[rowIndex][elIndex]), float(tabV[rowIndex][elIndex]),0,element)

        elIndex += 1
    rowIndex += 1

for i in range(1000):
    for row in allElements:
        for element in row:
            if element.type == '1':
                actionTab = [module.Action(1,0), module.Action(2,0), module.Action(3,0), module.Action(4,0)]
                oldV = element.v

                for j in range(len(element.probabs)):
                    probab = element.probabs[j]
                    pRow = 0
                    for row in probab:
                        pCol = 0
                        for col in row:
                            if col!= 0:
                                elP = float(probab[pRow][pCol])
                                elV = float(allElements[pRow][pCol].v)
                                actionTab[j].value += float(elP*elV)
                            pCol += 1
                        pRow += 1
                maxValue = actionTab[0].value
                newAction = actionTab[0].move

                newV = 0
                for ac in actionTab:
                    if ac.value > maxValue:
                        maxValue = float(ac.value)
                        newAction = ac.move
                    newV = int(element.r) + gamma * maxValue

                if abs(oldV - newV) > 0.0001:
                    element.v = newV
                    element.action = newAction
                else:
                    break

resultTab = [['' for x in range(width)] for y in range(height)]
rowNumber = 0
for row in allElements:
    colNumber = 0
    for elem in row:
        string = ("{0:.2f}".format(elem.v)), elem.action
        resultTab[rowNumber][colNumber] = string
        colNumber += 1
    rowNumber +=1

print '===================Rozwiazanie===================='
for row in resultTab:
    print row