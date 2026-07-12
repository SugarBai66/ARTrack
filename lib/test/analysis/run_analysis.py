import argparse
from lib.test.evaluation.datasets import get_dataset
from lib.test.evaluation.tracker import Tracker
from lib.test.analysis.plot_results import plot_results, print_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='got10k_test',
                        help='Dataset name, e.g., got10k_test, got10k_val')
    parser.add_argument('--tracker_name', type=str, default='artrack')
    parser.add_argument('--parameter_name', type=str, default='artrack_256_got')
    parser.add_argument('--run_id', type=int, default=None,
                        help='Run ID if multiple runs exist, otherwise None')
    parser.add_argument('--display_name', type=str, default='ARTrack')
    parser.add_argument('--report_name', type=str, default='ARTrack_got10k_analysis')
    args = parser.parse_args()

    # 加载数据集（会自动读取 got10k_path 下的标注）
    dataset = get_dataset(args.dataset)

    # 构造 Tracker 对象（无需指定 results_dir）
    tracker = Tracker(
        name=args.tracker_name,
        parameter_name=args.parameter_name,
        dataset_name=args.dataset,   # 必须传入，尽管不用于路径
        run_id=args.run_id,
        display_name=args.display_name,
    )
    # 若您的参数有多个运行，可以修改 run_id，但这里用 None

    trackers = [tracker]

    # 绘图（生成 PDF 和 TEX 文件）
    plot_results(
        trackers=trackers,
        dataset=dataset,
        report_name=args.report_name,
        merge_results=False,
        plot_types=('success', 'prec', 'norm_prec'),
        force_evaluation=False,     # 若设为 True 会重新计算（忽略缓存）
    )

    # 打印数值报表
    print_results(
        trackers=trackers,
        dataset=dataset,
        report_name=args.report_name,
        plot_types=('success', 'prec', 'norm_prec'),
    )

if __name__ == '__main__':
    main()