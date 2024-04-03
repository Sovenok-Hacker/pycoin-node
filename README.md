# PyCoin

## Running
Build gRPC protocol:
```bash
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. protocol/node.proto
```
Run node:
```bash
python3 main.py
```