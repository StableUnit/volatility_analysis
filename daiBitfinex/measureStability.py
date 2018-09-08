import csv
import time
import matplotlib.pyplot as plt
import math



def getMinMaxInCandles(data, interval):
    result = []
    candleStart = int(data[0][1]/interval) * interval
    lastPrice = 0

    def changeMinMax(price, min, max):
        if price < min:
            min = row[3]
        if price > max:
            max = row[3]
        return min, max

    min = max = data[0][3]
    for row in data:
        if row[1] > candleStart + interval:
            result.append([candleStart, min, max])
            candleStart += interval
            if row[1] < candleStart + interval:
                min = max = row[3]
                min, max = changeMinMax(row[3], min, max)
            else:
                result.append([candleStart, lastPrice, lastPrice])
                candleStart += interval
        else:
            min, max = changeMinMax(row[3], min, max)
        lastPrice = row[3]
    return result

def averagePrice(data):
    sumOfPrices = 0
    for row in data:
        sumOfPrices += row[3]
    return sumOfPrices / len(data)

def getTotalVolume(data):
    sumOfVol = 0
    for row in data:
        sumOfVol += row[2]
    return sumOfVol

def averagePriceWeightedByVolume(data):
    sumOfPricesWeighted = 0
    for row in data:
        sumOfPricesWeighted += (row[2]*row[3])
    return sumOfPricesWeighted/getTotalVolume(data)


def variance(data, isFullSetOfData):
    avrg = averagePrice(data)
    sumOfSquares = 0
    for row in data:
        sumOfSquares += (row[3] - avrg)**2
    if isFullSetOfData:
        return sumOfSquares/len(data)
    else:
        return sumOfSquares/(len(data)-1)

def movingVarStdDev(data, setOfDataTimeLength, timeBetweenNewVariancePoint):
    moveVar = []
    moveStdDev = []
    firstPeriodStart = int(data[0][1]/setOfDataTimeLength) * setOfDataTimeLength
    for i in range(int(((data[-1][1] - firstPeriodStart - setOfDataTimeLength)/timeBetweenNewVariancePoint))):
        lastTimeframe = []
        for row in data:
            if row[1] > firstPeriodStart+(i*timeBetweenNewVariancePoint) and row[1] < firstPeriodStart+setOfDataTimeLength+(i*timeBetweenNewVariancePoint):
                lastTimeframe.append(row)
        tempVar = variance(lastTimeframe, False)
        moveVar.append(tempVar)
        moveStdDev.append(math.sqrt(tempVar))
    return moveVar, moveStdDev


def countTimesPassedDifference(data, difference):
    aboveDifferenceCount = 0
    belowDifferenceCount = 0
    for row in data:
        if row[1] < 1-difference:
            belowDifferenceCount += 1
        if row[2] > 1+difference:
            aboveDifferenceCount += 1
    return belowDifferenceCount, aboveDifferenceCount


data = []
price = []
with open('daiHistoryBitfinexEdited.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        data.append([int(row[0]), int(row[1]), float(row[2]), float(row[3])])
        price.append(float(row[3]))
        if float(row[3]) < 0.95:
            print(row[3])

print(data)
var = variance(data, True)
stanDev = math.sqrt(var)

print('Variance = {}'.format(var))
print('Standard deviation = {}'.format(stanDev))

print(averagePrice(data))
print(averagePriceWeightedByVolume(data))
movingVar, movingStdDev = movingVarStdDev(data, 864000000, 86400000)

print(movingVar)
plt.plot(movingVar)
plt.xlabel('Days since April 26th')
plt.ylabel('Variance')
plt.title('Moving variance of the last 10 days, calculated for every day')
plt.show()
plt.plot(movingStdDev)
plt.xlabel('Days since April 26th')
plt.ylabel('Standard deviation')
plt.title('Moving std dev of the last 10 days, calculated for every day')
plt.show()


candleWidths = [300000, 900000, 3600000, 14400000, 86400000, 604800000, 2419200000]
belowArray = []
aboveArray = []

for width in candleWidths:
    dataCandles = getMinMaxInCandles(data, width)
    for i in range(1, 11):
        i = i/100
        belowDifferenceCount, aboveDifferenceCount = countTimesPassedDifference(dataCandles, i)
        belowArray.append(belowDifferenceCount)
        aboveArray.append(aboveDifferenceCount)
        print('In {}    min timeframe ( {}   days), times passed below  {}    =     {}.     Times passed above  {}   =      {}'.format(
            width/60000, width/86400000, 1-i, belowDifferenceCount, 1+i, aboveDifferenceCount))

concatCounts = []
for i in range(0, len(candleWidths)):
    i = i*10
    for k in reversed(range(0, 10)):
        concatCounts.append(belowArray[i+k])
    concatCounts.append(0)
    for j in range(0, 10):
        concatCounts.append(aboveArray[i+j])


# x = [1 + t/100 for t in range(-10, 11)]
# print(x)
# for p in range(7):
#     plt.scatter(x, concatCounts[p*21:(p+1)*21])
#     plt.title('{} min ({} days) candles'.format(str(candleWidths[p]/60000), str(candleWidths[p]/86400000)))
#     plt.xlabel('Price of Dai in USD')
#     plt.ylabel('Number of candles < or > than the price level')
#     plt.show()


# plt.hist(price, 21)
# plt.xlabel('Price of Dai in USD (bins = 21)')
# plt.ylabel('Number of trades in bin price range')
# plt.show()

    # timeArray = []
    # minArray = []
    # maxArray = []
    #
    # for row in dataCandles:
    #     timeArray.append(row[0])
    #     minArray.append(row[1])
    #     maxArray.append(row[2])



    # print(timeArray)
    # print(minArray)
    # print(len(timeArray))
    # print(len(minArray))
    # plt.plot(maxArray)
    # plt.show()