from typing import Dict

import aiomas
import async_timeout

from spruned.application.abstracts import RPCAPIService


class ElectrodService(RPCAPIService):
    def __init__(self, socketfile):
        self.socketfile = socketfile

    async def call(self, method, payload: Dict=None):
        async with async_timeout.timeout(3):
            rpc_con = await aiomas.rpc.open_connection(self.socketfile)
            call = getattr(rpc_con.remote, method)
            resp = payload is not None and await call(payload) or await call()
            await rpc_con.close()
            return resp

    async def getbestheight(self):
        return await self.call("getbestheight")

    async def getrawtransaction(self, txid, verbose=False):
        payload = {"txid": txid, "verbose": verbose}
        return await self.call("getrawtransaction", payload)

    async def getblockheader(self, blockhash, verbose=True):
        payload = {"block_hash": blockhash, "verbose": verbose}
        return await self.call("getblockheader", payload)

    async def getblock(self, txid, verbose=False):
        return None

    async def getblockhash(self, height: int):
        payload = {"block_height": height}
        return await self.call("getblockhash", payload)

    async def getblockheight(self, blockhash: str):
        payload = {"block_hash": blockhash}
        return await self.call("getblockheight", payload)

    async def estimatefee(self, blocks: int):
        payload = {"blocks": blocks}
        return await self.call("estimatefee", payload)

    async def sendrawtransaction(self, rawtx: str):
        payload = {"rawtx": rawtx}
        return await self.call("sendrawtransaction", payload)

    @property
    def available(self) -> bool:
        return True