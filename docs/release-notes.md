# Medical Illustration v1.1.1

为已经安装 Skill 的用户加入“检查更新、更新、回退”三个入口，减少重复安装报错和手工覆盖风险。原有漫画、科研图与 Illustrator 工作流保留。

- 随包 `update_skill.py` 默认查询最新正式 GitHub Release，核验独立 ZIP、SHA-256、内部清单和版本；支持离线包。
- GitHub 匿名 API 返回 403/429 时，自动尝试已登录 GitHub CLI 的只读查询；不提取令牌、启动登录或输出认证调试信息。CLI为可选依赖，不可用时保留原安装并提示重试/离线方式。
- 检测本地修改及缺少 VERSION/清单的旧安装，默认保留现场。用户明确选择后完整备份并替换，不静默合并或丢弃修改。
- 更新前后核对文件哈希，提供安装锁、完整旧版备份、失败恢复和可逆回退；历史备份保存在技能扫描目录之外。
- 遇到多个安装位置、插件管理目录、损坏包、路径异常或备份被修改时拒绝相关操作。网络失败不误报为最新。
- 增加更新器回归测试，并纳入 Validate 与 Release 的跨平台 CI。磁盘验收不代表宿主已刷新。

## 安装与旧版升级

本版本实际发布后，见[安装说明](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.1/INSTALL.md)。1.1.0 及更早版本没有更新器，需要先从完整新包取得脚本并指向实际旧安装目录；接入一次后可直接使用内置更新入口。已有漫画项目和模板不迁移。

独立附件为 `medical-illustration-1.1.1.zip` 与同名 `.sha256`；GitHub Source code 是完整仓库。插件管理或缓存副本应通过宿主更新，本脚本不覆盖。

[验证范围](https://github.com/wilbert-MD-PhD/medical-illustration/blob/v1.1.1/docs/validation.md)区分本地测试、远端 CI 与宿主实测。软件更新不构成医学审签或印前批准。

## English

Version 1.1.1 adds built-in check, update and rollback commands for standalone installations. Updates verify the release archive, checksums and version, preserve a complete backup, and restore the original after a caught replacement failure. Local edits and unknown legacy baselines require an explicit backup-and-replace choice; project files are untouched.

Older installations bootstrap once from a complete new package. Plugin-managed copies must use their host updater. Offline packages are supported. On anonymous API HTTP 403/429, the updater can reuse an existing authenticated GitHub CLI session without extracting credentials or prompting for login. Refresh the host and verify the loaded path/version after disk installation; package validation does not prove host discovery or medical approval.
