#!/bin/sh
pip install -e ".[api]" -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
cd lightrag_webui
bun install --frozen-lockfile
bun run build
cd ..
