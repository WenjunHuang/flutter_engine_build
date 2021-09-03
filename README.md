# Windows 10下编译和hack flutter engine
# 准备工作
1. 设置好你的代理，以下假设为http://127.0.0.1:9798
2. 打开powershell
3. 执行命令
$env:HTTP_PROXY="http://127.0.0.1:9798"
$env:HTTPS_PROXY="http://127.0.0.1:9798"

# flutter engine编译
1. git clone --recurse-submodules https://github.com/wenjunhuang/FlutterEngineBuild.git
2. 修改depot_tools_proxy.patch文件
将```+  $proxy.Address = "http://127.0.0.1:9798"```里面的地址改为你的代理地址，然后保存
3. cd depot_tools 并且执行 git apply ..\depot_tools_proxy.patch
4. 执行fetch-engine.py
5. 执行build.py
6. 使用管理员权限打开控制台cd "你的目录"\engine\src\out 执行mklink /J host_debug_unopt .\win_debug_unopt\
7. 使用visual studio 2019打开\win_debug_unopt\all.sln或者使用Clion打开本目录
8. 执行python watcher.py
9. 修改engine的代码，会自动编译并运行单元测试（在watcher.py脚本里面设置）