
from ndn.app import NDNApp
from ndn.encoding import Name
import argparse
from time import sleep
    
app = NDNApp()

async def main():
    pass


@app.route('/producer/test/msg2')
def on_interest(name, interest_param, application_param):
    app.put_data(name, content=b'content', freshness_period=10000)

app.run_forever(after_start=main())