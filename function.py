import Fw_single_rec
import Fw_user_similar
import Fw_goods_similar
import random


def get_data():
    food_info = {}
    base_info = {}
    filename = 'Fw_data.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            info_list = line.split('\t')
            food_id = info_list.pop(0)
            food_info.setdefault(food_id, [])
            food_info[food_id] = info_list
    for i in range(1, 31):
        base_info.setdefault(str(i), [])
        base_info[str(i)] = food_info[str(i)]
    return food_info, base_info


def rec_data(index):
    filename = 'Fw_data.txt'
    food_info, base_info = get_data()
    userid = 'user' + str(random.randint(1, 700))
    rec_id1 = Fw_user_similar.user_similar_data(userid)
    rec_id2 = Fw_single_rec.single_rec_data(str(index))
    rec_info1 = {}
    rec_info2 = {}
    for item in rec_id1:
        if item in food_info:
            rec_info1.setdefault(item, food_info[item])
    for item in rec_id2:
        if item in food_info:
            rec_info2.setdefault(item, food_info[item])

    return rec_info1, rec_info2


def rec3_data():
    food_info, base_info = get_data()
    rec_info = {}
    rec_id = Fw_goods_similar.good_similar_data()
    for item in rec_id:
        if item in food_info:
            rec_info.setdefault(item, food_info[item])

    return rec_info


def use_data(get_id):
    food_info, base_info = get_data()
    get_info = []
    if get_id in food_info:
        for i in food_info[get_id]:
            get_info.append(i)
    return get_info
