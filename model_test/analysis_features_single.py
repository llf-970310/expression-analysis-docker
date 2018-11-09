#!/your/real/python/path/python
# -*— coding: utf-8 -*-
# Time    : 2018/10/23 下午11:43
# Author  : tangdaye
# Desc    : 用于对已有识别的样本进行测试

# # do NOT use xf_recognise.rcg directly
# # do NOT use xf_evaluate.evl directly

import io
import feature_text
import feature_audio
import wave
import utils
import config
import numpy
import json

"""
Desc:   第一种题型特征提取
Input:  源wav文件地址，标准文本
Output: feature列表
"""


def analysis1(wave_file, std_text, rcg_file, evl_file):
    result = {
        'num': 0,  # 字数
        'last_time': 0,  # 长度
        'interval_num': 0,  # 超过0.7秒时间间隔数量
        'interval_ratio': 0,  # 超过0.7秒时间间隔占比
        'clr_ratio': 0,  # 清晰度
        'ftl_ratio': 0,  # 无效表达比率
        'cpl_ratio': 0,  # 完成度
        'phone_score': 0,  # 声韵分
        'fluency_score': 0,  # 流畅度分
        'tone_score': 0,  # 调型分
        'integrity_score': 0,  # 完整度分
        'speed': 0,  # 平均语速
        'speed_deviation': 0,  # 语速标准差
        'volume1': 0,  # 音量1
        'volume2': 0,  # 音量2
        'volume3': 0  # 音量3
    }
    wave_file_processed = io.BytesIO()
    # 间隔
    interval_list = utils.find_and_remove_intervals(wave_file, wave_file_processed)

    # temp_std_text_file = io.StringIO()
    # temp_std_text_file.write(std_text)
    # rcg_result_file = io.StringIO()
    # evl_result_file = io.StringIO()
    #
    # xf_recognise.rcg_and_save(wave_file_processed, rcg_result_file, timeout=timeout)
    with open(rcg_file, 'r') as f:
        rcg_text = json.loads(f.read())['data']

    with open(evl_file, 'r') as f:
        eva_result = f.read()
    # xf_evaluate.evl_and_save(wave_file_processed, temp_std_text_file, evl_result_file, framerate=8000, timeout=timeout)
    # eva_result = evl_result_file.getvalue()

    # 字数
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # last_time 时长 未擦除的文件
    with wave.open(wave_file) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    for (start, last) in interval_list:
        if last > config.INTERVAL_TIME_THRESHOLD1 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    # clr_ratio,ftl_ratio,cpl_ratio
    cfc = feature_audio.get_cfc(rcg_text, std_text)
    result['clr_ratio'], result['ftl_ratio'], result['cpl_ratio'] = cfc['clr_ratio'], cfc['ftl_ratio'], cfc[
        'cpl_ratio']
    # phone_score,fluency_score,tone_score,integrity_score
    chapter_scores, simp_result = feature_audio.simplify_result(eva_result, category=config.XF_EVL_CATEGORY)
    result['phone_score'], result['fluency_score'], result['tone_score'], result['integrity_score'] = \
        float(chapter_scores['phone_score']), float(chapter_scores['fluency_score']), float(
            chapter_scores['tone_score']), float(chapter_scores['integrity_score'])
    # speeds
    speeds = numpy.array([wc / time for (wc, time) in utils.get_sentence_durations(simp_result)])
    result['speed'] = numpy.mean(speeds)
    result['speed_deviation'] = numpy.std(speeds)
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]
    return result


def analysis2(wave_file, wordbase, rcg_file):
    result = {
        'num': 0,
        'last_time': 0,
        'interval_num': 0,
        'interval_ratio': 0,
        'n_ratio': 0,
        'v_ratio': 0,
        'vd_ratio': 0,
        'vn_ratio': 0,
        'a_ratio': 0,
        'ad_ratio': 0,
        'an_ratio': 0,
        'd_ratio': 0,
        'm_ratio': 0,
        'q_ratio': 0,
        'r_ratio': 0,
        'p_ratio': 0,
        'c_ratio': 0,
        'u_ratio': 0,
        'xc_ratio': 0,
        'w_ratio': 0,
        'ne_ratio': 0,
        'word_num': 0,
        'noun_frequency_2': 0,
        'noun_frequency_3': 0,
        'noun_frequency_4': 0,
        'keywords_num': [0, 1],
        'mainwords_num': [0, 1],
        'detailwords_nums': [],
        'keywords_num_main': [0, 1],
        'speed1': 0,
        'speed2': 0,
        'speed3': 0,
        'volume1': 0,
        'volume2': 0,
        'volume3': 0
    }
    # last_time 时长 未擦除的文件
    with wave.open(wave_file) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    # interval 未擦除的文件
    wave_file_processed = io.BytesIO()
    interval_list = utils.find_and_remove_intervals(wave_file, wave_file_processed)
    for (start, last) in interval_list:
        if last > config.INTERVAL_TIME_THRESHOLD2 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    # 识别用擦除过的文件
    # rcg_result_file = io.StringIO()
    # xf_recognise.rcg_and_save(wave_file_processed, rcg_result_file, timeout=timeout)
    # temp = rcg_result_file.getvalue()
    # if temp and len(temp) == 3:
    #     rcg_text1, rcg_text2, rcg_text3 = temp[0], temp[1], temp[2]
    # else:
    #     rcg_text1, rcg_text2, rcg_text3 = '', '', ''
    # rcg_text = rcg_text1 + rcg_text2 + rcg_text3

    with open(rcg_file, 'r') as f:
        [rcg_text1, rcg_text2, rcg_text3] = json.loads(f.read())['data']
    rcg_text = rcg_text1 + rcg_text2 + rcg_text3
    # 字数
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # 词性比例
    proportions = feature_text.proportion(rcg_text)
    all_words_num = proportions['all']
    if all_words_num == 0:
        all_words_num = 1
    result['n_ratio'] = proportions['n'] / all_words_num
    result['v_ratio'] = proportions['v'] / all_words_num
    result['vd_ratio'] = proportions['vd'] / all_words_num
    result['vn_ratio'] = proportions['vn'] / all_words_num
    result['a_ratio'] = proportions['a'] / all_words_num
    result['ad_ratio'] = proportions['ad'] / all_words_num
    result['an_ratio'] = proportions['an'] / all_words_num
    result['d_ratio'] = proportions['d'] / all_words_num
    result['m_ratio'] = proportions['m'] / all_words_num
    result['q_ratio'] = proportions['q'] / all_words_num
    result['r_ratio'] = proportions['r'] / all_words_num
    result['p_ratio'] = proportions['p'] / all_words_num
    result['c_ratio'] = proportions['c'] / all_words_num
    result['u_ratio'] = proportions['u'] / all_words_num
    result['xc_ratio'] = proportions['xc'] / all_words_num
    result['w_ratio'] = proportions['w'] / all_words_num
    result['ne_ratio'] = proportions['ne'] / all_words_num
    result['word_num'] = all_words_num
    # noun frequency 名词 人名 地名 机构名 作品名 其他专名 专名识别缩略词
    nouns = proportions['nouns']
    result['noun_frequency_2'], result['noun_frequency_3'], result['noun_frequency_4'] = feature_text.words_frequency(
        nouns)
    # sentence_num
    result['sentence_num'] = len(feature_text.divide_text_to_sentence(rcg_text))
    # 词库击中，谐音
    # [
    #     ['美好', '幸福', '快乐', '灿烂', '美丽', '珍惜', '愉快', '渴望', '光辉', '盼望'],
    #     ['城市', '郊区', '大都市', '卫星城', '小城镇', '周边地区'],
    #     ['生活', '贫困', '家庭', '与世隔绝', '穷困', '境遇', '孤独']
    # ],
    # [
    #     [
    #         ['转型', '迈进', '年轻化', '转变', '持续发展', '迈向', '蜕变', '导向', '主导', '承接'],
    #         ['2011'],
    #         ['50']
    #     ]
    # ]
    keywords, mainwords, detailwords = wordbase.get('keywords'), wordbase.get('mainwords'), wordbase.get('detailwords')
    for word in keywords:
        if feature_text.words_pronunciation(text=rcg_text, answers=word) >= 1:
            result['keywords_num'][0] += 1
        if feature_text.words_pronunciation(text=rcg_text[:config.MAIN_IDEA_WORD_COUNT], answers=word) >= 1:
            result['keywords_num_main'][0] += 1
    result['keywords_num'][1] = len(keywords)
    result['keywords_num_main'][1] = len(keywords)
    for word in mainwords:
        if feature_text.words_pronunciation(text=rcg_text, answers=word) >= 1:
            result['mainwords_num'][0] += 1
    result['mainwords_num'][1] = len(mainwords)
    for temp_l in detailwords:
        x = 0
        for word in temp_l:
            if feature_text.words_pronunciation(text=rcg_text, answers=word) >= 1:
                x += 1
        result['detailwords_nums'].append([x, len(temp_l)])
    # speed
    if not result['last_time'] == 0:
        result['speed1'] = 3 * feature_text.len_without_punctuation(rcg_text1) / result['last_time']
        result['speed2'] = 3 * feature_text.len_without_punctuation(rcg_text2) / result['last_time']
        result['speed3'] = 3 * feature_text.len_without_punctuation(rcg_text3) / result['last_time']
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]
    return result


def analysis3(wave_file, wordbase, rcg_file):
    result = {
        'num': 0,
        'last_time': 0,
        'interval_num': 0,
        'interval_ratio': 0,
        'n_ratio': 0,
        'v_ratio': 0,
        'vd_ratio': 0,
        'vn_ratio': 0,
        'a_ratio': 0,
        'ad_ratio': 0,
        'an_ratio': 0,
        'd_ratio': 0,
        'm_ratio': 0,
        'q_ratio': 0,
        'r_ratio': 0,
        'p_ratio': 0,
        'c_ratio': 0,
        'u_ratio': 0,
        'xc_ratio': 0,
        'w_ratio': 0,
        'ne_ratio': 0,
        'word_num': 0,
        'noun_frequency_2': 0,
        'noun_frequency_3': 0,
        'noun_frequency_4': 0,
        'sentence_num': 0,
        'sum-aspects_num': 0,
        'aspects_num': 0,
        'example_num': 0,
        'opinion_num': 0,
        'sum_num': 0,
        'cause-affect_num': 0,
        'transition_num': 0,
        'progressive_num': 0,
        'parallel_num': 0,
        'speed1': 0,
        'speed2': 0,
        'speed3': 0,
        'volume1': 0,
        'volume2': 0,
        'volume3': 0
    }
    # last_time 时长 未擦除的文件
    with wave.open(wave_file) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    # interval 未擦除的文件
    wave_file_processed = io.BytesIO()
    interval_list = utils.find_and_remove_intervals(wave_file, wave_file_processed)
    for (start, last) in interval_list:
        if last > config.INTERVAL_TIME_THRESHOLD3 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    # 识别用擦除过的文件
    # rcg_result_file = io.StringIO()
    # xf_recognise.rcg_and_save(wave_file_processed, rcg_result_file, segments=3, timeout=timeout)
    # temp = rcg_result_file.getvalue()
    # if temp and len(temp) == 3:
    #     rcg_text1, rcg_text2, rcg_text3 = temp[0], temp[1], temp[2]
    # else:
    #     rcg_text1, rcg_text2, rcg_text3 = '', '', ''
    with open(rcg_file, 'r') as f:
        [rcg_text1, rcg_text2, rcg_text3] = json.loads(f.read())['data']
    rcg_text = rcg_text1 + rcg_text2 + rcg_text3
    # 字数
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # 词性比例
    proportions = feature_text.proportion(rcg_text)
    all_words_num = proportions['all']
    if all_words_num == 0:
        all_words_num = 1
    result['n_ratio'] = proportions['n'] / all_words_num
    result['v_ratio'] = proportions['v'] / all_words_num
    result['vd_ratio'] = proportions['vd'] / all_words_num
    result['vn_ratio'] = proportions['vn'] / all_words_num
    result['a_ratio'] = proportions['a'] / all_words_num
    result['ad_ratio'] = proportions['ad'] / all_words_num
    result['an_ratio'] = proportions['an'] / all_words_num
    result['d_ratio'] = proportions['d'] / all_words_num
    result['m_ratio'] = proportions['m'] / all_words_num
    result['q_ratio'] = proportions['q'] / all_words_num
    result['r_ratio'] = proportions['r'] / all_words_num
    result['p_ratio'] = proportions['p'] / all_words_num
    result['c_ratio'] = proportions['c'] / all_words_num
    result['u_ratio'] = proportions['u'] / all_words_num
    result['xc_ratio'] = proportions['xc'] / all_words_num
    result['w_ratio'] = proportions['w'] / all_words_num
    result['ne_ratio'] = proportions['ne'] / all_words_num
    result['word_num'] = all_words_num
    # noun frequency 名词 人名 地名 机构名 作品名 其他专名 专名识别缩略词
    nouns = proportions['nouns']
    result['noun_frequency_2'], result['noun_frequency_3'], result['noun_frequency_4'] = feature_text.words_frequency(
        nouns)
    # sentence_num
    result['sentence_num'] = len(feature_text.divide_text_to_sentence(rcg_text))
    # 词库击中 谐音
    result['sum-aspects_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('sum-aspects'))
    result['aspects_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('aspects'))
    result['example_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('example'))
    result['opinion_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('opinion'))
    result['sum_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('sum'))
    result['cause-affect_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('cause-affect'))
    result['transition_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('transition'))
    result['progressive_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('progressive'))
    result['parallel_num'] = feature_text.words_pronunciation(rcg_text, wordbase.get('parallel'))
    # speed
    if not result['last_time'] == 0:
        result['speed1'] = 3 * feature_text.len_without_punctuation(rcg_text1) / result['last_time']
        result['speed2'] = 3 * feature_text.len_without_punctuation(rcg_text2) / result['last_time']
        result['speed3'] = 3 * feature_text.len_without_punctuation(rcg_text3) / result['last_time']
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]

    return result


if __name__ == '__main__':
    wordbase = {
        "keywords": [
            [
                "高铁",
                "高速铁路"
            ],
            [
                "方式",
                "方法",
                "形式",
                "手段"
            ],
            [
                "出行"
            ],
            [
                "性价比",
                "最受欢迎"
            ]
        ],
        "mainwords": [
            [
                "速度",
                "速率"
            ],
            [
                "舒适",
                "不适感"
            ],
            [
                "正点率",
                "准点",
                "误点"
            ],
            [
                "成本",
                "效率",
                "费用",
                "效益",
                "价格"
            ]
        ],
        "detailwords": [
            [
                [
                    "40",
                    "6",
                    "贵阳",
                    "昆明",
                    "桂林",
                    "成都",
                    "柳州",
                    "南宁",
                    "贵州",
                    "遵义",
                    "蒙自"
                ],
                [
                    "天气",
                    "天候",
                    "飞机",
                    "直升机",
                    "民航机",
                    "起飞",
                    "飞行中",
                    "航空器"
                ],
                [
                    "电源插座",
                    "餐车",
                    "无线网络",
                    "wifi"
                ]
            ],
            [
                [
                    "运营",
                    "营运",
                    "运行"
                ],
                [
                    "专业"
                ],
                [
                    "管理",
                    "监管",
                    "行政"
                ]
            ]
        ]
    }
    audio_base = '/home/tangdaye/git-project/exp-docker/model_test/Samples2_audio/'
    text_base = '/home/tangdaye/git-project/exp-docker/model_test/Samples2_text/'
    features_base = '/home/tangdaye/git-project/exp-docker/model_test/features/2/'
    for i in range(1, 117):
        audio_path = audio_base + str(i) + '/3.wav'
        rcg_path = text_base + 'rcg_' + str(i) + '_3.json'
        result = analysis2(wave_file=audio_path, wordbase=wordbase, rcg_file=rcg_path)
        with open(features_base + str(i) + '.json', 'w') as f:
            f.write(json.dumps(result, ensure_ascii=False))
    # wordbase = {
    #     "sum-aspects" : [
    #         "分为几点",
    #         "分情况",
    #         "看情况",
    #         "有几点"
    #     ],
    #     "aspects" : [
    #         "第一",
    #         "第1",
    #         "第二",
    #         "第2",
    #         "第三",
    #         "第3",
    #         "第四",
    #         "首先",
    #         "其次",
    #         "还有"
    #     ],
    #     "example" : [
    #         "举个例子",
    #         "比如",
    #         "例如",
    #         "比方说",
    #         "我的工作",
    #         "我的职业"
    #     ],
    #     "opinion" : [
    #         "我同意",
    #         "我不同意",
    #         "我觉得",
    #         "我认为",
    #         "我的观点",
    #         "应该",
    #         "不应该"
    #     ],
    #     "sum" : [
    #         "总之",
    #         "最后",
    #         "总的来说"
    #     ],
    #     "cause-affect" : [
    #         "因为",
    #         "所以",
    #         "因此"
    #     ],
    #     "transition" : [
    #         "虽然",
    #         "但",
    #         "但是"
    #     ],
    #     "if" : [
    #         "假如",
    #         "如果"
    #     ],
    #     "parallel" : [
    #         "而且",
    #         "也"
    #     ],
    #     "progressive" : [
    #         "不但"
    #     ]
    # }
    # audio_base = '/home/tangdaye/git-project/exp-docker/model_test/Samples2_audio/'
    # text_base = '/home/tangdaye/git-project/exp-docker/model_test/Samples2_text/'
    # features_base = '/home/tangdaye/git-project/exp-docker/model_test/features/4/'
    # for i in range(1, 117):
    #     audio_path = audio_base + str(i) + '/4.wav'
    #     rcg_path = text_base + 'rcg_' + str(i) + '_4.json'
    #     # eva_path = text_base + 'evl_' + str(i) + '_1.json'
    #     result = analysis3(wave_file=audio_path, wordbase=wordbase, rcg_file=rcg_path)
    #     with open(features_base + str(i) + '.json', 'w') as f:
    #         f.write(json.dumps(result, ensure_ascii=False))
    # text = '表达能力是一种非常有用的技能，但重要性往往被人忽视。具备优秀的表达能力，能够让你在工作、学习、生活和情感上，获得很大的优势，还能提升自信心，增加个人魅力，是一种跟世界建立连接的高效方式。能够清晰准确表达自己观点的人，更加容易脱颖而出，成为人群的焦点和领导者。在一个表达力没有得到普遍重视的环境里，先意识到这点的人，将会获得巨大优势。'
    # audio_base = 'Samples2_audio/'
    # text_base = 'Samples2_text/'
    # features_base = 'features/1/'
    # for i in range(1, 117):
    #     audio_path = audio_base + str(i) + '/1.wav'
    #     rcg_path = text_base + 'rcg_' + str(i) + '_1.json'
    #     eva_path = text_base + 'evl_' + str(i) + '_1.json'
    #     result = analysis1(wave_file=audio_path, std_text=text, rcg_file=rcg_path, evl_file=eva_path)
    #     with open(features_base + str(i) + '.json', 'w') as f:
    #         f.write(json.dumps(result, ensure_ascii=False))
