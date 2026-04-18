# Canto Calibrator Handoff

更新时间：2026-04-16

## 当前目标

在 `apps/jyut-soeng/` 下实现一个只给小米手机侧载使用的 Android 粵語高階讀音校準 App MVP。

## 已完成

- 安装了 JDK 21，`java -version` 正常。
- 创建了 Android 工程根骨架：
  - `settings.gradle.kts`
  - `build.gradle.kts`
  - `gradle.properties`
  - `gradle/libs.versions.toml`
  - `app/build.gradle.kts`
  - `app/proguard-rules.pro`
  - `.gitignore`
- 已创建项目目录：`/home/ubuntu/apps/jyut-soeng`
- Android SDK 目录已建立在：`/home/ubuntu/android-sdk`

## 当前状态

- Android SDK 安装命令仍在后台运行。
- 观测到的后台进程：

```text
/bin/bash -c set -e export ANDROID_SDK_ROOT=/home/ubuntu/android-sdk ...
/usr/lib/jvm/java-21-openjdk-amd64/bin/java ... sdkmanager ... platform-tools platforms;android-35 build-tools;35.0.0
```

- 从磁盘状态看，以下目录已经出现，说明 SDK 安装大概率接近完成或正在收尾：
  - `/home/ubuntu/android-sdk/build-tools/35.0.0`
  - `/home/ubuntu/android-sdk/platform-tools`
  - `/home/ubuntu/android-sdk/platforms/android-35`
  - `/home/ubuntu/android-sdk/licenses`

- `gradle` 本地分发目录只创建了根目录：
  - `/home/ubuntu/.local/gradle-dist`
- Gradle 发行包下载/解压尚未确认完成。

## 当前文件清单

```text
/home/ubuntu/apps/jyut-soeng/.gitignore
/home/ubuntu/apps/jyut-soeng/app/build.gradle.kts
/home/ubuntu/apps/jyut-soeng/app/proguard-rules.pro
/home/ubuntu/apps/jyut-soeng/build.gradle.kts
/home/ubuntu/apps/jyut-soeng/gradle.properties
/home/ubuntu/apps/jyut-soeng/gradle/libs.versions.toml
/home/ubuntu/apps/jyut-soeng/settings.gradle.kts
```

## 下一步实施顺序

1. 确认 `sdkmanager` 已结束，必要时查看：
   - `/tmp/android-sdk-licenses.log`
   - `/tmp/android-sdk-install.log`
2. 下载并解压 Gradle 8.7，生成 `gradlew`、`gradlew.bat` 和 `gradle/wrapper/*`
3. 补全 Android app 最小可编译骨架：
   - `AndroidManifest.xml`
   - `Application` / `Activity`
   - Compose 主题与导航
   - Hilt 基础接入
4. 搭建数据层：
   - Room entities / DAO / database
   - DataStore settings
   - content import pipeline
   - search repository
5. 落 UI 与学习流程：
   - `今日`
   - `詞庫`
   - `搜尋`
   - `我的`
   - 学习 session / 判题 / SRS
6. 建内容工具链：
   - `tools/validate_content.py`
   - `tools/build_assets.py`
   - `tools/generate_audio.py`
   - `tools/report_content.py`
7. 生成 240 条内置内容与音频，导入到 `app/src/main/assets/`
8. 跑测试与构建，产出可安装 APK

## 已选定的关键约束

- 目标设备只考虑你本人使用的小米手机，当前是小米 15 Pro，后续也只考虑更好的小米手机。
- 首版不做公开分发、不做多品牌兼容、不做云同步、不做账号、不做录音跟读。
- 更新方式固定为手动安装新 APK。
- 技术栈固定：
  - Kotlin
  - Jetpack Compose
  - Hilt
  - Room
  - DataStore
  - WorkManager
  - Media3
- Android 基线：
  - `compileSdk 35`
  - `targetSdk 35`
  - `minSdk 31`

## 接续时的注意点

- 这是 `ralph` 模式任务，不能只停在脚手架，必须继续推进到可构建、可验证、尽量可安装。
- 用户要求“尽可能完善”，所以要优先做完整闭环，而不是只做空页面。
- 当前 `/home/ubuntu` 不是 git 仓库；不要依赖 git 工作流来判断变更。
- 如果后台 `sdkmanager` 卡住，要先查日志和进程，再决定是否重跑，不要盲目重复安装。
