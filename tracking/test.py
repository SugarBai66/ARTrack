import os
import sys
import argparse

# 将项目根目录（ARTrack/）加入 sys.path，确保后续能正确导入 lib 包下的模块。
prj_path = os.path.join(os.path.dirname(__file__), '..')
if prj_path not in sys.path:
    sys.path.append(prj_path)

# get_dataset：根据名称加载对应的测试数据集（如 OTB、GOT-10k、LaSOT 等）
# run_dataset：在数据集上运行跟踪器（支持多线程、多GPU并行）
# Tracker：封装跟踪器模型、配置和参数
from lib.test.evaluation import get_dataset
from lib.test.evaluation.running import run_dataset
from lib.test.evaluation.tracker import Tracker

#@Param: tracker_name: 跟踪器名称
#@Param: tracker_param: 跟踪器参数文件名称
#@Param: run_id: 运行ID（可选）
#@Param: dataset_name: 数据集名称（默认 'otb'）
#@Param: sequence: 指定序列名称或编号（可选）
#@Param: debug: 调试级别（默认 0）
#@Param: threads: 使用的线程数（默认 0，表示自动选择）
#@Param: num_gpus: 使用的GPU数量（默认 8）
def run_tracker(tracker_name, tracker_param, run_id=None, dataset_name='otb', sequence=None, debug=0, threads=0,
                num_gpus=8):
    """Run tracker on sequence or dataset.
    args:
        tracker_name: Name of tracking method.
        tracker_param: Name of parameter file.
        run_id: The run id.
        dataset_name: Name of dataset (otb, nfs, uav, tpl, vot, tn, gott, gotv, lasot).
        sequence: Sequence number or name.
        debug: Debug level.
        threads: Number of threads.
    """

    dataset = get_dataset(dataset_name)

    if sequence is not None:
        dataset = [dataset[sequence]]

    trackers = [Tracker(tracker_name, tracker_param, dataset_name, run_id)]

    run_dataset(dataset, trackers, debug, threads, num_gpus=num_gpus)

#@Param: tracker_name: 跟踪器名称
#@Param: tracker_param: 跟踪器参数文件名称
#@Param: runid: 运行ID（可选）
#@Param: dataset_name: 数据集名称（默认 'otb'）
#@Param: sequence: 指定序列名称或编号（可选）
#@Param: debug: 调试级别（默认 0）
#@Param: threads: 使用的线程数（默认 0，表示自动选择）
#@Param: num_gpus: 使用的GPU数量（默认 8）
def main():
    parser = argparse.ArgumentParser(description='Run tracker on sequence or dataset.')
    parser.add_argument('tracker_name', type=str, help='Name of tracking method.')
    parser.add_argument('tracker_param', type=str, help='Name of config file.')
    parser.add_argument('--runid', type=int, default=None, help='The run id.')
    parser.add_argument('--dataset_name', type=str, default='otb', help='Name of dataset (otb, nfs, uav, tpl, vot, tn, gott, gotv, lasot).')
    parser.add_argument('--sequence', type=str, default=None, help='Sequence number or name.')
    parser.add_argument('--debug', type=int, default=0, help='Debug level.')
    parser.add_argument('--threads', type=int, default=0, help='Number of threads.')
    parser.add_argument('--num_gpus', type=int, default=8)

    args = parser.parse_args()

    try:
        seq_name = int(args.sequence)
    except:
        seq_name = args.sequence

    run_tracker(args.tracker_name, args.tracker_param, args.runid, args.dataset_name, seq_name, args.debug,
                args.threads, num_gpus=args.num_gpus)


if __name__ == '__main__':
    main()
