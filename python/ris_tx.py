#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: ris_tx
# Author: genesys
# GNU Radio version: 3.8.4.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

from gnuradio import qtgui

class ris_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "ris_tx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("ris_tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "ris_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.gain = gain = 80
        self.freq_0 = freq_0 = 890e6

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", "addr=192.168.50.2", "master_clock_rate=200e6")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_subdev_spec("A:0", 0)
        self.uhd_usrp_sink_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(freq_0,1e6), 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_clock_rate(200e6, uhd.ALL_MBOARDS)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_time_sink_x_0_0_1_1_0_0 = qtgui.time_sink_f(
            200000, #size
            samp_rate, #samp_rate
            'Tx Signal', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0_1_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_1_1_0_0.enable_stem_plot(False)


        labels = ['IQ', 'Corr Output', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_1_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_1_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_1_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_1_1_0_0_win)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/genesys/Desktop/txData.bin', True, 10, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_real_0, 0), (self.qtgui_time_sink_x_0_0_1_1_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.uhd_usrp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ris_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0_0_1_1_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.freq_0,1e6), 0)





def main(top_block_cls=ris_tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
