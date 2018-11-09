#!/your/real/python/path/python
# -*— coding: utf-8 -*-
# Time    : 2018/10/23 下午11:45
# Author  : tangdaye
# Desc    : 统一评分模型USM

import json

# todo 参数化
"""
Desc:   第一种题型评分规则
Input:  第一题的特征列表
Output: 百分制得分
"""


def score1(features):
    tone_quality = 100
    temp = 300 * (1 - features['clr_ratio'])
    if temp > 18:
        temp = 18
    tone_quality -= temp
    temp = 300 * (1 - features['cpl_ratio'])
    if temp > 18:
        temp = 18
    tone_quality -= temp
    if features['last_time'] > 35:
        temp = (features['last_time'] - 35) * 3
        if temp > 18:
            temp = 18
        tone_quality -= temp
    if features['last_time'] < 30:
        temp = (30 - features['last_time']) * 3
        if temp > 18:
            temp = 18
        tone_quality -= temp
    temp = 0.2 * (95 - features['phone_score'])
    if temp >= 0:
        if temp >= 6:
            temp = 6
        tone_quality -= temp
    temp = 0.2 * (85 - features['fluency_score'])
    if temp >= 0:
        if temp >= 6:
            temp = 6
        tone_quality -= temp
    temp = 0.2 * (90 - features['tone_score'])
    if temp >= 0:
        if temp >= 6:
            temp = 6
        tone_quality -= temp
    temp = 0.2 * (99 - features['integrity_score'])
    if temp >= 0:
        if temp >= 6:
            temp = 6
        tone_quality -= temp
    temp = 300 * features['ftl_ratio']
    if temp > 0:
        if temp > 18:
            temp = 18
        tone_quality -= temp
    if features['interval_num'] == 1:
        tone_quality -= 5
    if features['interval_num'] >= 2:
        tone_quality -= 10
    tone_quality *= features['clr_ratio']
    tone_quality *= features['cpl_ratio']
    if tone_quality < 0:
        tone_quality = 0
    return {"quality": tone_quality}


def score2(features):
    main_idea, detail = 0, 0
    mainidea_time_list = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 10000)]
    mainidea_wordcount_list = [(0, 10), (10, 30), (30, 40), (40, 50), (50, 100), (100, 120), (120, 10000)]
    mainidea_score_list = [[0, 0, 0, 0, 0, 0, 0],
                           [0, 40, 60, 100, 100, 100, 100],
                           [0, 100, 100, 100, 100, 100, 100],
                           [0, 100, 100, 100, 100, 100, 100],
                           [0, 100, 100, 100, 100, 100, 100],
                           [0, 100, 100, 100, 100, 100, 100]]
    detail_time_list = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 30), (30, 10000)]
    detail_wordcount_list = [(0, 10), (10, 30), (30, 50), (50, 80), (80, 100), (100, 120), (120, 10000)]
    detail_score_list = [[0, 0, 0, 0, 0, 0, 0],
                         [0, 30, 30, 30, 30, 30, 30],
                         [0, 30, 60, 60, 60, 60, 60],
                         [0, 30, 60, 80, 80, 80, 80],
                         [0, 30, 60, 80, 100, 100, 100],
                         [0, 30, 80, 100, 100, 100, 100]]
    # 基础分
    last_time = features['last_time']
    words_count = features['num']
    for i in range(len(mainidea_time_list)):
        for j in range(len(mainidea_wordcount_list)):
            if mainidea_time_list[i][0] <= last_time < mainidea_time_list[i][1]:
                if mainidea_wordcount_list[j][0] <= words_count < mainidea_wordcount_list[j][1]:
                    main_idea = mainidea_score_list[i][j]
    for i in range(len(detail_time_list)):
        for j in range(len(detail_wordcount_list)):
            if detail_time_list[i][0] <= last_time < detail_time_list[i][1]:
                if detail_wordcount_list[j][0] <= words_count < detail_wordcount_list[j][1]:
                    detail = detail_score_list[i][j]
    keywords_num = features['keywords_num']
    mainwords_num = features['mainwords_num']
    details_num = features['detailwords_nums']
    # 按照比例乘
    main_idea *= (keywords_num[0] / keywords_num[1])
    # 每少1个主干关键词扣6分
    main_idea -= (mainwords_num[1] - mainwords_num[0]) * 6
    # 按照比例乘
    single_detail = detail / len(details_num)
    for temp in details_num:
        detail -= single_detail * (1 - temp[0] / temp[1])
    # 其他可用属性：前n秒关键词['keywords_num_main']
    if main_idea <= 0:
        main_idea = 0
    if detail <= 0:
        detail = 0
    return {"main": main_idea, "detail": detail}


def score3(features):
    # 结构
    # 结构判断所⽤用五个词库分别是: 总分，分点，举例，亮观点，总结
    # 评分标准: 按是否击中每类词库算，不不管击中⼏几个词，击中就算⼀一次。⽐比如说回答击中了了总分⼦子
    # 击中⼤于3类词库对应分数80
    # 击中2类词库对应分数70
    # 击中0-1类词库对应分数55
    # 按照字数加分和减分
    structure, logic = 0, 0
    [a1, a2, a3, a4, a5] = [features['sum-aspects_num'] > 0, features['aspects_num'] > 0,
                            features['example_num'] > 0, features['opinion_num'] > 0,
                            features['sum_num'] > 0]
    if a1 + a2 + a3 + a4 + a5 >= 3:
        structure = 80
    elif a1 + a2 + a3 + a4 + a5 == 2:
        structure = 70
    else:
        structure = 55
    if features['num'] > 280:
        structure *= 1.2
    if 45 <= features['num'] < 120:
        structure *= 0.5
    if 10 <= features['num'] < 45:
        structure *= 0.25
    if 5 <= features['num'] < 10:
        structure *= 0.1
    if features['num'] < 5:
        structure = 0

    # 逻辑评分
    # 逻辑判断所⽤用四个词库分别是:因果，转折，并列，递进
    # 击中大于3类词库对应分数80
    # 击中2类词库对应分数75
    # 击中0-1类词库对应分数60
    # 按照字数加分和减分
    [a1, a2, a3, a4] = [features['cause-affect_num'] > 0, features['transition_num'] > 0,
                        features['progressive_num'] > 0, features['parallel_num'] > 0]
    if a1 + a2 + a3 + a4 >= 3:
        logic = 80
    elif a1 + a2 + a3 + a4 == 2:
        logic = 75
    else:
        logic = 60
    if features['num'] > 280:
        logic *= 1.2
    if 45 <= features['num'] < 120:
        logic *= 0.5
    if 10 <= features['num'] < 45:
        logic *= 0.25
    if 5 <= features['num'] < 10:
        logic *= 0.05
    if features['num'] < 5:
        logic = 0

    return {"structure": structure, "logic": logic}


if __name__ == '__main__':
    # audio_base = 'Samples2_audio/'
    # text_base = 'Samples2_text/'
    # features_base = 'features/1/'
    # for i in range(1, 117):
    #     with open(features_base + str(i) + '.json', 'r') as f:
    #         feature = json.loads(f.read())
    #         print('%d: %s'%(i,score1(feature).__str__()))

    # features_base = 'features/4/'
    # for i in range(1, 117):
    #     with open(features_base + str(i) + '.json', 'r') as f:
    #         feature = json.loads(f.read())
    #         print('%d: %s'%(i,score3(feature).__str__()))

    features_base = 'features/2/'
    score_base = 'scores/2'
    objs = []
    for i in range(1, 117):
        with open(features_base + str(i) + '.json', 'r') as f:
            feature = json.loads(f.read())
            x = score2(feature)
            x['id'] = i
            objs.append(x)
            print(x['main'],x['detail'])
    with open(score_base + '/2.json', 'w') as f:
        f.write(json.dumps(objs))
