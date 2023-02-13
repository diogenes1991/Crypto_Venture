from API import API
import requests
from web3 import Web3

class AlchemyETH(API):
    
    base_url = "https://eth-mainnet.g.alchemy.com/v2/"
    header = {
    "accept": "application/json",
    "content-type": "application/json"
    }
    
    defaults = {"fromBlock":"0x0",
               "toBlock":"latest",
               "category":["external", "internal", "erc20", "erc721", "erc1155", "specialnft"],
               "withMetadata":True,
               "excludeZeroValue":True,
               "maxCount":"0x3e8"
              }
    
    def start(self):
        self.url = self.base_url + self.api_key
    
    def getAssetTransfers(self,address):
        rval = {}
        
        outparams = [self.defaults.copy()]
        outparams[0]["fromAddress"] = address
        outjson = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "alchemy_getAssetTransfers",
                "params": outparams
                }
        rval["Outgoing"] = PaginatedResponse(self,outjson)
        
        innparams = [self.defaults.copy()]
        innparams[0]["toAddress"]   = address
        innjson = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "alchemy_getAssetTransfers",
                "params": innparams
                }
        rval["Incoming"] = PaginatedResponse(self,innjson)
    
        return rval
    
    def __call__(self,request):
        return requests.post(self.url,json=request,headers=self.header).json()

class PaginatedResponse:
    def __init__(self,api_endpoint,request):
        ''' Create a generator of the pages '''
        self.api_endpoint   = api_endpoint
        self.request        = request
        self.orig_req       = self.request
        self.has_failed     = False
    
    def get_next_page(self):
        if self.request == None:
            return False
        else:
            try:
                self.current_page = self.api_endpoint(self.request)
                if "pageKey" in self.current_page["result"].keys():
                    self.request["params"][0]["pageKey"] = self.current_page["result"]["pageKey"]
                else:
                    self.request = None
                return True
            except:
                print("Request Failed",self.request)
                print(self.current_page)
                print("Retrying...")
                self.get_next_page()
    
    def restart(self):
        self.request = self.orig_request

        