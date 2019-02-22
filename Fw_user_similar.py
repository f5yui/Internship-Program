"""基于用户相似度的协同过滤推荐算法

    初始数据：txt文本，一行表示一个用户对一件购买过的商品的评分
    最终结果：作为推荐的商品的编号的列表
        by范唯"""
from math import sqrt
from operator import itemgetter


# 1.拿到用户购买的所有商品信息&所有商品信息

# 用户购买的所有商品信息：user_goods_info
# {id:[goods_id,...],
# ...}
# 所有商品信息 goods_info
# {goods_id:[name,price,...],
# ...}
def get_data():
    filename = 'Fw_user_data.txt'
    user_goods_info = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            userid, goods_id, score = line.split('\t')
            if userid not in user_goods_info:
                user_goods_info.setdefault(userid, [])
            user_goods_info[userid].append(goods_id)
    return user_goods_info


# 2.计算用户两两之间共同购买的商品数
def get_goods_num(user_goods_info):
    # {u:{v:12, vv:15, vvv:25,...}, v:{u:12}}
    user_similar = {}
    # 2.列表->集合->交集数
    for u in user_goods_info:
        for v in user_goods_info:
            u_set = set(user_goods_info[u])
            v_set = set(user_goods_info[v])
            if u not in user_similar:
                user_similar.setdefault(u, {})
            if v not in user_similar[u]:
                user_similar[u].setdefault(v, 0)
            user_similar[u][v] = len(u_set & v_set)
    return user_similar


# 3.使用余弦公式计算两两用户之间的相似度
def get_user_similar(user_goods_info, user_similar):
    # 余弦公式
    # A,B共同购买的商品数/sqrt(A购买的商品数*B购买的商品数)
    # A商品数=len(user_goods_info[A])
    for u, uvw in user_similar.items():
        for v, counts in uvw.items():
            u_counts = len(user_goods_info[u])
            v_counts = len(user_goods_info[v])
            # {u:{v:0.751254, vv:0.85452, vvv:0.951245,...}, v:{u:0.12454}}
            user_similar[u][v] = counts / sqrt(u_counts * v_counts)
    return user_similar


# 4.针对指定用户，拿到与他最相似的10个用户  15
def get_similar_user(user_id, user_similar):
    similar_users = []
    user_similar_dict = user_similar.get(user_id, -1)
    # 排序取top10
    user_similar_dict_sorted = sorted(user_similar_dict.items(), key=itemgetter(1), reverse=True)[1:20]
    for similar_user in user_similar_dict_sorted:
        similar_users.append(similar_user[0])
    return similar_users


# 5.统计这10个用户购买过的商品，剔除目标用户已购买的商品，商品的推荐指数为用户相似度相加，倒排取top5   20
# 拿到最终作为推荐的商品编号列表
# {goods_id:0.454512+0.784512+0.9451245}

def get_similar_goods(user_goods_info, user_id, similar_users, user_similar):
    goods_similar = {}
    similar_good = []
    for u in similar_users:
        for v in user_goods_info[u]:
            if v not in user_goods_info[user_id]:
                if v not in goods_similar:
                    goods_similar.setdefault(v, user_similar[user_id][u])
                goods_similar[v] = goods_similar[v] + user_similar[user_id][u]
    # 排序取top5
    goods_similar_sorted = sorted(goods_similar.items(), key=itemgetter(1), reverse=True)[0:10]
    for similar_goods in goods_similar_sorted:
        similar_good.append(similar_goods[0])
    return similar_good

    # 7.在总商品信息数据中找到编号对应的商品信息，传递给web页面显示


def user_similar_data(uid='user53'):
    data = get_data()
    a = get_user_similar(data, get_goods_num(data))
    user = get_similar_user(uid, a)
    b = get_similar_goods(data, uid, user, a)
    return b[:6]

