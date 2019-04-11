import io
import base_recognise
import base_evaluate
import feature_text
import feature_audio
import wave
import utils
import config
import numpy
import json

import numpy as np


def analysis_features(wave_file, wordbase, timeout=30, voice_features=None, rcg_interface='baidu'):
    result = {
        'rcg_text': '',
        'key_hits': [],     # key击中列表
        'keywords': [],     # 击中的keyword列表
        'detail_hits': [],  # detail击中列表
        'detailwords': [],  # 击中的detailword列表
        'num': 0,           # 字数
        'sentence_num': 0,  # 句子数

        'last_time': 0,     # 持续时间
        'interval_num': 0,  # 中断次数
        'interval_ratio': 0,    # 中断比率
        'volumes': 0,
        'speeds': 0,

    }

    # 分析音频特征并分段识别，如果传入voice_features就不分析
    if voice_features:
        result['rcg_text'] = voice_features['rcg_text']
        result['last_time'] = voice_features['last_time']
        result['interval_num'] = voice_features['interval_num']
        result['interval_ratio'] = voice_features['interval_ratio']
        result['volumes'] = voice_features['volumes']
        result['speeds'] = voice_features['speeds']
    else:
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
        rcg_result_file = io.StringIO()
        # volume
        result['volumes'] = feature_audio.get_volume(wave_file_processed, config.SEGMENTS_VOLUME2)

        # 分段识别
        base_recognise.rcg_and_save(wave_file_processed, rcg_result_file, timeout=timeout,
                                    segments=config.SEGMENTS_RCG2, rcg_interface=rcg_interface)
        temp = json.loads(rcg_result_file.getvalue()).get('data')
        if temp and len(temp) == config.SEGMENTS_RCG2:
            rcg_text = ''.join(temp)
        else:
            rcg_text = ''
        # speed
        if not result['last_time'] == 0:
            result['speeds'] = [
                config.SEGMENTS_RCG2 * feature_text.len_without_punctuation(rcg_text_seg) / result['last_time'] for
                rcg_text_seg in temp]
        result['rcg_text'] = rcg_text

    # 字数
    result['num'] = feature_text.len_without_punctuation(result['rcg_text'])

    # 句子数
    result['sentence_num'] = len(feature_text.divide_text_to_sentence(result['rcg_text']))

    # 词库击中，谐音
    keywords, detailwords = wordbase.get('keywords'), wordbase.get('detailwords')

    for word in keywords:
        hitwords = feature_text.words_pronunciation(text=result['rcg_text'], answers=word)
        if len(hitwords) >= 1:
            result['key_hits'].append(1)  # 是否击中
            result['keywords'].append(hitwords[0])  # 添加被击中的词语
        else:
            result['key_hits'].append(0)
            result['keywords'].append('')

    for temp_l in detailwords:
        x = 0
        temp_words = []
        temp_hits = []
        for word in temp_l:
            hitwords = feature_text.words_pronunciation(text=result['rcg_text'], answers=word)
            if len(hitwords) >= 1:
                x += 1
                temp_hits.append(1)  # 是否击中
                temp_words.append(hitwords[0])  # 添加被击中的词语
            else:
                temp_hits.append(0)
                temp_words.append('')
        result['detail_hits'].append(temp_hits)
        result['detailwords'].append(temp_words)

    return result


def compute_score(key_hits, detail_hits, key_weights, detail_weights):
    np_key_hits = np.array([1] + key_hits)
    temp_detail_hits = []
    for w in detail_hits:
        temp_detail_hits += w
    np_detail_hits = np.array([1] + temp_detail_hits)
    np_key_weights = np.array(key_weights)
    np_detail_weights = np.array(detail_weights)
    key = 0 if np_key_hits[1:].sum() == 0 else (np_key_hits * np_key_weights).sum()
    detail = 0 if np_detail_hits[1:].sum() == 0 else (np_detail_hits * np_detail_weights).sum()
    return {
        'key': key if 0 <= key <= 100 else ( 0 if key < 0 else 100),
        'detail': detail if 0 <= detail <= 100 else ( 0 if detail < 0 else 100)
    }


if __name__ == '__main__':
    path = '/Users/gyue/Programs/exp-docker/expression/net_test.wav'
    wordbase = {"keywords":[["胡杨"],["抗旱","干旱"],["生命力"],["强"]],"mainwords":[["扎根"],["贮水","存水"],["盐碱"],["温差","降水量","蒸发量"],["寿命"],["沙漠","荒漠","草原"]],"detailwords":[[["10","十"],["固土","防沙","水土流失","环境保护"],["地下水","含水层","水源","雨水"]],[["储存","存储","贮存","存放","蓄水","保存"],["干旱","旱季","潮湿","缺水","干燥","寒冷","雨季"]],[["树叶","树枝","树干","叶子","枝叶","枝干"],["排出"],["盐碱"]],[["荒漠","草原","沙漠"],["41","四十"],["零下","低温"],["高温","室温","加热","高低温"],["千","寿命"],["39","三十九","80","八十"]]]}
    feature_result = analysis_features(path, wordbase, timeout=30)
    print(feature_result)
    key_weights = [26, 26.0, 26.0, 26.0, 26.0]
    detail_weights = [8, 8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714, 
            8.14285714285714
        ]
    score = compute_score(feature_result['key_hits'], feature_result['detail_hits'], key_weights, detail_weights)
    print(score)


