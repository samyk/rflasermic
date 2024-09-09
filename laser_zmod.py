#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: samy
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip



class laser_zmod(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "laser_zmod")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_au = samp_rate_au = 96000
        self.samp_rate = samp_rate = samp_rate_au * 23
        self.mid_decim = mid_decim = int(samp_rate/samp_rate_au/5)
        self.mid_sr = mid_sr = int(samp_rate/mid_decim)
        self.upconvert_freq = upconvert_freq = 125000000
        self.rf_offset = rf_offset = 30e3*10
        self.laser_freq = laser_freq = 0
        self.end_decim = end_decim = int(mid_sr/samp_rate_au)
        self.up_offset = up_offset = 0
        self.trw = trw = 5000
        self.rf_gain = rf_gain = 0
        self.rf_freq = rf_freq = laser_freq+rf_offset+upconvert_freq
        self.lpf = lpf = 20000*2.4
        self.if_gain = if_gain = 10
        self.hpf = hpf = 100
        self.gain_xlat = gain_xlat = 10
        self.gain_hp = gain_hp = 10
        self.end_sr = end_sr = int(mid_sr/end_decim)
        self.decim = decim = int(samp_rate/samp_rate_au)
        self.bb_gain = bb_gain = 10

        ##################################################
        # Blocks
        ##################################################

        self._rf_gain_range = qtgui.Range(0, 100, 1, 0, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "'rf_gain'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        self._laser_freq_range = qtgui.Range(0, 3050000, 1, 0, 200)
        self._laser_freq_win = qtgui.RangeWidget(self._laser_freq_range, self.set_laser_freq, "'laser_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._laser_freq_win)
        self._if_gain_range = qtgui.Range(1, 64, 1, 10, 200)
        self._if_gain_win = qtgui.RangeWidget(self._if_gain_range, self.set_if_gain, "'if_gain'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._if_gain_win)
        self._gain_xlat_range = qtgui.Range(1, 100, 1, 10, 200)
        self._gain_xlat_win = qtgui.RangeWidget(self._gain_xlat_range, self.set_gain_xlat, "'gain_xlat'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_xlat_win)
        self._gain_hp_range = qtgui.Range(1, 100, 1, 10, 200)
        self._gain_hp_win = qtgui.RangeWidget(self._gain_hp_range, self.set_gain_hp, "'gain_hp'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._gain_hp_win)
        self._bb_gain_range = qtgui.Range(1, 64, 1, 10, 200)
        self._bb_gain_win = qtgui.RangeWidget(self._bb_gain_range, self.set_bb_gain, "'bb_gain'", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bb_gain_win)
        self.qtgui_freq_sink_x_0_0_0_0_0_1 = qtgui.freq_sink_f(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate_au, #bw
            'xlat freq', #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_update_time(0.1)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_fft_window_normalized(True)


        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_plot_pos_half(not False)

        labels = ['hp+xlat/dec', 'hp+xlat+resamp', 'xlat/decim', 'bp+xlat/decim', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "cyan", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_0_0_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            rf_freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.25)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            mid_sr, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'hackrf=0'
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(rf_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.high_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.high_pass(
                gain_hp,
                samp_rate_au,
                60,
                100,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0_0_1 = filter.freq_xlating_fir_filter_ccc(mid_decim, firdes.band_pass(gain_xlat, samp_rate, 30, lpf, trw), (laser_freq-laser_freq-rf_offset+up_offset), samp_rate)
        self.blocks_correctiq_0 = blocks.correctiq()
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0 = audio.sink(samp_rate_au, '', True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.high_pass_filter_1, 0))
        self.connect((self.blocks_correctiq_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_1, 0), (self.blocks_correctiq_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.high_pass_filter_1, 0), (self.audio_sink_0, 0))
        self.connect((self.high_pass_filter_1, 0), (self.qtgui_freq_sink_x_0_0_0_0_0_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0_1, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "laser_zmod")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate_au(self):
        return self.samp_rate_au

    def set_samp_rate_au(self, samp_rate_au):
        self.samp_rate_au = samp_rate_au
        self.set_decim(int(self.samp_rate/self.samp_rate_au))
        self.set_end_decim(int(self.mid_sr/self.samp_rate_au))
        self.set_mid_decim(int(self.samp_rate/self.samp_rate_au/5))
        self.set_samp_rate(self.samp_rate_au * 23)
        self.high_pass_filter_1.set_taps(firdes.high_pass(self.gain_hp, self.samp_rate_au, 60, 100, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0_0_0_0_1.set_frequency_range(0, self.samp_rate_au)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_decim(int(self.samp_rate/self.samp_rate_au))
        self.set_mid_decim(int(self.samp_rate/self.samp_rate_au/5))
        self.set_mid_sr(int(self.samp_rate/self.mid_decim))
        self.freq_xlating_fir_filter_xxx_0_0_1.set_taps(firdes.band_pass(self.gain_xlat, self.samp_rate, 30, self.lpf, self.trw))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rf_freq, self.samp_rate)

    def get_mid_decim(self):
        return self.mid_decim

    def set_mid_decim(self, mid_decim):
        self.mid_decim = mid_decim
        self.set_mid_sr(int(self.samp_rate/self.mid_decim))

    def get_mid_sr(self):
        return self.mid_sr

    def set_mid_sr(self, mid_sr):
        self.mid_sr = mid_sr
        self.set_end_decim(int(self.mid_sr/self.samp_rate_au))
        self.set_end_sr(int(self.mid_sr/self.end_decim))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.mid_sr)

    def get_upconvert_freq(self):
        return self.upconvert_freq

    def set_upconvert_freq(self, upconvert_freq):
        self.upconvert_freq = upconvert_freq
        self.set_rf_freq(self.laser_freq+self.rf_offset+self.upconvert_freq)

    def get_rf_offset(self):
        return self.rf_offset

    def set_rf_offset(self, rf_offset):
        self.rf_offset = rf_offset
        self.set_rf_freq(self.laser_freq+self.rf_offset+self.upconvert_freq)
        self.freq_xlating_fir_filter_xxx_0_0_1.set_center_freq((self.laser_freq-self.laser_freq-self.rf_offset+self.up_offset))

    def get_laser_freq(self):
        return self.laser_freq

    def set_laser_freq(self, laser_freq):
        self.laser_freq = laser_freq
        self.set_rf_freq(self.laser_freq+self.rf_offset+self.upconvert_freq)
        self.freq_xlating_fir_filter_xxx_0_0_1.set_center_freq((self.laser_freq-self.laser_freq-self.rf_offset+self.up_offset))

    def get_end_decim(self):
        return self.end_decim

    def set_end_decim(self, end_decim):
        self.end_decim = end_decim
        self.set_end_sr(int(self.mid_sr/self.end_decim))

    def get_up_offset(self):
        return self.up_offset

    def set_up_offset(self, up_offset):
        self.up_offset = up_offset
        self.freq_xlating_fir_filter_xxx_0_0_1.set_center_freq((self.laser_freq-self.laser_freq-self.rf_offset+self.up_offset))

    def get_trw(self):
        return self.trw

    def set_trw(self, trw):
        self.trw = trw
        self.freq_xlating_fir_filter_xxx_0_0_1.set_taps(firdes.band_pass(self.gain_xlat, self.samp_rate, 30, self.lpf, self.trw))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_rf_freq(self):
        return self.rf_freq

    def set_rf_freq(self, rf_freq):
        self.rf_freq = rf_freq
        self.osmosdr_source_0.set_center_freq(self.rf_freq, 0)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.rf_freq, self.samp_rate)

    def get_lpf(self):
        return self.lpf

    def set_lpf(self, lpf):
        self.lpf = lpf
        self.freq_xlating_fir_filter_xxx_0_0_1.set_taps(firdes.band_pass(self.gain_xlat, self.samp_rate, 30, self.lpf, self.trw))

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_hpf(self):
        return self.hpf

    def set_hpf(self, hpf):
        self.hpf = hpf

    def get_gain_xlat(self):
        return self.gain_xlat

    def set_gain_xlat(self, gain_xlat):
        self.gain_xlat = gain_xlat
        self.freq_xlating_fir_filter_xxx_0_0_1.set_taps(firdes.band_pass(self.gain_xlat, self.samp_rate, 30, self.lpf, self.trw))

    def get_gain_hp(self):
        return self.gain_hp

    def set_gain_hp(self, gain_hp):
        self.gain_hp = gain_hp
        self.high_pass_filter_1.set_taps(firdes.high_pass(self.gain_hp, self.samp_rate_au, 60, 100, window.WIN_HAMMING, 6.76))

    def get_end_sr(self):
        return self.end_sr

    def set_end_sr(self, end_sr):
        self.end_sr = end_sr

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)




def main(top_block_cls=laser_zmod, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
