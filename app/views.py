#render函数用于将数据渲染到指定的模板中，并返回生成的HTML内容
#redirect允许你将用户从一个URL重定向到另一个URL，通常用于处理单表提交、用户登录、注册等操作后的页面跳转
from django.db import models  # 核心修正点
from django.db.models import Q
from django.shortcuts import render,redirect
from app.models import User, TravelInfo, Comment
from app.recommdation import getUser_ratings,user_bases_collaborative_filtering
from app.utils import errorResponse,getHomeData,getPublicData,getChangeSelfInfoData,getAddCommentsData,getEchartsData,getRecommendationData
from django.contrib.auth.hashers import check_password  # 用于安全验证密码
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render
from app.models import TravelInfo
from app.utils import getPublicData, getEchartsData


#todo  新的登录模块代码
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        # todo 新增验证码模块  start
        # 新增验证码验证逻辑
        captcha_input = request.POST.get('captcha', '').lower().strip()  # 获取并处理输入
        captcha_session = request.session.get('captcha', '').lower()  # 获取session存储值
        # 验证码校验（顺序不能颠倒）
        if not captcha_input:
            return errorResponse.errorResponse(request, '验证码不能为空')
        if captcha_input != captcha_session:
            return errorResponse.errorResponse(request, '验证码错误')
        # 验证通过后立即删除session中的验证码
        if 'captcha' in request.session:
            del request.session['captcha']
        # todo 新增验证码模块  end

        username = request.POST.get('username')
        password = request.POST.get('password')

        # 基本输入校验
        if not username or not password:
            return errorResponse.errorResponse(request, '用户名和密码不能为空')

        try:
            # 1. 查询用户是否存在
            user = User.objects.get(username=username)

            # 2. 使用 check_password 验证密码（与注册时的 make_password 匹配）
            if check_password(password, user.password):
                # 3. 登录成功：设置 session
                request.session['username'] = username
                return redirect('/app/home')
            else:
                # 密码错误
                return errorResponse.errorResponse(request, '账号或密码错误')

        except User.DoesNotExist:
            # 用户不存在
            return errorResponse.errorResponse(request, '账号或密码错误')

#todo  新的注册模块代码
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # 校验输入
        if not username or not password or not confirm_password:
            return errorResponse.errorResponse(request, '不允许为空值')
        if password != confirm_password:
            return errorResponse.errorResponse(request, '两次密码不一致')

        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            return errorResponse.errorResponse(request, '该账号已存在')

        # 创建用户（使用 make_password 加密）
        user = User(username=username)
        user.set_password(password)  # 自动加密
        user.save()

        return redirect('/app/login')

def logOut(request):
    request.session.clear() #退出登录时，清除request.session
    return redirect('/app/login') #退出登录 转到登陆页面

# def home(request):
#     username = request.session.get('username')
#     userInfo = User.objects.get(username=username)
#     a5Len,commentsLenTitle,provienceDicSort = getHomeData.getHomeTagData()
#     scoreTop10Data,saleCountTop10 = getHomeData.getAnthorData()
#     year,mon,day = getHomeData.getNowTime()
#     geoData = getHomeData.getGeoData()
#     userBarCharData = getHomeData.getUserCreateTimeData()
#     #字典
#     return render(request,'home.html',{
#         'userInfo':userInfo,
#         'a5Len':a5Len,
#         'commentsLenTitle':commentsLenTitle,
#         'provienceDicSort':provienceDicSort,
#         'scoreTop10Data':scoreTop10Data,
#         'nowTime':{
#             'year':year,
#             'mon':getPublicData.monthList[mon - 1],
#             'day':day
#         },
#         'geoData':geoData,
#         'userBarCharData':userBarCharData,
#         'saleCountTop10':saleCountTop10
#     })

def home(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    a5Len, commentsLenTitle, provienceDicSort = getHomeData.getHomeTagData()
    # 获取评分排名前十的景点
    scoreTop10Data = TravelInfo.objects.order_by('-score')[:10]
    saleCountTop10 = getHomeData.getAnthorData()
    year, mon, day = getHomeData.getNowTime()
    geoData = getHomeData.getGeoData()
    userBarCharData = getHomeData.getUserCreateTimeData()

    return render(request, 'home.html', {
        'userInfo': userInfo,
        'a5Len': a5Len,
        'commentsLenTitle': commentsLenTitle,
        'provienceDicSort': provienceDicSort,
        'scoreTop10Data': scoreTop10Data,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'geoData': geoData,
        'userBarCharData': userBarCharData,
        'saleCountTop10': saleCountTop10
    })





def changeSelfInfo(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year,mon,day = getHomeData.getNowTime()
    if request.method == 'POST':
        getChangeSelfInfoData.changeSelfInfo(username,request.POST,request.FILES)
        userInfo = User.objects.get(username=username)

    return render(request,'changeSelfInfo.html',{
        'userInfo':userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })



#todo   新的修改密码代码
def changePassword(request):
    # 验证登录状态
    username = request.session.get('username')
    if not username:
        return redirect('/app/login')

    try:
        userInfo = User.objects.get(username=username)
    except User.DoesNotExist:
        return errorResponse.errorResponse(request, '用户不存在')

    if request.method == 'POST':
        # 获取表单数据（字段名称与前端完全一致）
        old_password = request.POST.get('oldPassword', '').strip()  # 注意这里是 oldPassword
        new_password = request.POST.get('newPassword', '').strip()  # 注意这里是 newPassword
        confirm_password = request.POST.get('newPasswordConfirm', '').strip()  # 注意这里是 newPasswordConfirm

        # 字段非空校验
        if not all([old_password, new_password, confirm_password]):
            return errorResponse.errorResponse(request, '所有字段不能为空')

        # 验证旧密码
        if not userInfo.check_password(old_password):
            return errorResponse.errorResponse(request, '原密码错误')

        # 验证新密码一致性
        if new_password != confirm_password:
            return errorResponse.errorResponse(request, '两次新密码不一致')

        # 更新密码
        userInfo.set_password(new_password)
        userInfo.save()

        # 清除会话并跳转登录
        request.session.flush()
        return redirect('/app/home')

    # GET请求处理（保持原有时间逻辑）
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'changePassword.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
    })




# todo 新增搜索功能和分页功能

# def tableData(request):
#     # 用户信息获取
#     username = request.session.get('username')
#     try:
#         userInfo = User.objects.get(username=username)
#     except User.DoesNotExist:
#         # 处理用户不存在的情况，这里可以重定向到登录页
#         return redirect('login')
#
#     # 获取当前时间
#     year, mon, day = getHomeData.getNowTime()
#
#     # 获取初始查询集（确保返回的是QuerySet）
#     try:
#         # 如果getAllTravelInfoMapData返回的是QuerySet
#         queryset = getPublicData.getAllTravelInfoMapData()
#         # 保险检查：如果不是QuerySet则重新获取
#         if not isinstance(queryset, models.QuerySet):
#             queryset = TravelInfo.objects.all()
#     except Exception as e:
#         # 处理异常情况，使用备用查询方式
#         queryset = TravelInfo.objects.all()
#
#     # 处理搜索关键词
#     keyword = request.GET.get('keyword', '').strip()
#     if keyword:
#         queryset = queryset.filter(
#             Q(title__icontains=keyword) |
#             Q(province__icontains=keyword) |
#             Q(level__icontains=keyword)
#         ).distinct()
#
#     # 分页处理（带安全限制）
#     paginator = Paginator(queryset, 10)  # 每页10条
#     page_number = request.GET.get('page', 1)
#
#     # 安全处理页码参数
#     try:
#         page_number = int(page_number)
#         if page_number < 1 or page_number > 10:  # 限制最多显示10页
#             page_number = 1
#     except (ValueError, TypeError):
#         page_number = 1
#
#     try:
#         talbeData = paginator.page(page_number)
#     except EmptyPage:
#         # 如果页码超出范围，返回最后一页
#         talbeData = paginator.page(paginator.num_pages)
#
#     # 构造上下文
#     context = {
#         'userInfo': userInfo,
#         'nowTime': {
#             'year': year,
#             'mon': getPublicData.monthList[mon - 1],
#             'day': day
#         },
#         'talbeData': talbeData,
#         'search_keyword': keyword,
#         'paginator': paginator
#     }
#
#     return render(request, 'tableData.html', context)



#wx 2025.6.12
def tableData(request):
    # 用户信息获取
    username = request.session.get('username')
    try:
        userInfo = User.objects.get(username=username)
    except User.DoesNotExist:
        # 处理用户不存在的情况，这里可以重定向到登录页
        return redirect('login')

    # 获取当前时间
    year, mon, day = getHomeData.getNowTime()

    # 获取初始查询集（确保返回的是QuerySet）
    try:
        # 如果getAllTravelInfoMapData返回的是QuerySet
        queryset = getPublicData.getAllTravelInfoMapData()
        # 保险检查：如果不是QuerySet则重新获取
        if not isinstance(queryset, models.QuerySet):
            queryset = TravelInfo.objects.all()
    except Exception as e:
        # 处理异常情况，使用备用查询方式
        queryset = TravelInfo.objects.all()

    # 处理搜索关键词
    keyword = request.GET.get('keyword', '').strip()
    if keyword:
        queryset = queryset.filter(
            Q(title__icontains=keyword) |
            Q(province__icontains=keyword) |
            Q(level__icontains=keyword)
        ).distinct()

    # 对查询集进行排序
    queryset = queryset.order_by('id')  # 按id排序，可根据实际需求修改

    # 分页处理（带安全限制）
    paginator = Paginator(queryset, 10)  # 每页10条
    page_number = request.GET.get('page', 1)

    # 安全处理页码参数
    try:
        page_number = int(page_number)
        if page_number < 1 or page_number > 10:  # 限制最多显示10页
            page_number = 1
    except (ValueError, TypeError):
        page_number = 1

    try:
        talbeData = paginator.page(page_number)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        talbeData = paginator.page(paginator.num_pages)

    # 构造上下文
    context = {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'talbeData': talbeData,
        'search_keyword': keyword,
        'paginator': paginator
    }

    return render(request, 'tableData.html', context)




def addComments(request,id):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    travelInfo = getAddCommentsData.getTravelById(id)

    # todo 修改部分
    # 修改查询条件：删除user过滤，保留景点过滤
    history_comments = Comment.objects.filter(
        travel=travelInfo
    ).select_related('user').order_by('-created_at')  # 使用模型默认排序，可省略

    if request.method == 'POST':
        # 修改后的保存逻辑
        rate = request.POST.get('rate')
        content = request.POST.get('content', '').strip()
        error = None
        if not rate:
            error = "请选择评分！"
        elif not content:
            error = "评论内容不能为空！"
        else:
            try:
                rate = int(rate)
                if rate < 1 or rate > 5:
                    error = "评分必须在1-5分之间！"
            except ValueError:
                error = "无效的评分值！"
        if error:
            return render(request, 'addComments.html', {
                'history_comments': history_comments,
                'userInfo': userInfo,
                'nowTime': {
                    'year': year,
                    'mon': getPublicData.monthList[mon - 1],
                    'day': day
                },
                'travelInfo': travelInfo,
                'id': id,
                'error': error
            })
        Comment.objects.create(
            user=userInfo,
            travel=travelInfo,
            rate=rate,
            content=content
        )
        return redirect('/app/tableData')
    return render(request, 'addComments.html', {
        'history_comments': history_comments,
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'travelInfo':travelInfo,
        'id':id,
    })




# todo 添加新的功能，根据省份去查询
# 修改后的视图函数
def cityChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()

    # 获取所有省份（去重并排序）
    provinces = sorted(TravelInfo.objects.values_list('province', flat=True).distinct())

    # 获取筛选条件
    selected_province = request.GET.get('province', '')

    # 修改点：直接传递省份参数而不是字典
    Xdata, Ydata = getEchartsData.cityCharDataOne(province=selected_province)
    resultData = getEchartsData.cityCharDataTwo(province=selected_province)

    return render(request, 'cityChar.html', {
        'userInfo': userInfo,
        'provinces': provinces,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'cityCharOneData': {
            'Xdata': Xdata,
            'Ydata': Ydata
        },
        'cityCharTwoData': resultData
    })



# def rateChar(request):
#     username = request.session.get('username')
#     userInfo = User.objects.get(username=username)
#     year, mon, day = getHomeData.getNowTime()
#     cityList = getPublicData.getCityList()
#     travelList = getPublicData.getAllTravelInfoMapData(cityList[0])
#     charOneData = getEchartsData.getRateCharDataOne(travelList)
#     charTwoData = getEchartsData.getRateCharDataTwo(travelList)
#     if request.method == 'POST':
#         travelList = getPublicData.getAllTravelInfoMapData(request.POST.get('province'))
#         charOneData = getEchartsData.getRateCharDataOne(travelList)
#         charTwoData = getEchartsData.getRateCharDataTwo(travelList)
#
#
#     return render(request, 'rateChar.html', {
#         'userInfo': userInfo,
#         'nowTime': {
#             'year': year,
#             'mon': getPublicData.monthList[mon - 1],
#             'day': day
#         },
#         'cityList':cityList,
#         'charOneData':charOneData,
#         'charTwoData':charTwoData
#     })


# ... 前面代码保持不变 ...
#wx  2025.6.12
# def rateChar(request):
#     username = request.session.get('username')
#     userInfo = User.objects.get(username=username)
#     year, mon, day = getHomeData.getNowTime()
#
#     # 获取所有省份列表
#     provinces = sorted(TravelInfo.objects.values_list('province', flat=True).distinct())
#
#     # 设置默认省份
#     default_province = ""
#     if provinces:
#         default_province = provinces[0]
#     else:
#         # 如果没有省份数据，尝试获取默认省份
#         try:
#             first_travel = TravelInfo.objects.first()
#             if first_travel:
#                 default_province = first_travel.province
#             else:
#                 default_province = "北京"
#         except:
#             default_province = "北京"
#
#     # 获取当前省份参数
#     province = request.POST.get('province', default_province)
#
#     # 使用省份参数获取图表数据
#     charOneData = getEchartsData.getRateCharDataOne(province=province)
#     charTwoData = getEchartsData.getRateCharDataTwo(province=province)
#
#     return render(request, 'rateChar.html', {
#         'userInfo': userInfo,
#         'nowTime': {
#             'year': year,
#             'mon': getPublicData.monthList[mon - 1],
#             'day': day
#         },
#         'provinces': provinces,  # 传递省份列表给模板
#         'selected_province': province,  # 当前选中的省份
#         'charOneData': charOneData,
#         'charTwoData': charTwoData
#     })

# app/views.py

import datetime

# wx01/app/views.py
def rateChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()

    # 获取所有省份列表
    provinces = sorted(TravelInfo.objects.values_list('province', flat=True).distinct())

    # 设置默认省份
    default_province = ""
    if provinces:
        default_province = provinces[0]
    else:
        try:
            first_travel = TravelInfo.objects.first()
            if first_travel:
                default_province = first_travel.province
            else:
                default_province = "北京"
        except:
            default_province = "北京"

    # 获取当前省份参数
    province = request.POST.get('province', default_province)

    # 使用省份参数获取图表数据
    charOneData = getEchartsData.getRateCharDataOne(province)
    charTwoData = getEchartsData.getRateCharDataTwo(province)

    return render(request, 'rateChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'provinces': provinces,  # 传递省份列表给模板
        'selected_province': province,  # 当前选中的省份
        'charOneData': charOneData,
        'charTwoData': charTwoData
    })

# ... 删除文件末尾重复的 rateChar 函数定义 ...





# todo 价格和月销量分析新增加省份功能
# def priceChar(request):
#     username = request.session.get('username')
#     userInfo = User.objects.get(username=username)
#     year, mon, day = getHomeData.getNowTime()
#
#     # 获取原始数据（直接使用ORM查询集）
#     queryset = TravelInfo.objects.all()  # 直接获取模型对象列表
#
#     # 处理省份筛选（不区分大小写）
#     province = request.GET.get('province', '').strip()
#     if province:
#         queryset = queryset.filter(province__icontains=province)
#
#     # 直接传递模型对象列表（不要转成字典）
#     travel_list = list(queryset)  # 这里是关键改动！！！
#
#     # 生成图表数据
#     xData, yData = getEchartsData.getPriceCharDataOne(travel_list)
#     x1Data, y1Data = getEchartsData.getPriceCharDataTwo(travel_list)
#     disCountPieData = getEchartsData.getPriceCharDataThree(travel_list)
#
#     return render(request, 'priceChar.html', {
#         'userInfo': userInfo,
#         'nowTime': {
#             'year': year,
#             'mon': getPublicData.monthList[mon - 1],
#             'day': day
#         },
#         'echartsData': {
#             'xData': xData,
#             'yData': yData,
#             'x1Data': x1Data,
#             'y1Data': y1Data,
#             'disCountPieData': disCountPieData
#         }
#     })



#wx 2525.6.12
def priceChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()

    # 获取所有省份列表
    provinces = sorted(TravelInfo.objects.values_list('province', flat=True).distinct())

    # 设置默认省份
    default_province = ""
    if provinces:
        default_province = provinces[0]
    else:
        try:
            first_travel = TravelInfo.objects.first()
            if first_travel:
                default_province = first_travel.province
            else:
                default_province = "北京"
        except:
            default_province = "北京"

    # 获取省份参数
    province = request.GET.get('province', default_province)

    # 使用省份参数获取图表数据
    xData, yData = getEchartsData.getPriceCharDataOne(province=province)
    x1Data, y1Data = getEchartsData.getPriceCharDataTwo(province=province)
    disCountPieData = getEchartsData.getPriceCharDataThree(province=province)

    return render(request, 'priceChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'provinces': provinces,  # 传递省份列表给模板
        'selected_province': province,  # 当前选中的省份
        'echartsData': {
            'xData': xData,
            'yData': yData,
            'x1Data': x1Data,
            'y1Data': y1Data,
            'disCountPieData': disCountPieData
        }
    })






# todo 新增根据省份去查询数据
def commentsChar(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    province = request.GET.get('province')  # 获取省份参数

    # 根据省份参数获取对应数据
    if province:
        xData, yData = getEchartsData.getCommentsCharDataOne(province)
        commentsScorePieData = getEchartsData.getCommentsCharDataTwo(province)
        x1Data, y1Data = getEchartsData.getCommentsCharDataThree(province)
    else:
        xData, yData = getEchartsData.getCommentsCharDataOne()
        commentsScorePieData = getEchartsData.getCommentsCharDataTwo()
        x1Data, y1Data = getEchartsData.getCommentsCharDataThree()

    return render(request, 'commentsChar.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'echartsData': {
            'xData': xData,
            'yData': yData,
            'commentsScorePieData': commentsScorePieData,
            'x1Data': x1Data,
            'y1Data': y1Data
        }
    })



def recommendation(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    try:
        user_ratings = getUser_ratings()
        recommended_items = user_bases_collaborative_filtering(userInfo.id, user_ratings)
        resultDataList = getRecommendationData.getAllTravelByTitle(recommended_items)
    except:
        resultDataList = getRecommendationData.getRandomTravel()

    return render(request, 'recommendation.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        },
        'resultDataList':resultDataList
    })

def detailIntroCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'detailIntroCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })

def commentContentCloud(request):
    username = request.session.get('username')
    userInfo = User.objects.get(username=username)
    year, mon, day = getHomeData.getNowTime()
    return render(request, 'commentContentCloud.html', {
        'userInfo': userInfo,
        'nowTime': {
            'year': year,
            'mon': getPublicData.monthList[mon - 1],
            'day': day
        }
    })


# todo  添加图片验证码功能
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from .utils.captcha import generate_captcha
from io import BytesIO
@require_GET
def captcha_view(request):  # 重命名视图函数
    # 生成验证码
    text, image = generate_captcha()  # 直接调用函数
    # 将验证码文本存入session
    request.session['captcha'] = text
    # 生成图片响应
    buf = BytesIO()
    image.save(buf, format='PNG')
    return HttpResponse(buf.getvalue(), content_type='image/png')









