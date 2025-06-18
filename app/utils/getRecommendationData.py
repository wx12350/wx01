from app.utils.getPublicData import getAllTravelInfoMapData
import random
def getAllTravelByTitle(traveTitleList):
    resultList = []
    for title in traveTitleList:
        for travel in getAllTravelInfoMapData():
            if title == travel.title:resultList.append(travel)
    return resultList

# def getRandomTravel():
#     travelList = getAllTravelInfoMapData()
#     maxLen = len(travelList)
#     resultList = []
#     for i in range(10):
#         randomNum = random.randint(0,maxLen)
#         resultList.append(travelList[randomNum])
#     return resultList


#wx 2025.6.12
from app.models import TravelInfo


def getRandomTravel():
    travelList = list(TravelInfo.objects.all())
    if not travelList:
        return []  # 如果列表为空，返回空列表

    resultList = []
    for _ in range(10):
        randomNum = random.randint(0, len(travelList) - 1)
        resultList.append(travelList[randomNum])
    return resultList