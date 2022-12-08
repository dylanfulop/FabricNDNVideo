from ndn.app import NDNApp
from ndn.encoding import Name
import argparse
from time import sleep
import time
from ndn.types import InterestCanceled, InterestTimeout, InterestNack, ValidationFailure
from math import ceil

bit_rates = ['45226', '88783', '128503', '177437', '217761', '255865', '323047', '378355', '509091', '577751', '782553', '1008699', 
'1207152',  '1473801',  '2087347', '2409742',  '2944291',  '3340509', '3613836',  '3936261']#20

parser = argparse.ArgumentParser(description='NDN Video consumer')
parser.add_argument('--log_file', '-l', type=str, help='the file for logging',default='/tmp/ndnvidlog.csv')
parser.add_argument('--namespace', '-n',type=str,help='the namespace of the video to stream', default='/producer/big_buck_bunny')
parser.add_argument('--must_be_fresh', '-f', action='store_true')

args = parser.parse_args()

log_file =  open(args.log_file, 'wb')

app = NDNApp()



#wondershaper TODO TODO add to install script wondershaper sudo wondershaper ens7 <up> <down> to set speeds
async def get_segment(namespace, segment_number, bitrate_number, segment_size):
    i = 0
    cont = True
    byte_content = b''
    data_name, meta_info, content = await app.express_interest(f'{args.namespace}/b{bitrate_number}/4s{segment_number}/meta', must_be_fresh=args.must_be_fresh, can_be_prefix=False, lifetime=6000)
    num_chunks = int(str(bytes(content))[2:-1])
    while cont:
        start_time = time.time()
        tries = 0
        while tries < 5:
            try:
                data_name, meta_info, content = await app.express_interest(f'{args.namespace}/b{bitrate_number}/{segment_size}s{segment_number}/c{i}', must_be_fresh=args.must_be_fresh, can_be_prefix=False, lifetime=6000)
                break
            except InterestTimeout:
                tries+=1
                time.sleep(2)
        if tries >= 5:
            return False
        end_time = time.time()
        time_length = end_time - start_time
        # print(time_length, num_chunks, time_length*(num_chunks-i))
        i += 1
        if time_length * (num_chunks-i) > segment_size*2.8: 
            return False
        if content is None or bytes(content)==b'': cont = False 
        else: byte_content += bytes(content)
    with open(f'/home/ubuntu/NDN_STREAMING/Files/BigBuckBunny_{segment_size}s{segment_number}.m4s', 'wb') as f:
        f.write(byte_content)
    return True

async def stream_video():
    
    log_file.write(f'time since start, playback time, playback segments, buffer size, remaining segments, segments, bitrate index, segment latency, times buffered, time spent buffering, bit rate\n'.encode())

    data_name, meta_info, content = await app.express_interest(f'{args.namespace}/meta', must_be_fresh=args.must_be_fresh, can_be_prefix=False, lifetime=6000)
    content = str(bytes(content))[2:-1]
    print(content)
    ind = content.find('|')
    num_bitrates = int(content[:ind])

    content = content[ind+1:]
    print(content)
    ind = content.find('|')
    num_segments = int(content[:ind])

    content = content[ind+1:]
    print(content)
    segment_size = int(content)

    print(num_bitrates, num_segments, segment_size)

    latency_record = [0]*(num_segments+1)
    bitrate_record = [0]*(num_segments+1)
    buffer_count = 0

    streaming_start = time.time() 
    segments_retrieved = 0
    bitrate = num_bitrates-1
    playback_time = 0
    buffering = True

    buffer_time = 0
    buffer_start = time.time()

    playback_started = False

    #init, 1-150 sg numbers
    for i in range(num_segments+1):
        cont = False 
        while not cont:
            segment_start = time.time() 
            if i == 0:  cont = await get_segment(args.namespace,'init', bitrate, segment_size)
            else:  cont = await get_segment(args.namespace, i, bitrate, segment_size)
            segment_end = time.time() 
            if not cont:
                bitrate-=1
                if bitrate < 0: bitrate = 0
        print(f"retrieved segment {i} at bitrate {bitrate}")
        #bitrate statistics
        #latency statistics
        segment_latency = segment_end - segment_start 
        latency_record[i] = segment_latency 
        bitrate_record[i] = bitrate
        if i!= 0: segments_retrieved+=1

        if playback_started:  playback_time = time.time() - playback_start
        else: playback_time = 0

        total_video_time = num_segments*segment_size
        playback_segments = ceil(playback_time/segment_size)
        time_since_start = time.time() - streaming_start
        extra_segment_latency = segment_latency - segment_size
        if extra_segment_latency < 0: extra_segment_latency = 0
        remaining_segments = num_segments - segments_retrieved
        remaining_time = remaining_segments*segment_size
        extra_time_stacked = extra_segment_latency*remaining_segments
        buffer_size = segments_retrieved - playback_segments
        previous_bitrate = bitrate 

        if segment_latency > segment_size*2.5: bitrate=bitrate-3
        if extra_time_stacked > segment_size*(buffer_size-2): bitrate -= 1 #without the -1 to the buffer size, technically works, but not very dynamic if something goes wrong. Buffer tends to only have 1 item in it (bad)
        elif extra_time_stacked < segment_size*(buffer_size-3): bitrate += 1
        if bitrate > num_bitrates-1: bitrate = num_bitrates-1
        if bitrate < 0: bitrate = 0

        if i == 2:
            playback_previous = 0
            buffering = False
            playback_start = time.time()
            buffer_time += time.time()-buffer_start
            buffer_count += 1
            playback_started = True
        if i > 2 and not buffering:
            if playback_segments > segments_retrieved:
                bitrate -= 3 
                if bitrate > num_bitrates-1: bitrate = num_bitrates-1
                if bitrate < 0: bitrate = 0
                playback_previous = playback_time
                buffering = True 
                buffer_start = time.time()
        if i > 2 and buffering and playback_segments < segments_retrieved - 2:
            playback_start = time.time() - playback_previous
            bufferfing = False 
            #buffer statistics
            buffer_count += 1
            buffer_time += time.time()-buffer_start
        print(f"{time_since_start}s | {playback_time}s played | {playback_segments} segments played | {buffer_size}/{remaining_segments} buffered | seg {i} | rate {previous_bitrate} | {segment_latency}s latency | {buffer_count} buffers | {buffer_time}s spent buffering ")
        print(f"{remaining_segments} segments left")
        log_file.write(f'{time_since_start},{playback_time},{playback_segments},{buffer_size},{remaining_segments},{i},{previous_bitrate},{segment_latency},{buffer_count},{buffer_time},{bit_rates[previous_bitrate]}\n'.encode())
        
        
    streaming_end = time.time() 
    print(buffer_count)
    print(streaming_end - streaming_start)
    print(latency_record)
    print(bitrate_record)
    print(buffer_time)
    log_file.close()
        
        



async def main():
    try:
        await stream_video()
    except InterestNack as e:
        # A NACK is received
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # Interest times out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to NFD is broken
        print(f'Canceled')
    except ValidationFailure:
        # Validation failure
        print(f'Data failed to validate')
    finally:
        app.shutdown()
    
app.run_forever(after_start=main())