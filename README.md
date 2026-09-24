# 粤常

`粤常` 的意思是“粤语变日常”。

这是一个面向个人小米手机侧载使用的 Android 粤语正音 App。核心思路不是背一张粤拼表，而是把 `Jyutping` 当成正音标尺：先开口，再用粤拼校对自己的声母、韵母、语流和常错点。

会保留一点“背词感”的学习节奏，但界面和练习结果默认不展示英文对照，重点仍然是把音读准、把表达用顺。

## 当前能力

- Jetpack Compose + Hilt + Room + DataStore + WorkManager + Media3
- 5 个主页面：`今日`、`例句`、`词库`、`搜索`、`我的`
- 学习与复习分成两条主线：
  - `今日学习`：先学新词，再学新表达
  - `今日复习`：把已学内容刷回嘴边
- 两种主练模式：
  - `输入题`：看词或表达，手动写 Jyutping（不用填 123456）
  - `多选题`：熟词快刷题，用于提高复习效率
- 输入题 + 多选题并存；多选主要用于加速复习
- 更细的 SRS 复习排程：输入题和多选题使用不同记忆权重
- 正误反馈带音效
- `例句`阅读模式：每天轮换一组较完整的日常粤语复合句，默认显示粤语原句和 Jyutping，中文意思与使用场景按需展开；设备有粤语语音时可点击播放
- 本地 JSON 内容导入
- GitHub 内容更新入口
- 应用内检查新版 APK，并可直接拉起系统安装覆盖更新
- 词库只收录标记为 `curated` 的词条；答题反馈和词库卡片会显示正音重点
- 应用名与图标已切到 `粤常`
- 当前内置题库：
  - 2600 条词语正音词条
  - 400 条日常表达卡片
  - 810 条日常例句（其中 440 条为本轮逐句撰写的澳门及日常场景内容）
  - 合计 3810 条

## 当前题库方向

- 不再把“参考音高”当成主练法
- 更强调真实词语、真实表达、例句和常错提醒
- `Jyutping` 是辅助你正音的手段，不是终点本身
- 构建脚本会汇总 `content/*_bank.json` 中标记为 `curated` 的条目；该标记表示编辑筛选，不代表真人撰写
- 发布校验会检查结构、重复和明显模板化内容；粤拼、语境和地道程度仍需逐句复核，不能只靠自动测试保证
- 正式 Release 额外要求至少 2000 句；当前 810 句，尚未达到发布目标

## 例句撰写与检查

1. 逐句构思日常场景、粤语正文、粤拼、中文解释和使用场景，保存到 `content/*sentence*_bank.json`；不用脚本拼接句子或套用同一模板批量扩写。
2. 每批完成后再逐句检查逻辑、口语自然度、俚语用法、粤拼声韵调和释义；澳门语境不靠硬塞地名，避免不确定的本地政策、路线及价格细节。
3. 运行 `python3 tools/build_assets.py`、`python3 tools/validate_content.py` 和 `python3 -m unittest discover -s tools/tests -p 'test*.py'`。自动测试能发现结构和数量问题，不能替代语义及读音复核。
4. 发布前运行 `python3 tools/validate_content.py --min-sentences 2000`，并验证 Android 构建和阅读界面。

## 构建

需要：

- JDK 21
- Android SDK：
  - `platform-tools`
  - `platforms;android-35`
  - `build-tools;35.0.0`

构建命令：

```bash
./gradlew --no-daemon --console=plain :app:testDebugUnitTest :app:assembleRelease
```

APK 输出：

```text
app/build/outputs/apk/release/app-release.apk
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

应用 APK 更新会读取 GitHub 最新 Release，并下载最新 APK 资产来覆盖安装。

## 签名与升级

- 现在的 APK 使用 repo 内固定 sideload keystore 签名，后续版本可以直接覆盖安装，保留应用数据。
- 由于更早几版 Release 使用的是临时 debug 签名，如果你手机里当前安装的是那批旧包，切到这个新签名时可能仍然需要最后重装一次。
- 这次之后，只要继续安装同一条发布链生成的 APK，就不需要再因为签名变化而卸载重装。

## 发布

推送 `v*` tag 后，GitHub Actions 会自动：

1. 安装 Android SDK 依赖
2. 运行 `:app:testDebugUnitTest`
3. 构建 release APK
4. 创建 GitHub Release
5. 上传 APK 和内容包 zip
