# ROCm 7.2 在 WSL2 上的完整安装教程

**适用环境：Windows 11 + WSL2 + Ubuntu 24.04 + AMD RX 7700 XT**

本教程将引导你在 Windows Subsystem for Linux 2 (WSL2) 上安装 AMD ROCm 7.2 和 PyTorch，以便在 AMD 显卡上进行机器学习开发。

---

## 目录

1. [系统要求检查](#1-系统要求检查)
2. [安装 WSL2](#2-安装-wsl2)
3. [安装 AMD Adrenalin Edition 驱动](#3-安装-amd-adrenalin-edition-驱动)
4. [安装 ROCm for WSL2](#4-安装-rocm-for-wsl2)
5. [安装 Conda 和创建 Python 环境](#5-安装-conda-和创建-python-环境)
6. [安装 PyTorch for ROCm](#6-安装-pytorch-for-rocm)
7. [验证安装](#7-验证安装)
8. [故障排除](#8-故障排除)

---

## 1. 系统要求检查

### 1.1 确认系统版本

在安装前，请确认你的系统满足以下要求：

- **操作系统**：Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11
- **显卡型号**：
  - AMD Radeon RX 9000 系列（9070/9060 等）
  - AMD Radeon RX 7000 系列（7900 XTX/7900 XT/7900 GRE/7800 XT/7700 XT/7700 等）
  - AMD Radeon PRO W7000 系列
- **WSL 版本**：WSL 2
- **Linux 发行版**：Ubuntu 22.04 或 Ubuntu 24.04

### 1.2 检查 Windows 版本

1. 按 `Win + R`，输入 `winver`，按回车
2. 确认版本号满足要求

### 1.3 检查显卡型号

1. 按 `Win + R`，输入 `dxdiag`，按回车
2. 切换到"显示"选项卡
3. 确认显卡型号为支持的 AMD 显卡

### 1.4 兼容性参考

根据 ROCm 7.2 官方兼容性矩阵：

| 项目 | 支持版本 |
|------|---------|
| Ubuntu | 22.04 或 24.04.2 Desktop (HWE) |
| WSL 内核 | 5.15 |
| ROCm | 7.2 |
| Windows 驱动 | Adrenalin Edition 26.1.1 |
| PyTorch | 2.9.1 + ROCm 7.2 |
| Python | 3.10 (Ubuntu 22.04) 或 3.12 (Ubuntu 24.04) |

---

## 2. 安装 WSL2

### 2.1 启用 WSL

如果你还没有安装 WSL2，请按照以下步骤操作：

1. **以管理员身份打开 PowerShell**
   - 右键点击开始菜单
   - 选择"Windows PowerShell (管理员)"或"终端 (管理员)"

2. **执行安装命令**
   ```powershell
   wsl --install
   ```

3. **重启计算机**
   - 安装完成后，系统会提示重启
   - 重启后继续下一步

### 2.2 安装 Ubuntu

安装完 WSL2 后，默认会安装 Ubuntu。如果需要指定版本：

```powershell
# 查看可用的 Linux 发行版
wsl --list --online

# 安装 Ubuntu 24.04
wsl --install -d Ubuntu-24.04

# 或安装 Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

### 2.3 设置 Ubuntu 用户

首次启动 Ubuntu 时：
1. 系统会要求创建用户名和密码
2. 输入用户名（建议使用小写字母）
3. 输入并确认密码

### 2.4 验证 WSL 版本

在 PowerShell 中运行：
```powershell
wsl --list --verbose
```

确认输出显示 VERSION 为 2：
```
  NAME            STATE           VERSION
* Ubuntu-24.04    Running         2
```

如果显示的是 VERSION 1，请升级到 WSL 2：
```powershell
wsl --set-version Ubuntu-24.04 2
```

### 2.5 更新 WSL 内核（如需要）

```powershell
wsl --update
```

---

## 3. 安装 AMD Adrenalin Edition 驱动

### 3.1 下载驱动

ROCm 7.2 需要 **AMD Software: Adrenalin Edition 26.1.1** 驱动。

1. 访问 AMD 官方驱动下载页面：
   [https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-1-1.html](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-1-1.html)

2. 点击下载链接：
   - **AMD Software: Adrenalin Edition 26.1.1 Driver**

### 3.2 安装驱动

1. 运行下载的安装程序
2. 选择"快速安装"或"自定义安装"
   - 快速安装：推荐给大多数用户
   - 自定义安装：可以选择安装组件
3. 等待安装完成

### 3.3 重启电脑

**重要**：安装驱动后，**必须重启计算机**才能生效。

### 3.4 验证驱动安装

重启后，确认驱动已正确安装：
1. 右键点击桌面空白处
2. 选择"AMD Software: Adrenalin Edition"
3. 查看驱动版本是否为 26.1.1

---

## 4. 安装 ROCm for WSL2

### 4.1 打开 WSL Ubuntu 终端

1. 在 Windows 开始菜单搜索"Ubuntu"
2. 点击打开 Ubuntu 终端

### 4.2 更新系统包

```bash
sudo apt update
```

### 4.3 下载并安装 ROCm 安装脚本

根据你的 Ubuntu 版本选择对应的命令：

#### Ubuntu 24.04

```bash
# 下载安装脚本
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/noble/amdgpu-install_7.2.70200-1_all.deb

# 安装脚本
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
```

#### Ubuntu 22.04

```bash
# 下载安装脚本
wget https://repo.radeon.com/amdgpu-install/7.2/ubuntu/jammy/amdgpu-install_7.2.70200-1_all.deb

# 安装脚本
sudo apt install ./amdgpu-install_7.2.70200-1_all.deb
```

### 4.4 安装 ROCm

使用 `amdgpu-install` 脚本安装 ROCm：

```bash
sudo amdgpu-install -y --usecase=wsl,rocm --no-dkms
```

**参数说明**：
- `-y`：自动确认，无需手动确认
- `--usecase=wsl,rocm`：安装 WSL 用例和 ROCm
- `--no-dkms`：不安装内核模块（WSL 不需要）

**注意**：此过程可能需要几分钟时间，具体取决于网络速度。

### 4.5 验证 ROCm 安装

安装完成后，运行以下命令验证：

```bash
rocminfo
```

**预期输出**：
```
*******
Agent 2
*******
  Name:                    gfx1100
  Marketing Name:          Radeon RX 7700 XT
  Vendor Name:             AMD
  [...]
```

如果看到你的显卡信息（如 Radeon RX 7700 XT），说明 ROCm 安装成功。

---

## 5. 安装 Conda 和创建 Python 环境

### 5.1 下载 Miniconda

推荐使用 Miniconda 来管理 Python 环境：

```bash
# 下载 Miniconda 安装脚本
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 运行安装脚本
bash Miniconda3-latest-Linux-x86_64.sh
```

### 5.2 安装过程

1. 按 `Enter` 查看许可协议
2. 输入 `yes` 接受许可
3. 按 `Enter` 确认安装位置（默认为 `~/miniconda3`）
4. 输入 `yes` 初始化 Miniconda

### 5.3 激活 Conda

```bash
# 关闭并重新打开终端，或运行
source ~/.bashrc

# 验证 Conda 安装
conda --version
```

### 5.4 创建 Python 环境

根据你的 Ubuntu 版本创建对应的 Python 环境：

#### Ubuntu 24.04 - Python 3.12

```bash
# 创建名为 rocm 的环境，Python 版本为 3.12
conda create -n rocm python=3.12 -y

# 激活环境
conda activate rocm
```

#### Ubuntu 22.04 - Python 3.10

```bash
# 创建名为 rocm 的环境，Python 版本为 3.10
conda create -n rocm python=3.10 -y

# 激活环境
conda activate rocm
```

**提示**：以后每次使用 PyTorch 时，都需要先激活此环境：
```bash
conda activate rocm
```

---

## 6. 安装 PyTorch for ROCm

### 6.1 安装基础依赖

```bash
# 安装 pip
sudo apt install python3-pip -y

# 更新 pip
pip3 install --upgrade pip wheel
```

### 6.2 下载 PyTorch Wheel 文件

根据你的 Ubuntu 版本和 Python 版本下载对应的 wheel 文件：

#### Ubuntu 24.04 (Python 3.12)

```bash
# 下载 PyTorch 和相关库
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torch-2.9.1%2Brocm7.2.0.lw.git7e1940d4-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchvision-0.24.0%2Brocm7.2.0.gitb919bd0c-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/triton-3.5.1%2Brocm7.2.0.gita272dfa8-cp312-cp312-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchaudio-2.9.0%2Brocm7.2.0.gite3c6ee2b-cp312-cp312-linux_x86_64.whl
```

#### Ubuntu 22.04 (Python 3.10)

```bash
# 下载 PyTorch 和相关库
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torch-2.9.1%2Brocm7.2.0.lw.git7e1940d4-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchvision-0.24.0%2Brocm7.2.0.gitb919bd0c-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/triton-3.5.1%2Brocm7.2.0.gita272dfa8-cp310-cp310-linux_x86_64.whl
wget https://repo.radeon.com/rocm/manylinux/rocm-rel-7.2/torchaudio-2.9.0%2Brocm7.2.0.gite3c6ee2b-cp310-cp310-linux_x86_64.whl
```

### 6.3 卸载旧版本（如果有）

```bash
pip3 uninstall torch torchvision triton torchaudio -y
```

### 6.4 安装 PyTorch

#### Ubuntu 24.04 (Python 3.12)

```bash
pip3 install torch-2.9.1+rocm7.2.0.lw.git7e1940d4-cp312-cp312-linux_x86_64.whl \
             torchvision-0.24.0+rocm7.2.0.gitb919bd0c-cp312-cp312-linux_x86_64.whl \
             torchaudio-2.9.0+rocm7.2.0.gite3c6ee2b-cp312-cp312-linux_x86_64.whl \
             triton-3.5.1+rocm7.2.0.gita272dfa8-cp312-cp312-linux_x86_64.whl
```

**注意**：在 Python 3.12 的非虚拟环境中安装时，可能需要添加 `--break-system-packages` 标志。如果使用 Conda 环境（推荐），则不需要此标志。

#### Ubuntu 22.04 (Python 3.10)

```bash
pip3 install torch-2.9.1+rocm7.2.0.lw.git7e1940d4-cp310-cp310-linux_x86_64.whl \
             torchvision-0.24.0+rocm7.2.0.gitb919bd0c-cp310-cp310-linux_x86_64.whl \
             torchaudio-2.9.0+rocm7.2.0.gite3c6ee2b-cp310-cp310-linux_x86_64.whl \
             triton-3.5.1+rocm7.2.0.gita272dfa8-cp310-cp310-linux_x86_64.whl
```

### 6.5 更新 WSL 兼容的运行时库

这是 **关键步骤**，用于确保 PyTorch 能在 WSL 环境中正常工作：

```bash
# 定位 torch 库的安装位置
location=$(pip show torch | grep Location | awk -F ": " '{print $2}')

# 进入 torch 库目录
cd ${location}/torch/lib/

# 移除不兼容的 HSA 运行时库
rm libhsa-runtime64.so*
```

### 6.6 处理 NumPy 兼容性问题

NumPy 2.0 与当前版本的 PyTorch wheel 不兼容，需要降级：

```bash
pip3 install numpy==1.26.4
```

### 6.7 （可选）Conda 环境的 GCC 升级

如果你在使用 Conda 环境时遇到 `ImportError: version 'GLIBCXX_3.4.30' not found` 错误，需要升级 GCC：

```bash
conda install -c conda-forge gcc=12.1.0 -y
```

---

## 7. 验证安装

### 7.1 验证 PyTorch 导入

```bash
python3 -c 'import torch' 2> /dev/null && echo 'PyTorch 导入成功' || echo 'PyTorch 导入失败'
```

**预期输出**：
```
PyTorch 导入成功
```

### 7.2 检查 GPU 可用性

```bash
python3 -c 'import torch; print(torch.cuda.is_available())'
```

**预期输出**：
```
True
```

如果输出为 `False`，说明 PyTorch 无法检测到 GPU，请参考[故障排除](#8-故障排除)部分。

### 7.3 显示 GPU 设备名称

```bash
python3 -c "import torch; print(f'GPU 设备: {torch.cuda.get_device_name(0)}')"
```

**预期输出**（以 RX 7700 XT 为例）：
```
GPU 设备: Radeon RX 7700 XT
```

### 7.4 查看环境详细信息

```bash
python3 -m torch.utils.collect_env
```

这会显示完整的 PyTorch 环境信息，包括：
- PyTorch 版本
- ROCm 版本
- 操作系统信息
- GPU 配置
- HIP 运行时版本
- MIOpen 版本

### 7.5 运行简单的 GPU 测试

创建一个测试脚本：

```bash
cat > test_gpu.py << 'EOF'
import torch

# 检查 GPU 是否可用
if torch.cuda.is_available():
    print(f"✓ GPU 可用")
    print(f"✓ GPU 数量: {torch.cuda.device_count()}")
    print(f"✓ 当前 GPU: {torch.cuda.get_device_name(0)}")
    
    # 在 GPU 上创建张量
    x = torch.rand(5, 3).cuda()
    print(f"✓ 在 GPU 上创建张量成功")
    print(f"张量内容:\n{x}")
    
    # 简单的 GPU 计算
    y = x * 2
    print(f"✓ GPU 计算成功")
    print(f"计算结果:\n{y}")
else:
    print("✗ GPU 不可用")
EOF

# 运行测试
python3 test_gpu.py
```

**预期输出**：
```
✓ GPU 可用
✓ GPU 数量: 1
✓ 当前 GPU: Radeon RX 7700 XT
✓ 在 GPU 上创建张量成功
张量内容:
tensor([[0.xxxx, 0.xxxx, 0.xxxx],
        [0.xxxx, 0.xxxx, 0.xxxx],
        [0.xxxx, 0.xxxx, 0.xxxx],
        [0.xxxx, 0.xxxx, 0.xxxx],
        [0.xxxx, 0.xxxx, 0.xxxx]], device='cuda:0')
✓ GPU 计算成功
计算结果:
[...]
```

---

## 8. 故障排除

### 8.1 问题：`rocminfo` 无法识别 GPU

**可能原因**：
- Windows 驱动未正确安装
- 未重启计算机
- ROCm 安装不完整

**解决方法**：
1. 确认 Windows 驱动版本为 Adrenalin Edition 26.1.1
2. 确保已重启计算机
3. 重新安装 ROCm：
   ```bash
   sudo amdgpu-uninstall
   sudo amdgpu-install -y --usecase=wsl,rocm --no-dkms
   ```

### 8.2 问题：`torch.cuda.is_available()` 返回 `False`

**可能原因**：
- PyTorch 未正确安装
- HSA 运行时库未更新
- Python 版本不匹配

**解决方法**：
1. 确认 PyTorch 版本：
   ```bash
   pip3 show torch
   ```
   应显示版本为 `2.9.1+rocm7.2.0`

2. 重新执行 HSA 运行时库更新步骤（6.5 节）

3. 确认 Python 版本：
   - Ubuntu 24.04 应使用 Python 3.12
   - Ubuntu 22.04 应使用 Python 3.10

### 8.3 问题：ImportError: version 'GLIBCXX_3.4.30' not found

**原因**：Conda 环境中的 GCC 版本过低

**解决方法**：
```bash
conda install -c conda-forge gcc=12.1.0 -y
```

### 8.4 问题：NumPy 版本不兼容

**症状**：
- 导入 PyTorch 时出现 NumPy 相关错误
- 版本冲突警告

**解决方法**：
```bash
pip3 install numpy==1.26.4
```

### 8.5 问题：下载 wheel 文件失败

**原因**：网络连接问题或 URL 编码

**解决方法**：
1. 检查网络连接
2. 使用浏览器手动下载 wheel 文件
3. 或使用代理/镜像源

### 8.6 问题：WSL 版本不是 2

**检查方法**：
```powershell
wsl --list --verbose
```

**升级到 WSL 2**：
```powershell
wsl --set-version Ubuntu-24.04 2
```

### 8.7 获取更多帮助

如果遇到其他问题：

1. **查看 ROCm 官方文档**：
   - [https://rocm.docs.amd.com/](https://rocm.docs.amd.com/)

2. **AMD 开发者社区**：
   - [https://github.com/RadeonOpenCompute/ROCm/discussions](https://github.com/RadeonOpenCompute/ROCm/discussions)

3. **报告问题**：
   - [https://github.com/ROCm/ROCm/issues](https://github.com/ROCm/ROCm/issues)

---

## 9. 下一步

安装完成后，你可以：

1. **运行机器学习模型**
   - 使用 Hugging Face Transformers
   - 训练自定义模型

2. **使用 LLM 工具**
   - vLLM（大语言模型推理）
   - Llama.cpp
   - ComfyUI（图像生成）

3. **安装其他框架**
   - ONNX Runtime
   - TensorFlow
   - JAX

4. **优化性能**
   - GEMM 调优
   - FlashAttention-2

---

## 10. 参考链接

- [ROCm for Radeon and Ryzen 官方文档](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/)
- [WSL 兼容性矩阵](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityrad/wsl/wsl_compatibility.html)
- [ROCm WSL 安装指南](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installrad/wsl/install-radeon.html)
- [PyTorch WSL 安装指南](https://rocm.docs.amd.com/projects/radeon-ryzen/en/docs-7.2/docs/install/installrad/wsl/install-pytorch.html)
- [WSL 官方文档](https://learn.microsoft.com/zh-cn/windows/wsl/install)
- [AMD Adrenalin Edition 26.1.1 发布说明](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-1-1.html)
- [Miniconda 安装指南](https://www.anaconda.com/docs/getting-started/miniconda/install)

---

## 附录：版本兼容性表

| 组件 | 版本 | 备注 |
|------|------|------|
| Windows | 10 (Build 19041+) 或 11 | 推荐 Windows 11 |
| WSL 内核 | 5.15 | 自动安装 |
| Ubuntu | 22.04 或 24.04 | 推荐 24.04 |
| Python | 3.10 (22.04) 或 3.12 (24.04) | 根据 Ubuntu 版本 |
| ROCm | 7.2 | |
| PyTorch | 2.9.1 + ROCm 7.2 | |
| Triton | 3.5.1 + ROCm 7.2 | |
| NumPy | 1.26.4 | 不支持 2.0+ |
| AMD 驱动 | Adrenalin Edition 26.1.1 | WSL2 必需 |

---

**最后更新日期**：2025 年 2 月 12 日

**文档版本**：1.0

如有问题或建议，请参考故障排除部分或联系社区获取帮助。