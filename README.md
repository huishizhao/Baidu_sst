此项目为 [Home Assistant](https://www.home-assistant.io/) 的[百度STT](https://ai.baidu.com/tech/speech/)插件。

## 功能
百度AI语音转文字服务。

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## 使用
  1. 注册百度云账号
  2. 创建应用, 会得到AppID，API Key 和 Secret Key
  3. 开通语音识别，目前只有两种语言可以选择
  
     |   语言    |     计费方式     |
     |----------:|------------------|
     | 中文普通话| 无限制，按量计费 |
     |  英语     | 无限制，按量计费 |

  4. 下载或者 clone 此项目, 将 custom\_components/baidu_stt 目录拷贝至 Home Assistant 配置目录的 custom\_components 目录下。
  5. 重启 Home Assistant 服务。
  6. 在 Home Assistant 的集成页面，搜索 "baidu_stt" 并添加。
  7. 根据提示输入AppID，API Key 和 Secret Key。
  8. 在Homeassistant 的-设置-语音助理-语音转文字中选择 BaiduStt, 语言选择 普通话