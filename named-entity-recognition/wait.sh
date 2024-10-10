#!/bin/bash

# 检查是否提供了 PID 参数
if [ -z "$1" ]; then
  echo "使用方法: $0 <PID>"
  exit 1
fi

# 从命令行参数获取目标进程的PID
TARGET_PID=$1


# 循环检查进程是否存在
while kill -0 $TARGET_PID 2> /dev/null; do
  echo "等待进程 $TARGET_PID 结束..."
  sleep 60  # 每秒钟检查一次
done

# 进程结束后运行的命令
echo "进程 $TARGET_PID 已结束，开始运行新命令"
sourec activate python3_11_gpu
python use_model_recognize_entity.py

