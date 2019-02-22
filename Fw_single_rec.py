# import random
#
# with open('Fw_user_data.txt', 'a', encoding='utf8') as f:
#     user_data = {}
#     for i in range(5000):
#         id = random.randint(1, 700)
#         goods_id = random.randint(0, 440)
#         score = random.randint(1, 5)
#         ...
#         string = 'user' + str(id) + '\t' + str(goods_id)
#         if string not in user_data:
#             user_data.setdefault(string, -1)
#             user_data[string] = score
#     for key, value in user_data.items():
#         f.write(key + '\t' + str(value) + '\n')
# """基于单个商品的推荐算法
#     购买过此商品的用户还购买过
#
#     初始数据：包含用户-商品-评分的txt文件
#         by 范唯"""
from operator import itemgetter


#   每一行格式为：用户-商品-评分
#   {用户id：[商品id，商品id]}
# 1.从txt文件中拿到数据
def get_data(filename):
    user_goods = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            userid, goods_id, score = line.split('\t')
            if userid not in user_goods:
                user_goods.setdefault(userid, [])
            user_goods[userid].append(goods_id)
    return user_goods


# 2.找出购买过对应商品的用户
# 3.把所有符合条件的用户购买记录统计，(剔除指定商品)以商品出现的频次倒叙排列取top10
# {goods_id1:512, goods_id2:612}
def get_rec(good_id):
    filename = 'Fw_user_data.txt'
    user_goods = get_data(filename)
    goods_allusers = []
    for i in user_goods:
        if good_id in user_goods[i]:
            goods_allusers.append(i)
    usergrecord = {}
    for i in user_goods:
        for j in goods_allusers:
            if i == j:
                for k in user_goods[i]:
                    if k != good_id:
                        if k not in usergrecord:
                            usergrecord.setdefault(k, 1)
                        else:
                            count = usergrecord.get(k) + 1
                            usergrecord[k] = count

    sorted_d = sorted(usergrecord.items(), key=itemgetter(1), reverse=True)[:20]
    return sorted_d


def single_rec_data(good_id='1361'):
    li1 = []
    li = get_rec(good_id)
    for i in li:
        li1.append(i[0])
    return li1[:6]

