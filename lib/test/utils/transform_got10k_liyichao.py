import numpy as np
import os
import shutil
import argparse
import _init_paths
from lib.test.evaluation.environment import env_settings


def transform_got10k(src_dir, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    items = os.listdir(src_dir)
    for item in items:
        if "all" in item:
            continue
        src_path = os.path.join(src_dir, item)
        if "time" not in item:
            seq_name = item.replace(".txt", '')
            seq_dir = os.path.join(dest_dir, seq_name)
            if not os.path.exists(seq_dir):
                os.makedirs(seq_dir)
            new_item = item.replace(".txt", '_001.txt')
            dest_path = os.path.join(seq_dir, new_item)
            # bbox_arr = np.loadtxt(src_path, dtype=np.int32, delimiter='\t')
            # `np.int` was a deprecated alias for the builtin `int`. To avoid this error in existing code, use `int` by itself.
            bbox_arr = np.loadtxt(src_path, dtype=int, delimiter='\t')
            np.savetxt(dest_path, bbox_arr, fmt='%d', delimiter=',')
        else:
            seq_name = item.replace("_time.txt", '')
            seq_dir = os.path.join(dest_dir, seq_name)
            if not os.path.exists(seq_dir):
                os.makedirs(seq_dir)
            dest_path = os.path.join(seq_dir, item)
            os.system("cp %s %s" % (src_path, dest_path))
    # make zip archive
    shutil.make_archive(src_dir, "zip", src_dir)
    shutil.make_archive(dest_dir, "zip", dest_dir)
    # Remove the original files
    # shutil.rmtree(src_dir)
    shutil.rmtree(dest_dir)


if __name__ == "__main__":
    for num in range(270,290):
    # for num in [290]:
        import glob

        parser = argparse.ArgumentParser(description='transform got10k results.')
        parser.add_argument('--tracker_name', type=str, default='litetrack', help='Name of tracking method.')
        parser.add_argument('--cfg_name', type=str, default='B9_cae_center_all_ep300', help='Name of config file.')

        args = parser.parse_args()
        tracker_name = args.tracker_name
        cfg_name = args.cfg_name
        env = env_settings()
        result_dir = env.results_path
        # num = 250
        # src_dir = os.path.join(result_dir, "%s/%s/got10k_%s/" % (tracker_name, cfg_name, num))
        src_dir = os.path.join(result_dir, "%s/%s/litetrack-Token+Soft/got10k_test/got10k_%s/" % (tracker_name, cfg_name, num))
        dest_dir = os.path.join(result_dir, "%s/%s/litetrack-Token+Soft/got10k_test/got10k_submit_%s/" % (tracker_name, cfg_name, num))
        #
        # listglob = glob.glob(src_dir)
        # listglob.sort()
        # src_list = listglob
        # dst_list = [ os.path.join(result_dir, "%s/%s/got10k/"
        #          % (tracker_name, path.split('/')[-3])) for path in listglob]
        # for i in range(len(src_list)):
        #     transform_got10k(src_list[i], dst_list[i])
        transform_got10k(src_dir, dest_dir)
        # transform_got10k(args.tracker_name, args.cfg_name) for

