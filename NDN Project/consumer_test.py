
from ndn.app import NDNApp
from ndn.encoding import Name
import argparse

parser = argparse.ArgumentParser(description='Basic consumer app test')
parser.add_argument('interest', type=str, help='the interest name to consume')
parser.add_argument('--must_be_fresh', '-f', action='store_true')
parser.add_argument('--can_be_prefix', '-p', action='store_true')
args = parser.parse_args()

interest = args.interest
fresh = args.must_be_fresh
prefix = args.can_be_prefix
# print(interest,fresh,prefix)


app = NDNApp()

async def main():
    try:
        data_name, meta_info, content = await app.express_interest(
            # Interest Name
            interest,
            must_be_fresh=fresh,
            can_be_prefix=prefix,
            # Interest lifetime in ms
            lifetime=6000)
        # Print out Data Name, MetaInfo and its conetnt.
        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)
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