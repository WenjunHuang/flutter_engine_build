# 编译和hack flutter engine
# 准备工作
1. 按需设置好你的代理(以下假设为http://127.0.0.1:9798)
1. 安装python3
1. 打开powershell(windows下)或者terminal(macos或linux)

# flutter engine编译
1. git clone --recurse-submodules https://github.com/wenjunhuang/FlutterEngineBuild.git
2. 编辑gclientconfig文件，将里面的"https://github.com/wenjunhuang/engine.git"改为你自己的fork或者flutter engine的地址
3. 如果你用的是windows，并且需要设置代理，那么修改depot_tools_proxy.patch文件
将```+  $proxy.Address = "http://127.0.0.1:9798"```里面的地址改为你的代理地址并保存。然后
cd depot_tools 并且执行 git apply ..\depot_tools_proxy.patch
4. 如果需要设置代理，请将fetch-engine.py和build.py里面的env['HTTP_PROXY']和env['HTTPS_PROXY']部分改为你的代理，否则请把他们删掉
5. 执行python fetch-engine.py
6. 执行python build.py
7. 使用支持CMake的IDE打开本目录（推荐CLion），IDE可以识别几乎所有flutter engine的c++代码，但是不能编译
8. 执行python watcher.py
9. 修改engine的代码，会自动编译并运行单元测试（在watcher.py脚本里面设置）