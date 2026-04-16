# 粤常

`粤常` 的意思是“粤语变日常”。

这是一个面向个人小米手机侧载使用的 Android 粤语正音 App。核心思路不是背一张粤拼表，而是把 `Jyutping` 当成正音标尺：先开口，再用粤拼校对自己的声母、韵母、语流和常错点。

英语释义会保留一点“背词感”，但最终目标是把音读准、把表达用顺。

## 当前能力

- Jetpack Compose + Hilt + Room + DataStore + WorkManager + Media3
- 4 个主页面：`今日`、`词库`、`搜索`、`我的`
- 两种主练模式：
  - `词语正音`：看词填 Jyutping，用输入方式校正读音
  - `俚语与用法`：卡片化学习表达、例句和使用场景，再补 Jyutping
- 输入题 + 多选题并存；多选主要用于加速复习
- 更细的 SRS 复习排程：输入题和多选题使用不同记忆权重
- 本地 JSON 内容导入
- GitHub 内容更新入口
- 应用名与图标已切到 `粤常`
- 当前内置题库：
  - 32 条高频正音词条
  - 15 条俚语 / 日常表达卡片

## 当前题库方向

- 不再把“参考音高”当成主练法
- 更强调真实词语、真实表达、例句和常错提醒
- `Jyutping` 是辅助你正音的手段，不是终点本身

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

- `dist/github/canto-calibrator/content.json`
- `dist/github/canto-calibrator/audio/generated/*.wav`

App 里的 GitHub 更新逻辑默认读取 GitHub 仓库中的这一套导出结果。

## 发布

推送 `v*` tag 后，GitHub Actions 会自动：

1. 安装 Android SDK 依赖
2. 运行 `:app:testDebugUnitTest`
3. 构建 debug APK
4. 创建 GitHub Release
5. 上传 APK 和内容包 zip
