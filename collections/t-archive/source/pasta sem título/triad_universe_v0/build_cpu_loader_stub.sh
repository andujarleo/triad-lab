#!/usr/bin/env bash
set -euo pipefail
cc -shared -fPIC -O2 "$(dirname "$0")/linux_cuda_stub.c" -o "$(dirname "$0")/libtriad_cuda_stub.so"
