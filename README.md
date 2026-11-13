# 粤常

`粤常` 的意思是“粤语变日常”。

这是一个面向个人小米手机侧载使用的 Android 粤语正音 App。核心思路不是背一张粤拼表，而是把 `Jyutping` 当成正音标尺：先开口，再用粤拼校对自己的声母、韵母、语流和常错点。

会保留一点“背词感”的学习节奏，但界面和练习结果默认不展示英文对照，重点仍然是把音读准、把表达用顺。

## 当前能力

- Jetpack Compose + Hilt + Room + DataStore + WorkManager + Media3
- 4 个底部主页面：`今日`、`词库`、`搜索`、`我的`；句子学习从首页进入
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
- 独立的`句子学习`页面：默认每天学习 50 句，可在`我的`页面调整目标；学习时先看逐字对齐的粤拼和汉字，按需展开释义，点击下一句继续
- 本地 JSON 内容导入
- GitHub 内容更新入口
- 应用内检查新版 APK，并可直接拉起系统安装覆盖更新
- 词库只收录标记为 `curated` 的词条；答题反馈和词库卡片会显示正音重点
- 应用名与图标已切到 `粤常`
- 当前内置题库：
  - 2600 条词语正音词条
  - 400 条日常表达卡片
  - 2000 张入选故事卡，包含繁体粤语、逐字粤拼、简体普通话释义和复述练习
  - 题库合计 5000 条

## 当前题库方向

- 不再把“参考音高”当成主练法
- 更强调真实词语、真实表达、例句和常错提醒
- `Jyutping` 是辅助你正音的手段，不是终点本身
- 构建脚本会汇总 `content/*_bank.json` 及 `content/sentence_bank/*.json` 中的条目；本版独立句子卡逐句编写，不使用脚本批量生成句子
- 应用内故事库按选择台账打包 2000 张故事卡；未入选故事不会进入内置故事列表
- 发布校验会检查结构、重复和明显模板化内容；粤拼、语境和地道程度仍需逐句复核，不能只靠自动测试保证
- `v0.36.3` 复审故事口语、逐字粤拼与复述提示；内置故事列表仍为 2000 张
- 活动故事源目录现保留入选的 2000 张；另外 3000 张原始卡保存在 `content/story_archive/jyut-soeng-original-source-v0.36.3.zip`，旁车 `content/story_source_index_map.json` 记录稳定 ID、原始文件和原始数组位置。审核台账仍按原 5000 行索引保留。
- 归档含原始故事文件、V2/口语台账、选集及 v0.36.3 内容资产，SHA-256 清单在 `content/story_archive/manifest.json`。用 `python3 tools/restore_story_archive.py` 校验归档；运行 `python3 tools/restore_story_archive.py --restore` 会恢复完整 5000 行源库，并同步切换索引映射到完整源状态，恢复后可直接重新构建。若要在隔离目录检查恢复结果，可加 `--destination /tmp/story-restore-check`；恢复命令不会删除归档。

## 例句撰写与检查

1. 逐卡构思生活场景、繁体粤语故事和粤拼；故事约 220–320 个汉字，主要控制在 250–300 字，附逐字核对的 Jyutping、完整简体普通话释义及以“故事练习：”开头的复述提示，保存到 `content/sentence_bank/`；不用脚本生成、翻译或转写语言字段。
2. 每批完成后再逐句检查逻辑、口语自然度、俚语用法、粤拼声韵调和释义；澳门语境不靠硬塞地名，避免不确定的本地政策、路线及价格细节。
3. 运行 `python3 tools/build_assets.py`、`python3 tools/validate_content.py --require-story-upgrade --min-sentences 2000` 和 `python3 -m unittest discover -s tools/tests -p 'test*.py'`。自动测试能发现结构和数量问题，不能替代语义及读音复核。
4. 发布前确认内置内容恰有 2000 张故事卡，并验证 Android 构建和阅读界面。

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
