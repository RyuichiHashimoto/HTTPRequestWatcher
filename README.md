# HTTP Request Wacher
![python](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## 目次


## 
HTTP Requestのheaderやbodyに付与されている情報を把握するための簡易サイト。

主に下記２つの機能を有する。
- HTTP Requestを叩いたときに付与されるheaderやbody情報を収集する。
  - API名：/register/<session_id>
  
- 収集したheaderやbody情報を閲覧する。
  - API名： /show/<session_id>

<session_id>は英数のみ許可されている。

## API種別
### 前提知識
<.>

### /register/<session_id>


ローカルでも展開できるが、