"""
Author: wind windzu1@gmail.com
Date: 2023-11-03 14:25:39
LastEditors: wind windzu1@gmail.com
LastEditTime: 2023-11-03 14:34:33
Description: 
Copyright (c) 2023 by windzu, All Rights Reserved. 
"""

import os
from argparse import ArgumentParser

from .hack import hack_nuscenes


def add_arguments(parser):
    """
    为子命令 `hack` 添加参数。

    参数:
        subparser (argparse.ArgumentParser): 子命令对应的 parser，由 `add_parser("hack")` 创建
    """
    # parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "--nuscenes-dataset-path",
        type=str,
        required=True,
        help="(required) nuscenes数据集路径",
    )
    parser.add_argument(
        "--conda-env-name",
        type=str,
        required=False,
        help="指定需要替换的conda环境名称,如果不指定，则使用当前环境",
    )
    parser.add_argument(
        "--lidar-channel",
        type=str,
        required=False,
        help="指定使用的激光雷达通道名称，如果不指定，则不替换",
    )
    parser.add_argument(
        "--camera-channels",
        type=str,
        required=False,
        help="指定相机通道，多个通道用逗号分隔，如果不指定，则不替换",
    )
    parser.add_argument(
        "--pcd-dims",
        type=int,
        required=False,
        help="指定点云的维度，如果不指定，则不替换",
    )
    # 设置main函数为默认处理函数
    parser.set_defaults(func=run)


def run(args, unknown_args=None):
    """
    主函数，执行hack操作

    Args:
        args: 解析后的已知参数
        unknown_args: 解析后的未知参数
    """
    # 获取并处理参数
    nuscenes_path = args.nuscenes_dataset_path
    conda_env_name = args.conda_env_name
    lidar_channel_name = args.lidar_channel
    camera_channels = []
    if args.camera_channels:
        camera_channels = args.camera_channels.split(",")
    pcd_dims = args.pcd_dims

    # 检查路径是否存在
    if not os.path.exists(nuscenes_path):
        print(f"错误: NuScenes数据集路径不存在: {nuscenes_path}")
        return

    # 调用hack_nuscenes函数
    hack_nuscenes(
        nuscenes_path=nuscenes_path,
        conda_env_name=conda_env_name,
        pcd_dims=pcd_dims,
        lidar_channel_name=lidar_channel_name,
        camera_channels=camera_channels,
    )
