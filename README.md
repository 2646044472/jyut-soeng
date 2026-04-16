# 粤常

`粤常` 的意思是“粤语变日常”。

这是一个面向个人小米手机侧载使用的 Android 粤语正音 App。核心思路不是背一张粤拼表，而是把 `Jyutping` 当成正音标尺：先开口，再用粤拼校对自己的声母、韵母、语流和常错点。

会保留一点“背词感”的学习节奏，但界面和练习结果默认不展示英文对照，重点仍然是把音读准、把表达用顺。

## 当前能力

- Jetpack Compose + Hilt + Room + DataStore + WorkManager + Media3
- 4 个主页面：`今日`、`词库`、`搜索`、`我的`
- 学习与复习分成两条主线：
  - `今日学习`：先学新词，再学新表达
  - `今日复习`：把已学内容刷回嘴边
- 两种主练模式：
  - `输入题`：看词或表达，手动写 Jyutping（不用填 123456）
  - `多选题`：熟词快刷题，用于提高复习效率
- 输入题 + 多选题并存；多选主要用于加速复习
- 更细的 SRS 复习排程：输入题和多选题使用不同记忆权重
- 正误反馈带音效
- 本地 JSON 内容导入
- GitHub 内容更新入口
- 应用名与图标已切到 `粤常`
- 当前内置题库：
  - 2993 条词语正音词条
  - 193 条俚语 / 日常表达卡片
  - 合计 3186 条

## 当前题库方向

- 不再把“参考音高”当成主练法
- 更强调真实词语、真实表达、例句和常错提醒
- `Jyutping` 是辅助你正音的手段，不是终点本身
- 构建脚本现在会自动汇总 `content/*_bank.json`
- 已接入大词表自动筛选链，可持续扩到几千条以上

## 构建

需要：

- JDK 21
- Android SDK：
  - `platform-tools`
  - `platforms;android-35`
  - `build-tools;35.0.0`

构建命令：

```bash
./gradlew --no-daemon --console=plain :app:testDebugUnitTest :app:assembleDebug
```

APK 输出：

```text
app/build/outputs/apk/debug/app-debug.apk
```

## GitHub 内容包

构建内置内容：

```bash
python3 tools/build_assets.py
python3 tools/validate_content.py
python3 tools/export_github_pack.py
```

导出的 GitHub 内容包目录：

- `dist/github/jyut-soeng/content.json`

App 里的 GitHub 更新逻辑默认读取 GitHub 仓库中的这一套导出结果。

## 发布

推送 `v*` tag 后，GitHub Actions 会自动：

1. 安装 Android SDK 依赖
2. 运行 `:app:testDebugUnitTest`
3. 构建 debug APK
4. 创建 GitHub Release
5. 上传 APK 和内容包 zip
