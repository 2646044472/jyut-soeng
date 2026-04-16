# Canto Calibrator

`jyut-soeng` 即“粤常”的粤语拼音。

这是一个面向个人小米手机侧载使用的 Android 粤语高阶读音校准 App MVP，目标是把粤语读音练习做成每天都能打开、每天都能推进的日常工具。

希望粤语变成日常。

## 当前能力

- Jetpack Compose + Hilt + Room + DataStore + WorkManager + Media3
- 4 个主页面：`今日`、`词库`、`搜索`、`我的`
- 学习 session、判题、SRS 复习排程
- 本地 JSON 内容导入
- GitHub 内容更新入口
- 240 条内置校准内容和 240 个合成参考音高 WAV

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

仓库根目录下的 `canto-calibrator/` 目录是给 App 在线拉取的内容包：

- `canto-calibrator/content.json`
- `canto-calibrator/audio/generated/*.wav`

App 里的 GitHub 更新逻辑默认读取这个目录。

## 发布

推送 `v*` tag 后，GitHub Actions 会自动：

1. 安装 Android SDK 依赖
2. 运行 `:app:testDebugUnitTest`
3. 构建 debug APK
4. 创建 GitHub Release
5. 上传 APK 和内容包 zip
