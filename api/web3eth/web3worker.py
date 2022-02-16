# -*- coding: utf-8 -*-
import logging
import os, sys
import json
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from . import config

def get_tx_receipt(tx_hash):
    return w3.eth.get_transaction_receipt(tx_hash)

def get_token_uri(_tokenId):
    return token721.functions.tokenURI(int(_tokenId)).call()


def handle_mint_nft(_ipfs_hash = None):
    """
    Sign  and Send new mint transaction to blockchain
    
    """
    try:
        if  _ipfs_hash is None:
            _ipfs_hash = ''
        #######################################################
        #1. Prepare contrac method
        ########################################################
        tx_data = token721.encodeABI(
            fn_name = "mintWithURI", #qdefi
            args    = [_ipfs_hash]
        )
        logging.debug('tx_data={}'.format(tx_data))

        ###################################################
        #2. eth tx
        tx_full_data={
            'to': config.ADDRESS_721, 
            'from': config.ADDRESS_OPERATOR, 
            'data': tx_data,
            'nonce':w3.eth.getTransactionCount(config.ADDRESS_OPERATOR), 
            #'nonce':2, 
            'gas':200000, 
            'gasPrice': _gasPrice
        }
        logging.debug('tx_full_data={}'.format(tx_full_data))

        _estGas = w3.eth.estimateGas(tx_full_data)
        logging.info(
            '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n'
            'Estimate gas = {}\n'
            'gasPrice = {} gwei\n'
            'Estimate tx cost = {} eth\n'.format(
                _estGas,
                w3.fromWei(_gasPrice, 'gwei'),
                w3.fromWei(_estGas*_gasPrice, 'ether')
            )
        )
    
    except Exception as e:
        logging.warning('Error in w3.eth.estimateGas = {}'.format(e.args))
    else:
        #Sign tx
        signed_tx=w3.eth.account.signTransaction(
            tx_full_data, 
            private_key=config.ADDRESS_OPERATOR_PRIVKEY
        )
        logging.debug('signed_tx={}'.format(signed_tx))
        
        #Send Raw tx
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info('Etherscan tx_hash= {}'.format(tx_hash.hex()))
        return tx_hash.hex() 
    finally:
        pass


def main(_ipfs_hash = None):
    """
    Mint nft with _ipfs_hash
    """
    handle_mint_nft(_ipfs_hash)
    pass 
####################################################################
####################################################################

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################

########################################
###  Module initialize section      ####
########################################
logging.basicConfig(format='%(asctime)s->%(levelname)s:[in %(filename)s:%(lineno)d]:%(message)s'
    , level=int(config.APP_LOGLEVEL)
)

#txSenderAddress = '0x86C3582b6505CcB8faDAcb211fC1E5a8fDD26E91' #ExoACCICO
#web3 provider initializing
if 'http:'.upper() in config.WEB3_PROVIDER.upper():
    w3 = Web3(HTTPProvider(config.WEB3_PROVIDER))
elif 'ws:'.upper()  in config.WEB3_PROVIDER.upper() or 'wss:'.upper() in config.WEB3_PROVIDER.upper():
    w3 = Web3(Web3.WebsocketProvider(config.WEB3_PROVIDER))    
else:
    w3 = Web3(IPCProvider(config.WEB3_PROVIDER))
logging.info('w3.eth.blockNumber=' + str(w3.eth.blockNumber))
#w3.eth.defaultAccount  = config.ADDRESS_OPERATOR


_gasPrice = w3.toWei(config.GAS_PRICE, 'wei')

#Need some injection on Rinkeby and -dev networks
if  w3.net.version == '4':
    from web3.middleware import geth_poa_middleware
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)


token721 = w3.eth.contract(address=config.ADDRESS_721,
    abi=config.ERC721_ABI
)

name     = token721.functions.name().call()
symbol   = token721.functions.symbol().call()
logging.debug('Token contract at address {} initialized:{} ({})'.format(
    config.ADDRESS_721,
    name,
    symbol,
    )
)

###########################################
if __name__ == '__main__':
    ipfs_hash = None
    if  len(sys.argv)==2:
        ipfs_hash = sys.argv[1]
        #TODO validate hash
    logging.info('Start as main with params {}'.format(sys.argv))    
    main(ipfs_hash)