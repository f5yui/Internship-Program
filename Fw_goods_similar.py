"""1.拿到所有商品的信息，分为标准集和推荐集
		标准集：你这一页显示的商品（30个）
		推荐集：剩下的所有商品
	2.拿到标准集30的共同重要程度top10的词A
	3.拿到推荐集的每一本书的top5重要程度的词B
	4.对每一计算（A∩B）/（A∪B）
	5.倒排取top10的书进行推荐
	最后结果依然是一个列表，包含被推荐的编号

	初始数据：txt文本，每一行表示一个商品的具体信息
	    by 范唯"""
import jieba.analyse
from operator import itemgetter


# 1.读到所有的数据，分为标准集和推荐集
# 标准集：你这一页显示的商品（30个）
# 推荐集：剩下的所有商品


def get_data():
    goods_info = {}
    base_set = {}
    other_set = {}
    goods_info_filename = 'Fw_data.txt'
    with open(goods_info_filename, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            info_list = line.split('\t')
            index = info_list.pop(0)
            # 剩下的就是信息列表
            goods_info.setdefault(index, [])
            goods_info[index] = info_list

    i = 0
    for index, info_list in goods_info.items():
        if i < 30:
            base_set.setdefault(index, [])
            base_set[index] = info_list
        else:
            other_set.setdefault(index, [])
            other_set[index] = info_list
        i += 1

    return base_set, other_set


# 2.拿到标准集30个商品的共同重要程度top10的词A
def get_base_words():
    base_set, other_set = get_data()
    string = ''

    for index, info_list in base_set.items():
        name = info_list[0]
        # 拿到了所有有用信息组成的字符串
        string = string + name
        # 通过TF-IDF来表征重要程度，倒排取top10的词
    base_words = jieba.analyse.extract_tags(string, topK=10)
    return base_words


# 3.拿到推荐集的每个商品的top5重要程度的词B
def get_other_each_book_words():
    base_set, other_words = get_data()
    data_string = {}
    for index, info_list in other_words.items():
        name = info_list[0]
        # 拿到了每个有用信息组成的字符串
        data_string.setdefault(index, [])
        data_string[index] = str(data_string[index]) + name
        other_words[index] = jieba.analyse.extract_tags(data_string[index], topK=10)
    return other_words


# 4.对每一个商品计算（A∩B）/（A∪B）
# 5.倒排取top10进行推荐

def good_similar_data():
    similar_data = {}
    a = get_other_each_book_words()
    b = get_base_words()
    for index, info_list in a.items():
        similar_data.setdefault(index, len(set(b) & set(info_list)) / len(set(b) | set(info_list)))

    sort_similar_data = sorted(similar_data.items(), key=itemgetter(1), reverse=True)[:10]
    sort_similar_goods = []
    for i in sort_similar_data:
        sort_similar_goods.append(i[0])
    return sort_similar_goods

