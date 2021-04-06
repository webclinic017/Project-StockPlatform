# pymongo 사용 모듈 추출
import pymongo
import json 

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import userSerializer,strategySerializer,resultSerializer

from .models import User, Strategy, Result

from .rebalancing.test import get_indicator_from_json
from .rebalancing.test import returnListObj

from .rebalancing import test_backtesting
from .rebalancing.test_backtesting_class_collection import Init_data,User_input_data,Stock_trading_indicator,Result,Loging

from bson import ObjectId
from bson import json_util, ObjectId

# =============== for dict to json ==================
# =================================================== 

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

# =============== for mongodb save ==================
# =================================================== 

def printResultObj(resultObj):
	print("strategy_result_test")
	print("writer_name_test")
	print(resultObj.profit_all)
	print(resultObj.currentAsset)
	print(resultObj.cagr)
	print(resultObj.Reavalanced_code_name_dic)
	print(resultObj.Assets_by_date_list)
	print(resultObj.win)
	print(resultObj.lose)


def saveResultInMongo(resultObj):
	client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.kjrlb.mongodb.net/<pnu_sgm_platformdata>?retryWrites=true&w=majority")    # 파이몽고 사용해서
	db = client.pnu_sgm_platformdata
	returnObj = {
		'strategy_result_id' : resultObj.strategy_number,
		'writer_name_id' : resultObj.writer_id,
		'profit_all' : resultObj.profit_all,
		'currentAsset' : resultObj.currentAsset,
		'Final_yield' : resultObj.cagr,
		'selected_companys' : str(resultObj.Reavalanced_code_name_dic),
		'Current_assets_by_date' : resultObj.Assets_by_date_list,
		'Winning_rate' : resultObj.win,
		'Reavalanced_code_name_list' : str(resultObj.Reavalanced_code_name_dic)
	}
	db.Results.insert_one(returnObj)
	
	return returnObj


# ================= user crud ======================= 
# ===================================================

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		# user api 예시
		'User List':'/user-list/',
		'User Detail':'/user-detail/<str:pk>/',
		'User Create':'/user-create/',
		'User Update':'/user-update/<str:pk>/',
		'User Delete':'/user-delete/<str:pk>/',
		# strategy api 예시
		'Strategy List':'/strat-list/',
		'Strategy Detail':'/strat-detail/<str:pk>/',
		'Strategy Create':'/strat-create/',
		'Strategy Update':'/strat-update/<str:pk>/',
		'Strategy Delete':'/strat-delete/<str:pk>/',
		# Result api 예시
		'Result List':'/result-list/',
		'Result Detail':'/result-detail/<str:pk>/',
		'(Do not use)Result Create':'/result-create/',
		'(Do not use)Result Update':'/result-update/<str:pk>/',
		'(Do not use)Result Delete':'/result-delete/<str:pk>/',
		}
	
	
	return Response(api_urls)


@api_view(['GET'])
def userList(request):
	users = User.objects.all().order_by('-id')
	serializer = userSerializer(users, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def userDetail(request, pk):
	user = User.objects.get(id=pk)
	serializer = userSerializer(user, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def userCreate(request):
	serializer = userSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['POST'])
def userUpdate(request, pk):
	user = User.objects.get(id=pk)
	serializer = userSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def userDelete(request, pk):
	user = User.objects.get(id=pk)
	user.delete()

	return Response('user succsesfully delete!')

# ================= stretagy crud ===================
# =================================================== 

@api_view(['GET'])
def strategyList(request):
	strategys = Strategy.objects.all().order_by('-id')
	serializer = strategySerializer(strategys, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def strategyDetail(request, pk):
	strategys = Strategy.objects.get(id=pk)
	serializer = strategySerializer(strategys, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def strategyCreate(request):
    # strategy data from request
	serializer = strategySerializer(data=request.data)
	# save it in mongodb
	if serializer.is_valid():
		serializer.save()
		print("strategy is saved!")
	# data preprocessing (userparameters -> indicator list, max valuelist, min valuelist) 
	listObj1=get_indicator_from_json(request.data)
	print(listObj1.INDICATOR_LIST)
	print(listObj1.INDICATOR_MIN_LIST)
	print(listObj1.INDICATOR_MAX_LIST)
	# make backtesting object
	initData = Init_data()
	userInputData = User_input_data()

	userInputData.set_basic_data(request.data["investment"],request.data["investment_Start"],request.data["investment_End"])
	userInputData.set_indicator_data(listObj1.INDICATOR_LIST,listObj1.INDICATOR_MIN_LIST,listObj1.INDICATOR_MAX_LIST)
	userInputData.set_backtesting_data(request.data["purchaseCondition"]/10,request.data["targetPrice"]/10,request.data["sellPrice"]/10)
	
	stockTradingIndicator = Stock_trading_indicator()
	result = Result(request.data["writerName"])
	result.strategy_number = request.data["strategyNumber"]
	log = Loging()

	resultObj = test_backtesting.backtesting(initData,userInputData,stockTradingIndicator,result,log)
	# save backtested result in mongodb 
	objTypeResult = saveResultInMongo(resultObj)
	print("dictionarytype return value")
	#print(objTypeResult)
	#print(type(objTypeResult))
	# objTypeResult = JSONEncoder().encode(objTypeResult)
	objTypeResult = json.loads(json_util.dumps(objTypeResult))
	print("jsontype return value")
	#print(objTypeResult)
	#print(type(objTypeResult))

	#return Response(serializer.data)
	return JsonResponse(objTypeResult, safe=False)


@api_view(['POST'])
def strategyUpdate(request, pk):
	strategys = Strategy.objects.get(id=pk)
	serializer = strategySerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def strategyDelete(request, pk):
	strategys = Strategy.objects.get(id=pk)
	strategys.delete()

	return Response('strategy succsesfully delete!')
	
# ================= result crud ===================
# =================================================== 

@api_view(['GET'])
def resultList(request):
	results = Result.objects.all().order_by('-id')
	serializer = resultSerializer(results, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def resultDetail(request, pk):
	results = Result.objects.get(id=pk)
	serializer = resultSerializer(results, many=False)
	return Response(serializer.data)


@api_view(['POST'])
def resultCreate(request):
	serializer = resultSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['POST'])
def resultUpdate(request, pk):
	results = Result.objects.get(id=pk)
	serializer = resultSerializer(instance=task, data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)


@api_view(['DELETE'])
def resultDelete(request, pk):
	results = Result.objects.get(id=pk)
	results.delete()

	return Response('result succsesfully delete!')