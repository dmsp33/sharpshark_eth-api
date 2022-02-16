import json

from web3eth import web3worker

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    print('received: {}'.format(event))

    return {
        "statusCode": 200,
        "body": json.dumps(mint_nft(event["pathParameters"]["hashipfs"])),
    }

def mint_nft(ipfs_hash):
    """
    Mint NFT with ipfs hash in tokenURI
    `ipfs_hash` 46-byte string like QmafZq1ZYLGvQJKAVt8PM3Y78to5wQrsazyasqdBCB9XU9 
    """
    r = web3worker.handle_mint_nft(ipfs_hash)
    print(r)
    item = {
        'ipfs_hash': ipfs_hash, 
        'state': 'queued_up', 
        'tx_hash': r,
        'link': '{}{}'.format(web3worker.config.TX_LINK_PREFIX, r)
    }
    return item
