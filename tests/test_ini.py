# -*- coding: utf-8 -*-
"""
@Time ： 2024/12/14 15:14
@Auth ： Jin Lyu
@File ：test_ini.py
@IDE ：PyCharm
@Describe：...
"""
from pathlib import Path

import pytest

from pytest_result_sender_lj import plugin

pytest_plugins = "pytester"  # 我是测试开发


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {"passed": 0, "failed": 0}
    # 创建一个干净的测试环境
    yield

    # 恢复测试环境
    plugin.data = bak_data


@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = {send_when}
send_api = https://open.feishu.cn/open-apis/bot/v2/hook/65223bdb-adda-402e-a2f9-9c5d77b3f6c9
        """
    )
    # 断言：配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when

    pytester.makepyfile(  # 构造场景，用例全部测试通过
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))
    # 如何断言，插件到底有没有发送结果
    print(plugin.data)
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize(
    "send_api",
    [
        "www.baidu.com",
        "https://open.feishu.cn/open-apis/bot/v2/hook/65223bdb-adda-402e-a2f9-9c5d77b3f6c9",
        "",
    ],
)
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = every
send_api = {send_api}
            """
    )
    # 断言：配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_api") == send_api

    pytester.makepyfile(  # 构造场景，用例全部测试通过
        """
        def test_pass():
            ...
        """
    )
    pytester.runpytest("-c", str(config_path))
    # 如何断言，插件到底有没有发送结果
    print(plugin.data)
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
