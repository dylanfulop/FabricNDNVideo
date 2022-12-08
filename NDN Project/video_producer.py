from ndn.app import NDNApp
from ndn.encoding import Name
import traceback
import argparse
from time import sleep
from ndn.types import InterestCanceled, InterestTimeout, InterestNack, ValidationFailure

app = NDNApp()

async def main():
    pass

bit_rates = ['45226', '88783', '128503', '177437', '217761', '255865', '323047', '378355', '509091', '577751', '782553', '1008699', 
'1207152',  '1473801',  '2087347', '2409742',  '2944291',  '3340509', '3613836',  '3936261']#20


# cached_bytes = b''
# cached_segment = ''

@app.route('/producer/big_buck_bunny/')
def on_interest(name, interest_param, application_param):
    bit_rate_str = str(bytes(name[2][2:]))[2:-1]
    if bit_rate_str == 'meta':
        app.put_data(name, content=b'20|120|4', freshness_period=1000)
        return
    else:
        print(bit_rate_str)
    bit_rate_num = int(str(bytes(name[2][2:]))[3:-1]) #b<index>
    bitrate = f'bunny_{bit_rates[bit_rate_num]}bps'
    seg_num = str(bytes(name[3][2:]))[2:-1]
    if (seg_num == '4sinit'):
        segment = f'BigBuckBunny_4s_init.mp4'
    else:
        segment = f'BigBuckBunny_{seg_num}.m4s' #4s<num>
    chunk_str = str(bytes(name[4][2:]))[2:-1]
    if (chunk_str == 'meta'): chunk = -1 
    else: chunk = int(str(bytes(name[4][2:]))[3:-1])#c<num>
    total_segment_name = bitrate + "_" + segment
    content_path = f'/var/www/html/media/BigBuckBunny/4sec/{bitrate}/{segment}'
    CHUNK_SIZE=8192
    start = chunk*CHUNK_SIZE
    end = chunk*CHUNK_SIZE + CHUNK_SIZE
    try:
        # if cached_segment != seg_num:
            with open(content_path, 'rb') as f:
                data = f.read()
                if chunk == -1:
                    app.put_data(name, content=f'{len(data)//CHUNK_SIZE}'.encode(), freshness_period=1000000)
                else:
                    c = data[start:end]
                    # cached_bytes = data
                    # cached_segment = seg_num
                    if chunk % 100 <= 10: print(content_path, chunk, len(data)/CHUNK_SIZE)
                    app.put_data(name, content=c, freshness_period=1000000)
        # else:
            # app.put_data(name, content=cached_bytes, freshness_period=10000)

    except:
        traceback.print_exc()
        print(content_path)
        app.put_data(name, content=b'no known file', freshness_period=1000000)

app.run_forever(after_start=main())
