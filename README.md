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
  - 370 条日常例句（仍需真人粤语母语者复核）
  - 合计 3370 条

## 当前题库方向

- 不再把“参考音高”当成主练法
- 更强调真实词语、真实表达、例句和常错提醒
- `Jyutping` 是辅助你正音的手段，不是终点本身
- 构建脚本会汇总 `content/*_bank.json` 中标记为 `curated` 的条目；该标记不证明真人撰写或审核
- 发布校验会检查结构、重复和明显模板化内容；粤拼、语境和地道程度仍需逐条由真人确认
- 正式 Release 额外要求至少 2000 句，并为每句提供真人撰写及复核记录；当前 370 句未有这类记录，不能视为已验收

## 例句供稿与验收

1. 真人作者逐句撰写日常场景句子、粤拼、中文解释及使用场景，保存到 `content/*sentence*_bank.json`。不要用模型批量生成或补写。澳门生活语境、俚语和较复杂语流要由熟悉当地用法的人把关。
2. 真人复核者逐句检查地道程度、粤拼声韵调、文字与音节对应、释义和语境；自动校验只能发现部分结构错误。
3. 复核通过后，在 `content/sentence_human_reviews.json` 的 `reviews` 数组中逐句登记 `id`、`humanAuthored: true`、`author`、`reviewer`、`reviewedAt`（YYYY-MM-DD）和 `contentSha256`。指纹可用 `python3 tools/sentence_reviews.py <句子ID>` 查询；这只计算校验值，不会生成内容。正文或粤拼修改后必须重新复核并更新指纹。
4. 用 `python3 tools/validate_content.py --min-sentences 2000 --require-human-reviews` 检查发布条件。姓名和声明本身仍不能自动证明真人来源，须由实际供稿、复核者如实填写。

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
