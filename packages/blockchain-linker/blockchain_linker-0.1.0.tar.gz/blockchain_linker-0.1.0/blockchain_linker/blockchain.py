import hashlib
import json
import time
from typing import Any, Dict, List, Optional

class Block:
    def __init__(self, index: int, data: Dict[str, Any], previous_hash: str, timestamp: Optional[float] = None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]

    def create_genesis_block(self) -> Block:
        return Block(0, {'genesis': True}, '0')

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            data=data,
            previous_hash=last_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.hash != current.calculate_hash():
                return False
        return True

    def to_list(self) -> List[Dict[str, Any]]:
        return [block.to_dict() for block in self.chain]

    def save(self, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(self.to_list(), f, indent=2)

    @classmethod
    def load(cls, filename: str) -> 'Blockchain':
        with open(filename, 'r') as f:
            chain_data = json.load(f)
        blockchain = cls()
        blockchain.chain = []
        for block_data in chain_data:
            block = Block(
                index=block_data['index'],
                data=block_data['data'],
                previous_hash=block_data['previous_hash'],
                timestamp=block_data['timestamp']
            )
            block.hash = block_data['hash']
            blockchain.chain.append(block)
        return blockchain

    def __len__(self):
        return len(self.chain)

    def __getitem__(self, idx):
        return self.chain[idx]

    def modify_block_data(self, index: int, new_data: Dict[str, Any]) -> bool:
        """
        블록체인에서 특정 인덱스의 블록 데이터를 수정하고, 이후 블록들의 해시와 previous_hash를 재계산합니다.
        :param index: 수정할 블록의 인덱스
        :param new_data: 새로운 데이터 (dict)
        :return: 성공 여부 (bool)
        """
        if index == 0 or index >= len(self.chain):
            # 제네시스 블록은 수정 불가, 인덱스 범위 체크
            return False
        self.chain[index].data = new_data
        self.chain[index].hash = self.chain[index].calculate_hash()
        # 이후 블록들의 previous_hash, hash 재계산
        for i in range(index + 1, len(self.chain)):
            self.chain[i].previous_hash = self.chain[i - 1].hash
            self.chain[i].hash = self.chain[i].calculate_hash()
        return True

def make_blockchain(user_list: List[Dict[str, Any]]) -> Blockchain:
    bc = Blockchain()
    for user in user_list:
        bc.add_block(user)
    return bc 