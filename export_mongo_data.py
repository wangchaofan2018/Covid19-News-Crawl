import xlwt
import pymongo
import covid_19.settings as settings
import sys

client = pymongo.MongoClient(settings.MONGO_DB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
workbook = xlwt.Workbook()
sheet = workbook.add_sheet("数据统计")

titles = ["日期","地点","出席人员","标题","新闻概要","网页地址","详细内容"]
for index in range(len(titles)):
    sheet.write(0,index,titles[index])

cur = 1
site = sys.argv[1]
mydoc = collection.find()
if site == "hubei":
    mydoc = collection.find({"location":"湖北"})
elif site == "shanxi":
    mydoc = collection.find({"location":"山西"})
for item in mydoc:
    detail_url = item["detail_url"]
    sheet.write(cur,0,item["publish_time"])
    sheet.write(cur,1,item["location"])
    sheet.write(cur,2,item["attend_persons"])
    sheet.write(cur,3,item["title"])
    sheet.write(cur,4,item["summary"])
    sheet.write(cur,5,xlwt.Formula('HYPERLINK("%s")'%detail_url))#item["detail_url"])
    sheet.write(cur,6,item["content"])
    cur = cur+1

workbook.save("新闻发布会相关.xls")
print("job finish")
    