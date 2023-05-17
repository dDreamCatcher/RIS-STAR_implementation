#!/usr/bin/env python
import uhd
from gnuradio import gr
import time
import ipdb
import numpy
from scipy.io import savemat



def set_center_freq(uhd_usrp_source, center_freq, sources):
        # Tune all channels to the desired frequency
        
        tune_req =  uhd.libpyuhd.types.tune_request(center_freq)
        tune_resp = uhd_usrp_source.set_rx_freq(tune_req, 0)
        print(uhd_usrp_source.get_rx_freq(0))
        tune_req.rf_freq = center_freq
        tune_req.rf_freq_policy = uhd.libpyuhd.types.tune_request_policy.manual
        tune_req.dsp_freq_policy = uhd.libpyuhd.types.tune_request_policy.manual
        tune_req.dsp_freq = tune_resp.actual_dsp_freq

        for chan in range(sources):
                uhd_usrp_source.set_rx_freq(tune_req, chan)

        # Synchronize the tuned channels
        now = uhd_usrp_source.get_time_now()
        print(now.get_real_secs())
        print(now.get_frac_secs())


        # ipdb.set_trace()
        uhd_usrp_source.set_command_time(now + uhd.libpyuhd.types.time_spec(0.01))

        for chan in range(4):
            uhd_usrp_source.set_rx_freq(tune_req, chan)

        now2 = uhd_usrp_source.get_time_now()
        print(now2.get_real_secs()) 
        print(now2.get_frac_secs())       
        time.sleep(0.11)

        uhd_usrp_source.clear_command_time()
        print(uhd_usrp_source.get_rx_freq(3))


def create_rx_stream(uhd_usrp_source):
        #create a receive streamer
        num_samps = 200000
        st_args = uhd.usrp.StreamArgs("fc32", "sc16")
        st_args.channels = range(4)
        metadata = uhd.types.RXMetadata()
        rx_streamer = uhd_usrp_source.get_rx_stream(st_args)


        #Setup streaming
        # ipdb.set_trace()
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = False
        stream_cmd.time_spec = uhd_usrp_source.get_time_now() + uhd.libpyuhd.types.time_spec(1.0)
        rx_streamer.issue_stream_cmd(stream_cmd)
        recv_buffer = numpy.zeros((4, 1000), dtype=numpy.complex64)


        #Setup streaming
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = False
        stream_cmd.time_spec = uhd_usrp_source.get_time_now() + uhd.libpyuhd.types.time_spec(1.0)
        rx_streamer.issue_stream_cmd(stream_cmd)

        # Receive Samples
        samples = numpy.zeros((4, num_samps), dtype=numpy.complex64)
        for i in range(num_samps//1000):
            rx_streamer.recv(recv_buffer, metadata)
            samples[0][i*1000:(i+1)*1000] = recv_buffer[0]
            samples[1][i*1000:(i+1)*1000] = recv_buffer[1]
            samples[2][i*1000:(i+1)*1000] = recv_buffer[2]
            samples[3][i*1000:(i+1)*1000] = recv_buffer[3]

        # Stop Stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        rx_streamer.issue_stream_cmd(stream_cmd)

        # ipdb.set_trace()
        print(samples.shape)
        print(samples)

        return samples
 

##################################################
samp_rate = 400000
center_freq = 900000000
gain = [0,0,0,0]
sources = 4
addresses = "addr0=192.168.10.2,addr1=192.168.70.2"

##################################################
# Blocks
##################################################
uhd_usrp_source_0 = uhd.usrp.MultiUSRP(addresses)
uhd_usrp_source_0.set_clock_source('external')
uhd_usrp_source_0.set_time_source('external')
subdevs = "A:0 B:0"

for device in range(int(sources/2)):
        uhd_usrp_source_0.set_rx_subdev_spec(uhd.usrp.SubdevSpec(subdevs),device)

# Set channel specific settings
for chan in range(sources):
        uhd_usrp_source_0.set_rx_rate(samp_rate, chan)
        uhd_usrp_source_0.set_rx_gain(gain[chan], chan)
        uhd_usrp_source_0.set_rx_dc_offset(False, chan)
        uhd_usrp_source_0.set_rx_antenna('RX2', chan)
        uhd_usrp_source_0.set_rx_iq_balance(False, chan)

# Reset radios' sense of time to 0.000s on the next PPS edge:
uhd_usrp_source_0.set_time_next_pps(uhd.libpyuhd.types.time_spec(0.0))
time.sleep(1)

# Use timed commands to set frequencies
#This will ensure that the LO and DSP chain of our USRPs are retuned synchronously (on the same clock cycle).
set_center_freq(uhd_usrp_source_0, center_freq, sources)
data = create_rx_stream(uhd_usrp_source_0)

#write to .mat file

data_dic = {"ant1":data[0], "ant2":data[1], "ant3":data[2], "ant4":data[3]}

savemat("simo_file.mat", data_dic)



