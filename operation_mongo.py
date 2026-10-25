import pymongo

connection_string = "mongodb+srv://tikape:NAq8a4pNLWF8TMfd@cluster0.u4vehy9.mongodb.net/"
client = pymongo.MongoClient(connection_string)

database = client.get_database("tikape")
apartments = database["apartments"]

# 1. Monessako asunnossa postinumero on 00700?
count_postal_code = apartments.count_documents({
    "zip_code": "00700"
})
print("Asunnot postinumerolla 00700:", count_postal_code)

# 2. Monessako asunnossa rakennusvuosi on 2000-luvulla?
count_construction_year = apartments.count_documents({
    "construction_year": {"$gte": 2000, "$lte": 2099}
})
print("2000-luvulla rakennetut asunnot:", count_construction_year)

# 3. Monessako asunnossa pinta-ala on välillä 50–70 m²?
count_apartment_size = apartments.count_documents({
    "apartment_size": {"$gte": 50, "$lte": 70}
})
print("Pinta-alaltaan 50-70 m²:n asunnot:", count_apartment_size)

# 4. Moniko asunnoista on myyty ainakin kerran vuosina 2010–2012?
count_transactions = apartments.count_documents({
    "transactions.date": {"$gte": "2010-01-01", "$lt": "2013-01-01"}
})
print("Vuosina 2010-2012 myydyt asunnot:", count_transactions)

# 5. Mikä on kallein asunnon myyntihinta aineistossa?
result = apartments.aggregate([
    {"$unwind": "$transactions"},
    {"$sort": {"transactions.selling_price": -1}},
    {"$limit": 1}
])

for apartment in result:
    print("Korkein myyntihinta:", apartment["transactions"]["selling_price"])

client.close()
