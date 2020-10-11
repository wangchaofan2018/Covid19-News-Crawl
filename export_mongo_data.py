import xlwt
import pymongo
import covid_19.settings as settings
import sys

client = pymongo.MongoClient(settings.MONGO_DB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("数据统计")

titles = ["日期","省份","发布地点","出席人员","标题","新闻概要","网页地址","详细内容"]
for index in range(len(titles)):
    sheet.write(0,index,titles[index])

cur = 1
site = sys.argv[1]
mydoc = collection.find()
name = ""
if site == "hubei":
    name = "湖北"
    mydoc = collection.find({"location":name})
elif site == "shanxi":
    name = "山西"
    mydoc = collection.find({"location":name})
elif site == "anhui":
    name = "安徽"
    mydoc = collection.find({"location":name})
elif site == "heilongjiang":
    name = "黑龙江"
    mydoc = collection.find({"location":name})
elif site == "jilin":
    name = "吉林"
    mydoc = collection.find({"location":name})
elif site == "liaoning":
    name = "辽宁"
    mydoc = collection.find({"location":name})
elif site == "zhejiang":
    name = "浙江"
    mydoc = collection.find({"location":name})
for item in mydoc:
    detail_url = item["detail_url"]
    sheet.write(cur,0,item["publish_time"])
    sheet.write(cur,1,item["province"])
    sheet.write(cur,2,item["location"])
    sheet.write(cur,3,item["attend_persons"])
    sheet.write(cur,4,item["title"])
    summary = ""
    #先写死
    if name=="黑龙江" or name=="山西" or name=="湖北":
        summary = item["summary"]
    sheet.write(cur,5,summary)
    sheet.write(cur,6,xlwt.Formula('HYPERLINK("%s")'%detail_url))#item["detail_url"])
    sheet.write(cur,7,item["content"])
    cur = cur+1

workbook.save("%s-数据.xls"%name)

    