# -*— coding: utf-8 -*-
# Time    : 2018/8/24 下午10:39
# Author  : tangdaye
# Desc    : 评分机制（专家规则）
import json
import math

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


def total_score(each_score):
    [score1, score2, score3, score4] = each_score
    x = {
        "tone-quality": round(score1['tone-quality'], 6),
        "main-idea": round(score2['main-idea'] * 0.3 + score3['main-idea'] * 0.7, 6),
        "detail": round(score2['detail'] * 0.3 + score3['detail'] * 0.7, 6),
        "structure": round(score4['structure'], 6),
        "logistic": round(score4['logistic'], 6)
    }
    x['total-score'] = round(x["tone-quality"] * 0.3 + x["main-idea"] * 0.35 +
                             x["detail"] * 0.15 + x["structure"] * 0.1 + x["logistic"] * 0.1, 6)
    return x


class Score0902:
    def __init__(self, feature_list):
        self.feature_list = feature_list

    def score1(self):
        features = self.feature_list['feature1']
        # 音质
        score = {
            "tone-quality": 100,
            "main-idea": 0,
            "detail": 0,
            "structure": 0,
            "logistic": 0
        }
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
        # if features['num'] < 145 or 152 < features['num'] < 156:
        #     tone_quality -= 5
        # if features['num'] > 156:
        #     tone_quality -= 10
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
        score['tone-quality'] = tone_quality
        return score

    def score2(self):
        features = self.feature_list['feature2']
        score = {
            "tone-quality": 0,
            "main-idea": 0,
            "detail": 0,
            "structure": 0,
            "logistic": 0
        }
        last_time = features['last_time']
        words_count = features['num']
        for i in range(len(mainidea_time_list)):
            for j in range(len(mainidea_wordcount_list)):
                if mainidea_time_list[i][0] <= last_time < mainidea_time_list[i][1]:
                    if mainidea_wordcount_list[j][0] <= words_count < mainidea_wordcount_list[j][1]:
                        score["main-idea"] = mainidea_score_list[i][j]
        for i in range(len(detail_time_list)):
            for j in range(len(detail_wordcount_list)):
                if detail_time_list[i][0] <= last_time < detail_time_list[i][1]:
                    if detail_wordcount_list[j][0] <= words_count < detail_wordcount_list[j][1]:
                        score["detail"] = detail_score_list[i][j]

        score["main-idea"] -= (6 - features['classA_hit_count']) * 10
        [a1, a2, a3] = [features['detail_time_hit_count'] > 0, features['detail_store_hit_count'] > 0,
                        features['detail_welcome_hit_count'] > 0]
        score["detail"] -= (3 - (a1 + a2 + a3)) * 20

        if score["main-idea"] < 0:
            score["main-idea"] = 0
        if score["detail"] < 0:
            score["detail"] = 0
        return score

    def score3(self):
        features = self.feature_list['feature3']
        score = {
            "tone-quality": 0,
            "main-idea": 100,
            "detail": 100,
            "structure": 0,
            "logistic": 0
        }
        last_time = features['last_time']
        words_count = features['num']
        for i in range(len(mainidea_time_list)):
            for j in range(len(mainidea_wordcount_list)):
                if mainidea_time_list[i][0] <= last_time < mainidea_time_list[i][1]:
                    if mainidea_wordcount_list[j][0] <= words_count < mainidea_wordcount_list[j][1]:
                        score["main-idea"] = mainidea_score_list[i][j]
        for i in range(len(detail_time_list)):
            for j in range(len(detail_wordcount_list)):
                if detail_time_list[i][0] <= last_time < detail_time_list[i][1]:
                    if detail_wordcount_list[j][0] <= words_count < detail_wordcount_list[j][1]:
                        score["detail"] = detail_score_list[i][j]
        # 主旨
        # classA 击中6次不不扣分，每少击中⼀一次扣5分，⽐比如击中4次，(6-4)×5=扣10分
        # classB 击中8次不不扣分，每少击中⼀一次扣3分，⽐比如击中4词，(8-4)×3=扣12分
        # classA 前30个字击中次数/classA击中次数 ⼩小于0.75的扣8分，⼤大于等于0.75不不扣分
        if features['classA_hit_count'] < 6:
            score["main-idea"] -= (6 - features['classA_hit_count']) * 4
        if features['classB_hit_count'] < 8:
            score["main-idea"] -= (8 - features['classA_hit_count']) * 3
        if features['classA_hit_count_30'] == 0:
            score["main-idea"] -= 8
        elif features['classA_hit_count_30'] / features['classA_hit_count'] < 0.75:
            score["main-idea"] -= 8

        # 细节
        # 数度细节2个词不不扣分，少⼀一个扣10分
        # 准时细节3个词不不扣分。少⼀一个扣8分。
        # 舒适细节3个词不不扣分，少⼀一个扣8分。
        # 成本细节，6个词不不扣分，少⼀一个扣4分。
        # 字数⼤大于145字扣10分，过分拘泥泥于细节。
        # 字数少于100字扣5分，字数少于50字不额外扣分
        if features['detail_speed_hit_count'] == 0:
            score['detail'] -= 20
        if features['detail_on_time_hit_count'] == 0:
            score['detail'] -= 16
        if features['detail_comfortable_hit_count'] == 0:
            score['detail'] -= 16
        if features['detail_cost_hit_count'] == 0:
            score['detail'] -= 8

        if score["main-idea"] < 0:
            score["main-idea"] = 0
        if score["detail"] < 0:
            score["detail"] = 0
        return score

    def score4(self):
        features = self.feature_list['feature4']
        # 结构
        # 结构判断所⽤用五个词库分别是: 总分，分点，举例，亮观点，总结
        # 评分标准: 按是否击中每类词库算，不不管击中⼏几个词，击中就算⼀一次。⽐比如说回答击中了了总分⼦子
        # 击中⼤于3类词库对应分数80
        # 击中2类词库对应分数70
        # 击中0-1类词库对应分数55
        # 加分:长度超过65s *1.2
        # 减分:长度小于28s *0.5
        score = {
            "tone-quality": 0,
            "main-idea": 0,
            "detail": 0,
            "structure": 0,
            "logistic": 0
        }
        [a1, a2, a3, a4, a5] = [features['sum-aspects_num'] > 0, features['aspects_num'] > 0,
                                features['example_num'] > 0, features['opinion_num'] > 0,
                                features['sum_num'] > 0]
        if a1 + a2 + a3 + a4 + a5 >= 3:
            score['structure'] = 80
        elif a1 + a2 + a3 + a4 + a5 == 2:
            score['structure'] = 70
        else:
            score['structure'] = 55
        if features['num'] > 280:
            score['structure'] *= 1.2
        if 45 <= features['num'] < 120:
            score['structure'] *= 0.5
        if 10 <= features['num'] < 45:
            score['structure'] *= 0.25
        if 5 <= features['num'] < 10:
            score['structure'] *= 0.1
        if features['num'] < 5:
            score['structure'] = 0

        # 逻辑评分
        # 逻辑判断所⽤用四个词库分别是:因果，转折，并列，递进
        # 击中大于3类词库对应分数80
        # 击中2类词库对应分数75
        # 击中0-1类词库对应分数60
        # 加分:长度超过65s *1.2
        # 减分:⻓度⼩于28s *0.5
        [a1, a2, a3, a4] = [features['cause-affect_num'] > 0, features['transition_num'] > 0,
                            features['progressive_num'] > 0, features['parallel_num'] > 0]
        if a1 + a2 + a3 + a4 >= 3:
            score['logistic'] = 80
        elif a1 + a2 + a3 + a4 == 2:
            score['logistic'] = 75
        else:
            score['logistic'] = 60
        if features['num'] > 280:
            score['logistic'] *= 1.2
        if 45 <= features['num'] < 120:
            score['logistic'] *= 0.5
        if 10 <= features['num'] < 45:
            score['logistic'] *= 0.25
        if 5 <= features['num'] < 10:
            score['logistic'] *= 0.05
        if features['num'] < 5:
            score['logistic'] = 0
        return score

    def each_score(self):
        list = self.feature_list
        if list['feature1'] is None:
            x1 = {
                "tone-quality": 70,
                "main-idea": 0,
                "detail": 0,
                "structure": 0,
                "logistic": 0
            }
        else:
            x1 = self.score1()
        if list['feature2'] is None:
            x2 = {
                "tone-quality": 0,
                "main-idea": 70,
                "detail": 70,
                "structure": 0,
                "logistic": 0
            }
        else:
            x2 = self.score2()
        if list['feature3'] is None:
            x3 = {
                "tone-quality": 0,
                "main-idea": 70,
                "detail": 70,
                "structure": 0,
                "logistic": 0
            }
        else:
            x3 = self.score3()
        if list['feature4'] is None:
            x4 = {
                "tone-quality": 0,
                "main-idea": 0,
                "detail": 0,
                "structure": 70,
                "logistic": 70
            }
        else:
            x4 = self.score4()
        return [x1, x2, x3, x4]


if __name__ == '__main__':
    result0902_1 = []
    result0902_2 = []
    result0902_3 = []
    result0902_4 = []
    result0902_total = []
    for i in range(1, 117):
        with open('./result/sample/result_%d.json' % i, 'r') as f:
            x = json.loads(f.read())
        score0902 = Score0902(x)
        each = score0902.each_score()
        result0902_1.append(each[0])
        result0902_2.append(each[1])
        result0902_3.append(each[2])
        result0902_4.append(each[3])
        result0902_total.append(
            total_score(each)
        )
    with open('score/sample/score1.json', 'w') as f:
        f.write(json.dumps(result0902_1))
    with open('score/sample/score2.json', 'w') as f:
        f.write(json.dumps(result0902_2))
    with open('score/sample/score3.json', 'w') as f:
        f.write(json.dumps(result0902_3))
    with open('score/sample/score4.json', 'w') as f:
        f.write(json.dumps(result0902_4))
    with open('score/sample/score_total.json', 'w') as f:
        f.write(json.dumps(result0902_total))
    result0902_pro_1 = []
    result0902_pro_2 = []
    result0902_pro_3 = []
    result0902_pro_4 = []
    result0902_pro_total = []
    for i in range(1, 9):
        with open('./result/pro/result_%d.json' % i, 'r') as f:
            x = json.loads(f.read())
        score0902 = Score0902(x)
        each = score0902.each_score()
        result0902_pro_1.append(each[0])
        result0902_pro_2.append(each[1])
        result0902_pro_3.append(each[2])
        result0902_pro_4.append(each[3])
        result0902_pro_total.append(
            total_score(each)
        )
    with open('score/pro/score1.json', 'w') as f:
        f.write(json.dumps(result0902_pro_1))
    with open('score/pro/score2.json', 'w') as f:
        f.write(json.dumps(result0902_pro_2))
    with open('score/pro/score3.json', 'w') as f:
        f.write(json.dumps(result0902_pro_3))
    with open('score/pro/score4.json', 'w') as f:
        f.write(json.dumps(result0902_pro_4))
    with open('score/pro/score_total.json', 'w') as f:
        f.write(json.dumps(result0902_pro_total))
