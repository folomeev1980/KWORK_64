import  requests

url='https://poe.ninja/api/data/itemoverview?league=Metamorph&type=BaseType'
ukr="https://poe.ninja/api/data/itemoverview?league=Metamorph&type=BaseType"

r=requests.get(url)
q=r.text
print(len(q))
print(r.text)
#print(r.json())