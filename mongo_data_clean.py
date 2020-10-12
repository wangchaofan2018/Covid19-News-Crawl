import pymongo
import covid_19.settings as settings
import sys
from flashtext import KeywordProcessor

client = pymongo.MongoClient(settings.MONGO_DB_URI)
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]
deleteColl = db["deleteColl"]
mydoc = collection.find()
kw_list = ["新冠","疫情","抗疫","病例","冠状病毒"]
filter_list = ["扫黑除恶","自由贸易","光盘行动"]
keyword_processor = KeywordProcessor()
for keyword in kw_list:
    keyword_processor.add_keyword(keyword)
for item in mydoc:
    find_title = keyword_processor.extract_keywords(item["title"])
    find_content = keyword_processor.extract_keywords(item["content"])
    total_score = len(find_title)*2+len(find_content)
    if total_score<=5:
        myDeleteQuery = {"_id":item["_id"]}
        item.pop("_id")
        deleteColl.insert_one(item)
        collection.delete_one(myDeleteQuery)
    