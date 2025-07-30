# -*- coding: utf-8 -*-
import os
from functools import lru_cache

import yaml

from jarvis.jarvis_utils.builtin_replace_map import BUILTIN_REPLACE_MAP

"""配置管理模块。

该模块提供了获取Jarvis系统各种配置设置的函数。
所有配置都从环境变量中读取，带有回退默认值。
"""

def get_git_commit_prompt() -> str:
    """
    获取Git提交提示模板
    
    返回:
        str: Git提交信息生成提示模板，如果未配置则返回空字符串
    """
    return os.getenv("JARVIS_GIT_COMMIT_PROMPT", "")

# 输出窗口预留大小
INPUT_WINDOW_REVERSE_SIZE = 2048

@lru_cache(maxsize=None)
def get_replace_map() -> dict:
    """
    获取替换映射表。
    
    从数据目录下的replace_map.yaml文件中读取替换映射表，
    如果文件不存在则返回内置替换映射表。
    
    返回:
        dict: 合并后的替换映射表字典(内置+文件中的映射表)
    """
    replace_map_path = os.path.join(get_data_dir(), 'replace_map.yaml')
    if not os.path.exists(replace_map_path):
        return BUILTIN_REPLACE_MAP.copy()
    
    with open(replace_map_path, 'r', encoding='utf-8', errors='ignore') as file:
        file_map = yaml.safe_load(file) or {}
        return {**BUILTIN_REPLACE_MAP, **file_map}

def get_max_token_count() -> int:
    """
    获取模型允许的最大token数量。

    返回:
        int: 模型能处理的最大token数量。
    """
    return int(os.getenv('JARVIS_MAX_TOKEN_COUNT', '960000'))

def get_max_input_token_count() -> int:
    """
    获取模型允许的最大输入token数量。

    返回:
        int: 模型能处理的最大输入token数量。
    """
    return int(os.getenv('JARVIS_MAX_INPUT_TOKEN_COUNT', '32000'))


def is_auto_complete() -> bool:
    """
    检查是否启用了自动补全功能。

    返回：
        bool: 如果启用了自动补全则返回True，默认为False
    """
    return os.getenv('JARVIS_AUTO_COMPLETE', 'false') == 'true'


def get_shell_name() -> str:
    """
    获取系统shell名称。

    返回：
        str: Shell名称（例如bash, zsh），默认为bash
    """
    shell_path = os.getenv('SHELL', '/bin/bash')
    return os.path.basename(shell_path)
def get_normal_platform_name() -> str:
    """
    获取正常操作的平台名称。

    返回：
        str: 平台名称，默认为'yuanbao'
    """
    return os.getenv('JARVIS_PLATFORM', 'yuanbao')
def get_normal_model_name() -> str:
    """
    获取正常操作的模型名称。

    返回：
        str: 模型名称，默认为'deep_seek'
    """
    return os.getenv('JARVIS_MODEL', 'deep_seek_v3')


def get_thinking_platform_name() -> str:
    """
    获取思考操作的平台名称。

    返回：
        str: 平台名称，默认为'yuanbao'
    """
    return os.getenv('JARVIS_THINKING_PLATFORM', os.getenv('JARVIS_PLATFORM', 'yuanbao'))
def get_thinking_model_name() -> str:
    """
    获取思考操作的模型名称。

    返回：
        str: 模型名称，默认为'deep_seek'
    """
    return os.getenv('JARVIS_THINKING_MODEL', os.getenv('JARVIS_MODEL', 'deep_seek'))

def is_execute_tool_confirm() -> bool:
    """
    检查工具执行是否需要确认。

    返回：
        bool: 如果需要确认则返回True，默认为False
    """
    return os.getenv('JARVIS_EXECUTE_TOOL_CONFIRM', 'false') == 'true'
def is_confirm_before_apply_patch() -> bool:
    """
    检查应用补丁前是否需要确认。

    返回：
        bool: 如果需要确认则返回True，默认为False
    """
    return os.getenv('JARVIS_CONFIRM_BEFORE_APPLY_PATCH', 'true') == 'true'

def get_max_tool_call_count() -> int:
    """
    获取最大工具调用次数。

    返回：
        int: 最大连续工具调用次数，默认为20
    """
    return int(os.getenv('JARVIS_MAX_TOOL_CALL_COUNT', '20'))


def get_data_dir() -> str:
    """
    获取Jarvis数据存储目录路径。
    
    返回:
        str: 数据目录路径，优先从JARVIS_DATA_PATH环境变量获取，
             如果未设置或为空，则使用~/.jarvis作为默认值
    """
    data_path = os.getenv('JARVIS_DATA_PATH', '').strip()
    if not data_path:
        return os.path.expanduser('~/.jarvis')
    return data_path

def get_auto_update() -> bool:
    """
    获取是否自动更新git仓库。

    返回：
        bool: 如果需要自动更新则返回True，默认为True
    """
    return os.getenv('JARVIS_AUTO_UPDATE', 'true') == 'true'

def get_max_big_content_size() -> int:
    """
    获取最大大内容大小。

    返回：
        int: 最大大内容大小
    """
    return int(os.getenv('JARVIS_MAX_BIG_CONTENT_SIZE', '1024000'))

def get_pretty_output() -> bool:
    """
    获取是否启用PrettyOutput。

    返回：
        bool: 如果启用PrettyOutput则返回True，默认为True
    """
    return os.getenv('JARVIS_PRETTY_OUTPUT', 'false') == 'true'

def is_use_methodology() -> bool:
    """
    获取是否启用方法论。

    返回：
        bool: 如果启用方法论则返回True，默认为True
    """
    return os.getenv('JARVIS_USE_METHODOLOGY', 'false') == 'true'

def is_use_analysis() -> bool:
    """
    获取是否启用任务分析。

    返回：
        bool: 如果启用任务分析则返回True，默认为True
    """
    return os.getenv('JARVIS_USE_ANALYSIS', 'false') == 'true'

def is_print_prompt() -> bool:
    """
    获取是否打印提示。

    返回：
        bool: 如果打印提示则返回True，默认为True
    """
    return os.getenv('JARVIS_PRINT_PROMPT', 'false') == 'true'