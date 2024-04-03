import grpc
import concurrent.futures as pool
from protocol import node_pb2, node_pb2_grpc

from blockchain import Block, Transaction, Address
from utils import timestamp

chain = [
    Block(
        index=0,
        timestamp=timestamp(),
        phash=b'',
        txs=[],
        miner=Address.from_int(0),
        pow=0,
        diff=0
    )
]

class NodeService(node_pb2_grpc.NodeServicer):
    def Ping(self, request, context):
        return node_pb2.PingResponse(time=timestamp())
    def GetHeight(self, request, context):
        return node_pb2.HeightResponse(height=len(chain))
    def GetLastBlock(self, request, context):
        lb = chain[-1]
        return node_pb2.Block(
            index=lb.index,
            timestamp=lb.timestamp,
            hash=lb.hash,
            phash=lb.phash,
            txs=[node_pb2.Transaction(
                sender=tx.sender.to_bytes(),
                receiver=tx.receiver.to_bytes(),
                amount=tx.amount,
                data=tx.data,
                nonce=tx.nonce,
                signature=tx.signature
            ) for tx in lb.txs],
            miner=lb.miner.to_bytes(),
            pow=lb.pow,
            diff=lb.diff
        )
    def GetBlockByIndex(self, request, context):
        if request.index > chain[-1].index:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Invalid block index, #{chain[-1].index} is the last block")
            return node_pb2.Block()
        b = chain[request.index]
        return node_pb2.Block(
            index=b.index,
            timestamp=b.timestamp,
            hash=b.hash,
            phash=b.phash,
            txs=[node_pb2.Transaction(
                sender=tx.sender.to_bytes(),
                receiver=tx.receiver.to_bytes(),
                amount=tx.amount,
                data=tx.data,
                nonce=tx.nonce,
                signature=tx.signature
            ) for tx in b.txs],
            miner=b.miner.to_bytes(),
            pow=b.pow,
            diff=b.diff
        )

if __name__ == '__main__':
    server = grpc.server(thread_pool=pool.ThreadPoolExecutor(max_workers=10))
    node_pb2_grpc.add_NodeServicer_to_server(NodeService(), server)
    server.add_insecure_port("localhost:50051")
    server.start()
    server.wait_for_termination()