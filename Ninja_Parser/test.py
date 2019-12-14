list_=["Essence","DivinationCard","BaseType","Prophecy","HelmetEnchant","UniqueJewel","UniqueFlask","UniqueWeapon","UniqueArmour","UniqueAccessory"]

def make_url(lst):
    urls_lst=[]
    for i in lst:
        a="https://poe.ninja/api/data/itemoverview?league=Metamorph&type="+i
        urls_lst.append((i,a))
    return urls_lst


print(make_url(list_))