#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-8-18

import logging
import os
import socket
import sys

import config
from xf_evaluate import evl_and_save
from xf_recognise import rcg_and_save
import timeout_decorator

import utils
import analysis_single


class Analysis1(object):
    def __init__(self, wav_file, std_text_file, features_return):
        self.wav_file = wav_file
        self.features_return = features_return
        self.std_text_file = std_text_file

    def run(self):
        logging.debug('Analysis1 now running...')
        evl_file = "/tmp/exp_1_evl.json"
        rcg_file = "/tmp/exp_1_rcg.json"
        new_wav_file = '/tmp/exp_1_rcg_processed.wav'
        os.system('rm -f "%s"' % '" "'.join((evl_file, rcg_file, new_wav_file)))
        intervals_lst = utils.find_and_remove_intervals(self.wav_file, new_wav_file)
        evl_and_save(new_wav_file, self.std_text_file, evl_file, framerate=8000)
        rcg_and_save(new_wav_file, rcg_file)
        feature1 = analysis_single.analysis1(self.wav_file, new_wav_file, evl_file, rcg_file, intervals_lst)
        self.features_return['feature1'] = feature1
        logging.debug('Analysis1 done.')


class Analysis2(object):
    def __init__(self, wave_file, features_return):
        self.wav_file = wave_file
        self.features_return = features_return

    def run(self):
        logging.debug('Analysis2 now running...')
        rcg_file = "/tmp/exp_2_rcg.json"
        new_wav_file = '/tmp/exp_2_rcg_processed.wav'
        os.system('rm -f "%s"' % '" "'.join((rcg_file, new_wav_file)))
        intervals_lst = utils.find_and_remove_intervals(self.wav_file, new_wav_file)
        rcg_and_save(new_wav_file, rcg_file, segments=3)
        feature2 = analysis_single.analysis2(self.wav_file, new_wav_file, rcg_file, intervals_lst)
        self.features_return['feature2'] = feature2
        logging.debug('Analysis2 done.')


class Analysis3(object):
    def __init__(self, wave_file, features_return):
        self.wav_file = wave_file
        self.features_return = features_return

    def run(self):
        logging.debug('Analysis3 now running...')
        rcg_file = "/tmp/exp_3_rcg.json"
        new_wav_file = '/tmp/exp_3_rcg_processed.wav'
        os.system('rm -f "%s"' % '" "'.join((rcg_file, new_wav_file)))
        intervals_lst = utils.find_and_remove_intervals(self.wav_file, new_wav_file)
        rcg_and_save(new_wav_file, rcg_file, segments=3)
        feature3 = analysis_single.analysis3(self.wav_file, new_wav_file, rcg_file, intervals_lst)
        self.features_return['feature3'] = feature3
        logging.debug('Analysis3 done.')


class Analysis4(object):
    def __init__(self, wave_file, features_return):
        self.wav_file = wave_file
        self.features_return = features_return

    def run(self):
        logging.debug('Analysis4 now running...')
        rcg_file = "/tmp/exp_4_rcg.json"
        new_wav_file = '/tmp/exp_4_rcg_processed.wav'
        os.system('rm -f "%s"' % '" "'.join((rcg_file, new_wav_file)))
        intervals_lst = utils.find_and_remove_intervals(self.wav_file, new_wav_file)
        rcg_and_save(new_wav_file, rcg_file, segments=3)
        feature4 = analysis_single.analysis4(self.wav_file, new_wav_file, rcg_file, intervals_lst)
        self.features_return['feature4'] = feature4
        logging.debug('Analysis4 done.')


def get_data(Qnum):
    pass


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('arguments too less')
    Qnum = int(sys.argv[1])
    wav_file = sys.argv[2]
    print(Qnum, wav_file)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

    features = dict()

    #std_text = get_std_text(Qnum=1)

    if Qnum == 1:
        std_text = "text_files/Papers/朗读提.txt"
        analysis = Analysis1(wav_file, std_text, features)
        analysis.run()
    elif Qnum == 2:
        analysis = Analysis2(wav_file, features)
        analysis.run()
    elif Qnum == 3:
        analysis = Analysis3(wav_file, features)
        analysis.run()
    elif Qnum == 4:
        analysis = Analysis4(wav_file, features)
        analysis.run()
    else:
        print('invalid question number')

    print(features)
