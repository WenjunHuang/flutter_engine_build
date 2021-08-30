# Windows 10下编译flutter engine
# 准备工作
1. 设置好你的代理，以下假设为http://127.0.0.1:9798
2. 打开powershell
3. 执行命令
$env:HTTP_PROXY="http://127.0.0.1:9798"
$env:HTTPS_PROXY="http://127.0.0.1:9798"

# flutter engine编译
1. git clone --recurse-submodules https://github.com/wenjunhuang/FlutterEngineBuild.git
1. 修改depot_tools_proxy.patch文件
将```+  $proxy.Address = "http://127.0.0.1:9798"```里面的地址改为你的代理地址，然后保存
1. x
1. cd depot_tools 并且执行 git apply ..\depot_tools_proxy.patch
1. 执行fetch-engine.py
1. 执行build.py