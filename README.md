# 📁 发票上传系统后端
版本V1.0

本项目是一个发票上传和管理的后端服务，支持发票文件上传、发票打包下载，OCR扫描等功能。前端代码位于 `web` 分支，服务端主要通过可执行文件或源代码启动。本 `README.md` 将指导您如何配置和启动服务。

## 📂 目录结构

```
|-- data_upload_invoice/   # 存放上传的发票文件
|-- 临时文件/               # 存放打包后的发票文件，供前端下载（需要定期清理）
|-- 其他dll文件             # 项目所需的 DLL 文件
|-- 编译exe文件             # 服务端编译后的可执行文件
|-- README.md               # 项目说明文件
|-- config.json             # 配置文件
```

- **`data_upload_invoice/`**: 用于存放上传的发票文件。
- **`临时文件/`**: 用于存放打包后的发票文件，供前端下载使用，需要定期清理。
- **`其他dll文件`**: 项目运行过程中所需的其他动态链接库文件（DLL）。
- **`编译exe文件`**: 编译后的服务端可执行文件，推荐使用该文件启动服务。

---

## 🚀 快速开始

### 配置文件 `config.json` 说明

为了启动服务，你需要提供一个 `config.json` 配置文件。以下是 `config.json` 的内容说明：

```json
{
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "SQL_config": {
        "db_host": "127.0.0.1",
        "db_port": 3306,
        "db_user": "fapiao",
        "db_password": "fapiaosql123",
        "db_name": "fapiao"
    }
}
```

#### 配置项说明：
- **`host`**: 服务器 IP 地址（外部访问后端的 IP）。
- **`port`**: 服务器端口号。
- **`workers`**: 服务端的工作进程数量（推荐为 CPU 核心数的 2 倍）。
- **`SQL_config`**: 数据库的配置项，包含数据库连接的详细信息。
  - **`db_host`**: 数据库服务器的地址。
  - **`db_port`**: 数据库的端口号。
  - **`db_user`**: 数据库用户名。
  - **`db_password`**: 数据库密码。
  - **`db_name`**: 数据库名称。

### 使用编译后的 EXE 文件启动（推荐）

1. 打开命令行或终端，进入 `编译exe文件` 目录：
   ```bash
   cd invoice_upload/Backend
   ```

2. 启动服务：
   ```bash
   ./invoice_server.exe
   ```

> **提示**: 使用 EXE 文件启动的性能要优于源代码启动。

---

### 使用源代码启动（不推荐）

如果你需要使用源代码启动，请按照以下步骤操作：

1. **创建并激活虚拟环境**（可选）：
   - **Linux/macOS**：
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows**：
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

2. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

3. **启动服务**：
   ```bash
   python main.py
   ```

---

## 🛠 文件清理

- **`临时文件/`** 文件夹用于存放打包后的临时文件，这些文件需要定期清理，以避免磁盘空间被占满。

### 定期清理任务建议：
- **Linux**: 使用 `cron` 定时清理，例如每天凌晨清理：
  ```bash
  0 0 * * * rm -rf /path/to/临时文件/*
  ```

- **Windows**: 使用任务计划程序（Task Scheduler）配置定时任务，定期删除临时文件。

---

## 📋 环境要求

- **操作系统**: Windows 或 Linux
- **依赖**: 项目依赖使用 `requirements.txt` 管理，安装方式见上文。
- **前端代码**: 前端代码位于 `web` 分支，使用 Vue.js 构建。

---

## 📦 项目依赖

所有项目的依赖项都列在 `requirements.txt` 文件中。如果你使用源代码启动项目，请使用以下命令来安装依赖项：

```bash
pip install -r requirements.txt
```

---

## ⚠️ 注意事项

1. **性能问题**: 建议优先使用编译后的 EXE 文件启动服务。Python 源代码启动方式性能较低。
2. **定时清理临时文件**: `临时文件/` 文件夹中存放的文件应定期清理，防止占用大量磁盘空间。
3. **前端代码**: 前端部分代码位于 `web` 分支，需与后端配合使用，前端使用 Vue.js 框架构建。

---

## 📄 License

该项目遵循 MIT 许可证。更多详细信息请查看 [LICENSE](./LICENSE)。

---

## ✨ 开发者信息

- **作者**: UR-xiaoyang
- **联系方式**: xiaoyang@ur-xiaoyang.com
- **项目贡献**: 欢迎提交 issue 和 pull request，共同改进项目！
- **欢迎提出改进建议** : 

---
