# pytest-result-sender-lj

## 功能说明
* 用例执行完，自动发送消息的插件，可配置：
  * 发送时机：send_when（on_fail：当执行完有失败case才发送；every：每次执行结束都发送）
  * 发送地址：send_api（发送地址为
  * 测试报告地址：report_dir

配置文件：pytest.ini

## pytest.ini文件示例
```
[pytest]
# 什么时候发送
send_when = on_fail

# 发送到哪里
send_api = https://open.feishu.cn/open-apis/bot/v2/hook/65223bdb-adda-402e-a2f9-9c5d77b3f6c9

# 报告地址
report_dir = https://www.baidu.com123
```