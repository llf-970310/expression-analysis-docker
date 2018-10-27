# -*— coding: utf-8 -*-
# Time    : 2018/8/20 下午10:58
# Author  : tangdaye
# Desc    : 分析
import json
import wave
import feature_text
import feature_audio
import config
import numpy

"""
Desc:   对问题1的特征提取
Input:  源文件(未擦除)，源文件（擦除），评测文件，识别文件
Output: result
"""


def analysis1(wave_file_origin, wave_file_processed, eval_file, rcg_file, interval_list):
    std_text = '表达能力是一种非常有用的技能，但重要性往往被人忽视。具备优秀的表达能力，能够让你在工作、学习、生活和情感上，获得很大的优势，还能提升自信心，增加个人魅力，' \
               '是一种跟世界建立连接的高效方式。能够清晰准确表达自己观点的人，更加容易脱颖而出，成为人群的焦点和领导者。在一个表达力没有得到普遍重视的环境里，先意识到这点的人，将会获得巨大优势。'
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
    # num 没有标点的识别文字
    rcg_text = get_content(rcg_file)['data']
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # last_time 时长 未擦除的文件
    with wave.open(wave_file_origin) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    # interval 未擦除的文件
    # interval_list = utils.find_and_remove_intervals(wave_file_origin, wave_file_processed)
    for (start, last) in interval_list:
        if last > 0.7 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    # clr_ratio,ftl_ratio,cpl_ratio
    cfc = feature_audio.get_cfc(rcg_text, std_text)
    result['clr_ratio'], result['ftl_ratio'], result['cpl_ratio'] = cfc['clr_ratio'], cfc['ftl_ratio'], cfc['cpl_ratio']
    # phone_score to speed_deviation
    chapter_scores, simp_result = feature_audio.simplify_result(get_content(eval_file),
                                                                category=config.XF_EVL_CATEGORY)
    result['phone_score'], result['fluency_score'], result['tone_score'], result['integrity_score'] = \
        float(chapter_scores['phone_score']), float(chapter_scores['fluency_score']), float(
            chapter_scores['tone_score']), float(chapter_scores['integrity_score'])
    speeds = numpy.array([wc / time for (wc, time) in get_sentence_durations(simp_result)])
    result['speed'] = numpy.mean(speeds)
    result['speed_deviation'] = numpy.std(speeds)
    # volume1 to volume3 使用擦除后的wav文件
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]
    return result


"""
Desc:   对问题2的特征提取
Input:  源文件(未擦除)，源文件（擦除），识别文件
Output: result
"""


def analysis2(wave_file_origin, wave_file_processed, rcg_file, interval_list):
    main_idea_std_text = '肯德基和麦当劳是两大餐厅巨头。很多中国人觉得肯德基比麦当劳大，但事实上，麦当劳才是世界上最大的快餐企业。'
    result = {
        'num': 0,
        'last_time': 0,
        'interval_num': 0,
        'interval_ratio': 0,
        'main_idea_similarity': 0,
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
        'classA_ratio': 0,
        'classA_hit_count': 0,
        'classA_ratio_30': 0,
        'classA_hit_count_30': 0,
        'deduct_count': 0,
        'detail_time_hit_count': 0,
        'detail_store_hit_count': 0,
        'detail_welcome_hit_count': 0,
        'speed1': 0,
        'speed2': 0,
        'speed3': 0,
        'volume1': 0,
        'volume2': 0,
        'volume3': 0
    }
    # num 没有标点的识别文字
    eva = get_content(rcg_file).get('data')
    if eva and len(eva) == 3:
        rcg_text1, rcg_text2, rcg_text3 = eva[0], eva[1], eva[2]
    else:
        rcg_text1, rcg_text2, rcg_text3 = '', '', ''
    rcg_text = rcg_text1 + rcg_text2 + rcg_text3
    # rcg_text = get_content(rcg_file)['data']
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # last_time 时长 未擦除的文件
    with wave.open(wave_file_origin) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
        # interval 未擦除的文件
    # interval_list = utils.find_and_remove_intervals(wave_file_origin, wave_file_processed)
    for (start, last) in interval_list:
        if last > 2 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    result['main_idea_similarity'] = feature_text.similarity(rcg_text[:50], main_idea_std_text)
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
    # wordbase
    word_base = get_content('./text_files/Papers/wordbase.json')
    classA_words = word_base['part2']['classA']
    detail_time_words = word_base['part2']['detail_time']
    detail_store_words = word_base['part2']['detail_store']
    detail_welcome_words = word_base['part2']['detail_welcome']
    deduct_words = word_base['part2']['deduct']
    result['classA_ratio'] = feature_text.words(rcg_text, sum_list(classA_words)) / all_words_num
    result['classA_hit_count'] = feature_text.words_hit(rcg_text, classA_words)
    result['classA_ratio_30'] = feature_text.words(rcg_text[:30], sum_list(classA_words)) / all_words_num
    result['classA_hit_count_30'] = feature_text.words_hit(rcg_text[:30], classA_words)
    result['detail_time_hit_count'] = feature_text.words_hit(rcg_text, detail_time_words)
    result['detail_store_hit_count'] = feature_text.words_hit(rcg_text, detail_store_words)
    result['detail_welcome_hit_count'] = feature_text.words_hit(rcg_text, detail_welcome_words)
    result['deduct_count'] = feature_text.words(rcg_text, sum_list(deduct_words))
    # speed
    if not result['last_time'] == 0:
        result['speed1'] = 3 * feature_text.len_without_punctuation(rcg_text1) / result['last_time']
        result['speed2'] = 3 * feature_text.len_without_punctuation(rcg_text2) / result['last_time']
        result['speed3'] = 3 * feature_text.len_without_punctuation(rcg_text3) / result['last_time']
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]
    return result


"""
Desc:   对问题3的特征提取
Input:  源文件(未擦除)，源文件（擦除），识别文件
Output: result
"""


def analysis3(wave_file_origin, wave_file_processed, rcg_file, interval_list):
    main_idea_std_text = '高铁是现在最受欢迎的出行方式，主要有三个优点，速度快、整点率高、环境舒适。但高铁的缺点是前期投入大，运营成本高。'
    result = {
        'num': 0,
        'last_time': 0,
        'interval_num': 0,
        'interval_ratio': 0,
        'main_idea_similarity': 0,
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
        'classA_ratio': 0,
        'classB_ratio': 0,
        'classA_hit_count': 0,
        'classB_hit_count': 0,
        'classA_ratio_30': 0,
        'classB_ratio_30': 0,
        'classA_hit_count_30': 0,
        'classB_hit_count_30': 0,
        'deduct_count': 0,
        'detail_speed_hit_count': 0,
        'detail_on_time_hit_count': 0,
        'detail_comfortable_hit_count': 0,
        'detail_cost_hit_count': 0,
        'speed1': 0,
        'speed2': 0,
        'speed3': 0,
        'volume1': 0,
        'volume2': 0,
        'volume3': 0
    }
    # num 没有标点的识别文字
    eva = get_content(rcg_file).get('data')
    if eva and len(eva) == 3:
        rcg_text1, rcg_text2, rcg_text3 = eva[0], eva[1], eva[2]
    else:
        rcg_text1, rcg_text2, rcg_text3 = '', '', ''
    rcg_text = rcg_text1 + rcg_text2 + rcg_text3
    # rcg_text = get_content(rcg_file)['data']
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # last_time 时长 未擦除的文件
    with wave.open(wave_file_origin) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    # interval 未擦除的文件
    # interval_list = utils.find_and_remove_intervals(wave_file_origin, wave_file_processed)
    for (start, last) in interval_list:
        if last > 2 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
    proportions = feature_text.proportion(rcg_text)
    result['main_idea_similarity'] = feature_text.similarity(rcg_text[:50], main_idea_std_text)
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
    # wordbase
    word_base = get_content('./text_files/Papers/wordbase.json')
    classA_words = word_base['part3']['classA']
    classB_words = word_base['part3']['classB']
    detail_speed_words = word_base['part3']['detail_speed']
    detail_on_time_words = word_base['part3']['detail_on_time']
    detail_comfortable_words = word_base['part3']['detail_comfortable']
    detail_cost_words = word_base['part3']['detail_cost']
    deduct_words = word_base['part3']['deduct']
    result['classA_ratio'] = feature_text.words(rcg_text, sum_list(classA_words)) / all_words_num
    result['classB_ratio'] = feature_text.words(rcg_text, sum_list(classB_words)) / all_words_num
    result['classA_hit_count'] = feature_text.words_hit(rcg_text, classA_words)
    result['classB_hit_count'] = feature_text.words_hit(rcg_text, classB_words)
    result['classA_ratio_30'] = feature_text.words(rcg_text[:30], sum_list(classA_words)) / all_words_num
    result['classB_ratio_30'] = feature_text.words(rcg_text[:30], sum_list(classB_words)) / all_words_num
    result['classA_hit_count_30'] = feature_text.words_hit(rcg_text[:30], classA_words)
    result['classB_hit_count_30'] = feature_text.words_hit(rcg_text[:30], classB_words)
    result['detail_speed_hit_count'] = feature_text.words_hit(rcg_text, detail_speed_words)
    result['detail_on_time_hit_count'] = feature_text.words_hit(rcg_text, detail_on_time_words)
    result['detail_comfortable_hit_count'] = feature_text.words_hit(rcg_text, detail_comfortable_words)
    result['detail_cost_hit_count'] = feature_text.words_hit(rcg_text, detail_cost_words)
    result['deduct_count'] = feature_text.words(rcg_text, sum_list(deduct_words))
    # speed
    if not result['last_time'] == 0:
        result['speed1'] = 3 * feature_text.len_without_punctuation(rcg_text1) / result['last_time']
        result['speed2'] = 3 * feature_text.len_without_punctuation(rcg_text2) / result['last_time']
        result['speed3'] = 3 * feature_text.len_without_punctuation(rcg_text3) / result['last_time']
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]

    return result


"""
Desc:   对问题4的特征提取
Input:  源文件(未擦除)，源文件（擦除），识别文件
Output: result
"""


def analysis4(wave_file_origin, wave_file_processed, rcg_file, interval_list):
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
    # num 没有标点的识别文字
    eva = get_content(rcg_file).get('data')
    if eva and len(eva) == 3:
        rcg_text1, rcg_text2, rcg_text3 = eva[0], eva[1], eva[2]
    else:
        rcg_text1, rcg_text2, rcg_text3 = '', '', ''
    rcg_text = rcg_text1 + rcg_text2 + rcg_text3
    # rcg_text = get_content(rcg_file)['data']
    result['num'] = feature_text.len_without_punctuation(rcg_text)
    # last_time 时长 未擦除的文件
    with wave.open(wave_file_origin) as wav:
        result['last_time'] = wav.getnframes() / wav.getframerate()
    # interval 未擦除的文件
    # interval_list = utils.find_and_remove_intervals(wave_file_origin, wave_file_processed)
    for (start, last) in interval_list:
        if last > 2 and start > 0 and start + last > result['last_time'] - 0.02:
            result['interval_num'] += 1
            result['interval_ratio'] += last
    if result['last_time'] == 0:
        result['interval_ratio'] = 1
    else:
        result['interval_ratio'] /= result['last_time']
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
    # sum-aspects_num to parallel_num
    word_base = get_content('./text_files/Papers/wordbase.json')
    sum_aspects_words = sum_list(word_base['part4']['sum-aspects'])
    aspects_words = sum_list(word_base['part4']['aspects'])
    example_words = sum_list(word_base['part4']['example'])
    opinion_words = sum_list(word_base['part4']['opinion'])
    sum_words = sum_list(word_base['part4']['sum'])
    cause_affect_words = sum_list(word_base['part4']['cause-affect'])
    transition_words = sum_list(word_base['part4']['transition'])
    progressive_words = sum_list(word_base['part4']['progressive'])
    parallel_words = sum_list(word_base['part4']['parallel'])
    result['sum-aspects_num'] = feature_text.words(rcg_text, sum_aspects_words)
    result['aspects_num'] = feature_text.words(rcg_text, aspects_words)
    result['example_num'] = feature_text.words(rcg_text, example_words)
    result['opinion_num'] = feature_text.words(rcg_text, opinion_words)
    result['sum_num'] = feature_text.words(rcg_text, sum_words)
    result['cause-affect_num'] = feature_text.words(rcg_text, cause_affect_words)
    result['transition_num'] = feature_text.words(rcg_text, transition_words)
    result['progressive_num'] = feature_text.words(rcg_text, progressive_words)
    result['parallel_num'] = feature_text.words(rcg_text, parallel_words)
    # speed
    if not result['last_time'] == 0:
        result['speed1'] = 3 * feature_text.len_without_punctuation(rcg_text1) / result['last_time']
        result['speed2'] = 3 * feature_text.len_without_punctuation(rcg_text2) / result['last_time']
        result['speed3'] = 3 * feature_text.len_without_punctuation(rcg_text3) / result['last_time']
    # volume
    volume_list = feature_audio.get_volume(wave_file_processed, 3)
    result['volume1'], result['volume2'], result['volume3'] = volume_list[0], volume_list[1], volume_list[2]

    return result


def get_content(file):
    with open(file, 'r') as f:
        result = f.read()
    return json.loads(result)


def get_sentence_durations(simp_result):
    sd = list()
    for sentence in simp_result:
        words_pos = sentence['words_pos']
        duration = 0
        word_count = 0
        for wp in words_pos:
            if wp[0] != 'sil' and wp[0] != 'silv' and wp[0] != 'fil':
                word_count += 1
            duration += (wp[2] - wp[1])
            if wp == words_pos[-1]:
                if words_pos[0] == 'sil' or words_pos[0] == 'silv':
                    word_count -= 1
                    duration -= (words_pos[0][2] - words_pos[0][1])
                if words_pos[-1] == 'sil' or words_pos[-1] == 'silv':
                    word_count -= 1
                    duration -= (words_pos[-1][2] - words_pos[-1][1])
                if word_count > 0 and duration > 0:
                    sd.append((word_count, duration / 100))
                duration = 0
                word_count = 0
    return sd


def sum_list(lists):
    result = []
    for l in lists:
        result += l
    return result


if __name__ == '__main__':
    pass
