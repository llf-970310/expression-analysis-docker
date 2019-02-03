#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 19-2-3

from _xf_recognise import rcg_and_save


if __name__ == '__main__':
    import io
    import utils
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

    # result = rcg(config.WAV_FILE_PATH, segments=1, timeout=100)
    # rcg(config.WAV_FILE_PATH, timeout=10, segments=3)
    # print(isinstance(result, str))
    # print(isinstance(result, dict))

    wave_file_processed = io.BytesIO()
    interval_list = utils.find_and_remove_intervals('net_test.wav', wave_file_processed)

    rcg_fp = io.StringIO()
    rcg_and_save(wave_file_processed, rcg_fp, segments=3, timeout=1, stop_on_failure=True)

    print(utils.read(rcg_fp))
