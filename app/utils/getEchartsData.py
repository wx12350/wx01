# import json
# from random import random
#
# from django.db.models import Count
#
# from app.models import TravelInfo
# from app.utils import getPublicData
# import datetime
# travelInfoList = getPublicData.getAllTravelInfoMapData()
#
# # def cityCharDataOne():
# #     cityDic = {}
# #     for travel in travelInfoList:
# #         if cityDic.get(travel.province,-1) == -1:
# #             cityDic[travel.province] = 1
# #         else:
# #             cityDic[travel.province] += 1
# #
# #     return list(cityDic.keys()),list(cityDic.values())
# #
# # def cityCharDataTwo():
# #     cityDic = {}
# #     for travel in travelInfoList:
# #         if cityDic.get(travel.level, -1) == -1:
# #             cityDic[travel.level] = 1
# #         else:
# #             cityDic[travel.level] += 1
# #     resultData = []
# #     for key,value in cityDic.items():
# #         resultData.append({
# #             'name':key,
# #             'value':value
# #         })
# #     return resultData
#
#
#
# #todo  新添加的代码
# def cityCharDataOne(province=None):
#     queryset = TravelInfo.objects.all()
#     if province:
#         queryset = queryset.filter(province=province)
#
#     # 原有数据处理逻辑保持不变
#     city_counts = queryset.values('province').annotate(count=Count('id'))
#     Xdata = [item['province'] for item in city_counts]
#     Ydata = [item['count'] for item in city_counts]
#     return Xdata, Ydata
#
#
# def cityCharDataTwo(province=None):
#     queryset = TravelInfo.objects.all()
#     if province:
#         queryset = queryset.filter(province=province)
#
#     # 原有等级统计逻辑保持不变
#     level_counts = queryset.values('level').annotate(count=Count('id'))
#     resultData = [{'value': item['count'], 'name': item['level']} for item in level_counts]
#     return resultData
#
#
#
#
# def getRateCharDataOne(travelList):
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.star, -1) == -1:
#             startDic[travel.star] = 1
#         else:
#             startDic[travel.star] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData
#
#
# def getRateCharDataTwo(travelList):
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.score, -1) == -1:
#             startDic[travel.score] = 1
#         else:
#             startDic[travel.score] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData
#
# def getPriceCharDataOne(traveList):
#     xData = ['免费','100元以内','200元以内','300元以内','400元以内','500元以内','500元以外']
#     yData = [0 for x in range(len(xData))]
#     for travel in traveList:
#         price = float(travel.price)
#         if price <= 10:
#             yData[0] += 1
#         elif price <= 100:
#             yData[1] += 1
#         elif price <= 200:
#             yData[2] += 1
#         elif price <= 300:
#             yData[3] += 1
#         elif price <= 400:
#             yData[4] += 1
#         elif price <= 500:
#             yData[5] += 1
#         elif price > 500:
#             yData[6] += 1
#     return xData,yData
#
# def getPriceCharDataTwo(traveList):
#     xData = [str(x * 300) + '份以内' for x in range(1,15)]
#     yData = [0 for x in range(len(xData))]
#     for travel in traveList:
#         saleCount = float(travel.saleCount)
#         for x in range(1,15):
#             count = x * 300
#             if saleCount <= count:
#                 yData[x - 1] += 1
#                 break
#
#     return xData,yData
#
#
# def getPriceCharDataThree(travelList):
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.discount, -1) == -1:
#             startDic[travel.discount] = 1
#         else:
#             startDic[travel.discount] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData
#
# # def getCommentsCharDataOne():
# #     commentsList = getPublicData.getAllCommentsData()
# #     xData = []
# #     def get_list(date):
# #         return datetime.datetime.strptime(date,'%Y-%m-%d').timestamp()
# #     for comment in commentsList:
# #         xData.append(comment['date'])
# #     xData = list(set(xData))
# #     xData = list(sorted(xData,key=lambda x: get_list(x),reverse=True))
# #     yData = [0 for x in range(len(xData))]
# #     for comment in commentsList:
# #         for index,date in enumerate(xData):
# #             if comment['date'] == date:
# #                 yData[index] += 1
# #     return xData,yData
# #
# # def getCommentsCharDataTwo():
# #     commentsList = getPublicData.getAllCommentsData()
# #     startDic = {}
# #     for travel in commentsList:
# #         if startDic.get(travel['score'], -1) == -1:
# #             startDic[travel['score']] = 1
# #         else:
# #             startDic[travel['score']] += 1
# #     resultData = []
# #     for key, value in startDic.items():
# #         resultData.append({
# #             'name': key,
# #             'value': value
# #         })
# #     return resultData
# #
# # def getCommentsCharDataThree():
# #     travelList = getPublicData.getAllTravelInfoMapData()
# #     xData = [str(x * 1000) + '条以内' for x in range(1, 20)]
# #     yData = [0 for x in range(len(xData))]
# #     for travel in travelList:
# #         saleCount = int(travel.commentsLen)
# #         for x in range(1, 20):
# #             count = x * 1000
# #             if saleCount <= count:
# #                 yData[x - 1] += 1
# #                 break
# #     return xData, yData
# #
#
#
#
#
# # todo 新增根据省份去查询数据
# def getCommentsCharDataOne(province=None):
#     # 获取评论数据（支持省份过滤）
#     commentsList = []
#     if province:
#         travels = TravelInfo.objects.filter(province__icontains=province)
#         for travel in travels:
#             try:
#                 comments = json.loads(travel.comments)
#                 commentsList.extend(comments)
#             except:
#                 continue
#     else:
#         commentsList = getPublicData.getAllCommentsData()
#
#     # 原有处理逻辑
#     xData = []
#
#     def get_list(date):
#         return datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()
#
#     for comment in commentsList:
#         xData.append(comment['date'])
#     xData = list(set(xData))
#     xData = sorted(xData, key=lambda x: get_list(x), reverse=True)
#     yData = [0] * len(xData)
#     for comment in commentsList:
#         for index, date in enumerate(xData):
#             if comment['date'] == date:
#                 yData[index] += 1
#     return xData, yData
#
#
# def getCommentsCharDataTwo(province=None):
#     # 获取评论数据（支持省份过滤）
#     commentsList = []
#     if province:
#         travels = TravelInfo.objects.filter(province__icontains=province)
#         for travel in travels:
#             try:
#                 comments = json.loads(travel.comments)
#                 commentsList.extend(comments)
#             except:
#                 continue
#     else:
#         commentsList = getPublicData.getAllCommentsData()
#
#     # 原有处理逻辑
#     startDic = {}
#     for comment in commentsList:
#         score = comment['score']
#         startDic[score] = startDic.get(score, 0) + 1
#     return [{'name': k, 'value': v} for k, v in startDic.items()]
#
#
# def getCommentsCharDataThree(province=None):
#     # 获取景点数据（支持省份过滤）
#     travels = TravelInfo.objects.all()
#     if province:
#         travels = travels.filter(province__icontains=province)
#
#     # 原有处理逻辑
#     xData = [f"{x * 1000}条以内" for x in range(1, 20)]
#     yData = [0] * len(xData)
#     for travel in travels:
#         try:
#             count = int(travel.commentsLen)
#             for i in range(19):
#                 if count <= (i + 1) * 1000:
#                     yData[i] += 1
#                     break
#         except:
#             continue
#     return xData, yData



#wx 2025.6.12
# import json
# from random import random
# from django.db.models import Count
# from app.models import TravelInfo
# from app.utils import getPublicData
# import datetime
#
#
# # 删除模块级别的数据库查询
# # travelInfoList = getPublicData.getAllTravelInfoMapData() # 这行是问题根源
#
# # 所有函数都改为在内部获取所需数据
# def cityCharDataOne(province=None):
#     # 使用 ORM 查询，无需获取整个列表
#     queryset = TravelInfo.objects.all()
#     if province:
#         queryset = queryset.filter(province=province)
#
#     city_counts = queryset.values('province').annotate(count=Count('id'))
#     Xdata = [item['province'] for item in city_counts]
#     Ydata = [item['count'] for item in city_counts]
#     return Xdata, Ydata
#
#
# def cityCharDataTwo(province=None):
#     queryset = TravelInfo.objects.all()
#     if province:
#         queryset = queryset.filter(province=province)
#
#     level_counts = queryset.values('level').annotate(count=Count('id'))
#     resultData = [{'value': item['count'], 'name': item['level']} for item in level_counts]
#     return resultData
#
#
# def getRateCharDataOne():
#     # 在函数内部获取数据
#     travelList = getPublicData.getAllTravelInfoMapData()
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.star, -1) == -1:
#             startDic[travel.star] = 1
#         else:
#             startDic[travel.star] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData
#
# def getRateCharDataTwo():
#     # 在函数内部获取数据
#     travelList = getPublicData.getAllTravelInfoMapData()
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.score, -1) == -1:
#             startDic[travel.score] = 1
#         else:
#             startDic[travel.score] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData


# def getPriceCharDataOne():
#     # 在函数内部获取数据
#     travelList = getPublicData.getAllTravelInfoMapData()
#     xData = ['免费', '100元以内', '200元以内', '300元以内', '400元以内', '500元以内', '500元以外']
#     yData = [0 for x in range(len(xData))]
#     for travel in travelList:
#         price = float(travel.price)
#         if price <= 10:
#             yData[0] += 1
#         elif price <= 100:
#             yData[1] += 1
#         elif price <= 200:
#             yData[2] += 1
#         elif price <= 300:
#             yData[3] += 1
#         elif price <= 400:
#             yData[4] += 1
#         elif price <= 500:
#             yData[5] += 1
#         elif price > 500:
#             yData[6] += 1
#     return xData, yData


# def getPriceCharDataTwo():
#     # 在函数内部获取数据
#     travelList = getPublicData.getAllTravelInfoMapData()
#     xData = [str(x * 300) + '份以内' for x in range(1, 15)]
#     yData = [0 for x in range(len(xData))]
#     for travel in travelList:
#         saleCount = float(travel.saleCount)
#         for x in range(1, 15):
#             count = x * 300
#             if saleCount <= count:
#                 yData[x - 1] += 1
#                 break
#     return xData, yData


# def getPriceCharDataThree():
#     # 在函数内部获取数据
#     travelList = getPublicData.getAllTravelInfoMapData()
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.discount, -1) == -1:
#             startDic[travel.discount] = 1
#         else:
#             startDic[travel.discount] += 1
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#     return resultData






#wx2025.6.12

import json
from random import random
from django.db.models import Count
from app.models import TravelInfo
from app.utils import getPublicData
import datetime


# 删除模块级别的数据库查询
# travelInfoList = getPublicData.getAllTravelInfoMapData() # 这行是问题根源

# 所有函数都改为在内部获取所需数据
def cityCharDataOne(province=None):
    # 使用 ORM 查询，无需获取整个列表
    queryset = TravelInfo.objects.all()
    if province:
        queryset = queryset.filter(province=province)

    city_counts = queryset.values('province').annotate(count=Count('id'))
    Xdata = [item['province'] for item in city_counts]
    Ydata = [item['count'] for item in city_counts]
    return Xdata, Ydata


def cityCharDataTwo(province=None):
    queryset = TravelInfo.objects.all()
    if province:
        queryset = queryset.filter(province=province)

    level_counts = queryset.values('level').annotate(count=Count('id'))
    resultData = [{'value': item['count'], 'name': item['level']} for item in level_counts]
    return resultData


# def getRateCharDataOne(province=None):
#     # 在函数内部获取数据
#     if province:
#         travelList = TravelInfo.objects.filter(province=province)
#     else:
#         travelList = getPublicData.getAllTravelInfoMapData()
#
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.star, -1) == -1:
#             startDic[travel.star] = 1
#         else:
#             startDic[travel.star] += 1
#
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#
#     return resultData






# def getRateCharDataTwo(province=None):
#     if province:
#         travelList = TravelInfo.objects.filter(province=province)
#     else:
#         travelList = getPublicData.getAllTravelInfoMapData()
#
#     startDic = {}
#     for travel in travelList:
#         if startDic.get(travel.score, -1) == -1:
#             startDic[travel.score] = 1
#         else:
#             startDic[travel.score] += 1
#
#     resultData = []
#     for key, value in startDic.items():
#         resultData.append({
#             'name': key,
#             'value': value
#         })
#
#     return resultData



def getRateCharDataOne(province=None):
    if province:
        travelList = TravelInfo.objects.filter(province=province)
    else:
        travelList = TravelInfo.objects.all()
    startDic = {}
    for travel in travelList:
        if startDic.get(travel.star, -1) == -1:
            startDic[travel.star] = 1
        else:
            startDic[travel.star] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData



# wx01/app/utils/getEchartsData.py
def getRateCharDataTwo(province=None):
    if province:
        travelList = TravelInfo.objects.filter(province=province)
    else:
        travelList = TravelInfo.objects.all()
    startDic = {}
    for travel in travelList:
        if startDic.get(travel.score, -1) == -1:
            startDic[travel.score] = 1
        else:
            startDic[travel.score] += 1
    resultData = []
    for key, value in startDic.items():
        resultData.append({
            'name': key,
            'value': value
        })
    return resultData






def getPriceCharDataOne(province=None):
    if province:
        traveList = TravelInfo.objects.filter(province=province)
    else:
        traveList = getPublicData.getAllTravelInfoMapData()

    xData = ['免费', '100元以内', '200元以内', '300元以内', '400元以内', '500元以内', '500元以外']
    yData = [0 for _ in range(len(xData))]
    for travel in traveList:
        try:
            price = float(travel.price)
            if price <= 10:
                yData[0] += 1
            elif price <= 100:
                yData[1] += 1
            elif price <= 200:
                yData[2] += 1
            elif price <= 300:
                yData[3] += 1
            elif price <= 400:
                yData[4] += 1
            elif price <= 500:
                yData[5] += 1
            elif price > 500:
                yData[6] += 1
        except ValueError:
            # 处理价格无法转换为浮点数的情况
            continue

    return xData, yData


def getPriceCharDataTwo(province=None):
    if province:
        traveList = TravelInfo.objects.filter(province=province)
    else:
        traveList = getPublicData.getAllTravelInfoMapData()

    xData = [str(x * 300) + '份以内' for x in range(1, 15)]
    yData = [0 for x in range(len(xData))]
    for travel in traveList:
        try:
            saleCount = float(travel.saleCount)
            for x in range(1, 15):
                count = x * 300
                if saleCount <= count:
                    yData[x - 1] += 1
                    break
        except ValueError:
            # 处理销量无法转换为浮点数的情况
            continue

    return xData, yData


def getPriceCharDataThree(province=None):
    if province:
        traveList = TravelInfo.objects.filter(province=province)
    else:
        traveList = getPublicData.getAllTravelInfoMapData()

    discount_dict = {}
    for travel in traveList:
        if travel.discount:
            discount = travel.discount
            if discount in discount_dict:
                discount_dict[discount] += 1
            else:
                discount_dict[discount] = 1

    result_data = []
    for discount, count in discount_dict.items():
        result_data.append({
            'value': count,
            'name': f"{discount}折"
        })

    return result_data




  # 其他函数保持不变











def getCommentsCharDataOne(province=None):
    # 获取评论数据（支持省份过滤）
    commentsList = []
    if province:
        travels = TravelInfo.objects.filter(province__icontains=province)
        for travel in travels:
            try:
                comments = json.loads(travel.comments)
                commentsList.extend(comments)
            except:
                continue
    else:
        # 使用函数内部查询替代全局变量
        commentsList = getPublicData.getAllCommentsData()

    # 原有处理逻辑
    xData = []

    def get_list(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').timestamp()

    for comment in commentsList:
        xData.append(comment['date'])
    xData = list(set(xData))
    xData = sorted(xData, key=lambda x: get_list(x), reverse=True)
    yData = [0] * len(xData)
    for comment in commentsList:
        for index, date in enumerate(xData):
            if comment['date'] == date:
                yData[index] += 1
    return xData, yData


def getCommentsCharDataTwo(province=None):
    # 获取评论数据（支持省份过滤）
    commentsList = []
    if province:
        travels = TravelInfo.objects.filter(province__icontains=province)
        for travel in travels:
            try:
                comments = json.loads(travel.comments)
                commentsList.extend(comments)
            except:
                continue
    else:
        # 使用函数内部查询替代全局变量
        commentsList = getPublicData.getAllCommentsData()

    # 原有处理逻辑
    startDic = {}
    for comment in commentsList:
        score = comment['score']
        startDic[score] = startDic.get(score, 0) + 1
    return [{'name': k, 'value': v} for k, v in startDic.items()]


def getCommentsCharDataThree(province=None):
    # 获取景点数据（支持省份过滤）
    travels = TravelInfo.objects.all()
    if province:
        travels = travels.filter(province__icontains=province)

    # 原有处理逻辑
    xData = [f"{x * 1000}条以内" for x in range(1, 20)]
    yData = [0] * len(xData)
    for travel in travels:
        try:
            count = int(travel.commentsLen)
            for i in range(19):
                if count <= (i + 1) * 1000:
                    yData[i] += 1
                    break
        except:
            continue
    return xData, yData