import warnings

warnings.filterwarnings("ignore")
import sys
from pathlib import Path
import os
import torch

ROOT = str(Path(__file__).resolve().parents[2])
sys.path.append(ROOT)

import argparse
import os.path as osp
from mmcv import Config
from trademaster.utils import replace_cfg_vals
from trademaster.datasets.builder import build_dataset
from trademaster.trainers.builder import build_trainer


def parse_args():
    parser = argparse.ArgumentParser(description='Download Alpaca Datasets')
    parser.add_argument("--config", default=osp.join(ROOT, "configs", "portfolio_management", "sarl_dj30.py"),
                        help="download datasets config file path")
    parser.add_argument("--task_name", type=str, default="train")
    args = parser.parse_args()
    return args


def test_deeptrader():
    args = parse_args()

    cfg = Config.fromfile(args.config)
    task_name = args.task_name

    cfg = replace_cfg_vals(cfg)
    print(cfg)

    dataset = build_dataset(cfg)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    work_dir = os.path.join(ROOT, cfg.trainer.work_dir)

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    cfg.dump(osp.join(work_dir, osp.basename(args.config)))

    trainer = build_trainer(cfg, default_args=dict(dataset=dataset, device = device))

    if task_name.startswith("train"):
        trainer.train_and_valid()
    elif task_name.startswith("test"):
        trainer.test()


if __name__ == '__main__':
    test_deeptrader()
    """
    algorithmic_trading
    portfolio_management
    """