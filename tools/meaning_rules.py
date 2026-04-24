from __future__ import annotations

import re

LOW_INFO_GLOSS_MARKERS = (
    "常用词，适合放进句子里练熟",
    "常用来讲感受、状态或反应",
    "工作沟通里常见的词",
    "学习和说明语境里常用的词",
    "日常讲话常见词",
    "偏口语的说法，常用来讲状态、场面或反应",
    "对话里常见的说法，听起来会比较自然",
    "常见表达，日常讲话时可以自然用",
    "多用于交代事情、讲进度或讲处理方式",
    "用来表达感觉、情绪或当下反应",
)

LOW_INFO_USAGE_MARKERS = (
    "适合练",
    "适合拿来练",
    "适合拿来校正",
    "适合校正",
    "适合做基础稳定练习",
    "拿来练",
    "值得反复校正",
    "越高频越值得校准",
    "重点是读得自然",
    "读起来",
    "拿来练稳定度",
    "练鼻尾",
    "练入声",
    "练开口度",
    "练口型",
    "练圆唇韵母",
    "练自然语气",
    "普通话",
    "连读",
    "语流",
    "日常句子里直接用就可以。",
    "多放在讲感觉、情绪变化和反应时。",
    "适合放在开会、交代事情和讲做法时。",
    "适合放在提问、复述和说明时。",
    "对话里很常见，重点是读得自然。",
    "多放在熟人闲聊、吐槽和即时反应里。",
    "适合直接放进对话里，句子不用太长。",
    "日常开口时可以直接带出来。",
    "这条先当语气卡：跟读、记节奏就够；真要学点用，优先看人工整理的表达卡。",
    "这条先当读音卡：跟读、拆音、写 Jyutping 就够；真要学点用，优先看人工整理词条。",
)

GENERATED_WORD_GLOSS_OVERRIDES = {
    "善解人意": "形容人好识体谅别人，明白别人心思。",
    "心理關口": "指心理上最难跨过去的一关。",
    "本能反應": "指唔经思考就自然做出来的反应。",
    "自然反應": "指顺住当下情况，自然做出来的反应。",
    "通情達理": "形容人明白事理，又识得体谅别人。",
    "自作自受": "自己搞出来的后果，要自己受返。",
    "一時意氣": "一时冲动，为咗面子或者情绪去做决定。",
    "一本正經": "形容人好认真好严肃；有时带少少装正经意味。",
    "人工智能": "指电脑系统模仿人去学习、判断同处理信息的能力。",
    "人心肉做": "比喻人都有感情，会痛会受伤，唔系铁石心肠。",
    "人貴自知": "指人最紧要知道自己斤两，识得自量。",
    "人際關係": "指人与人之间点样相处、来往同合作。",
    "作法自斃": "自己用错做法，结果害返自己。",
    "修成正果": "经过一轮努力之后，终于有好结果。",
    "個人資料": "指个人身份、联络方式等资料同信息。",
    "出人意料": "结果超出一般预料，令人估唔到。",
    "出人意表": "同「出人意料」相近，指结果超出想像。",
    "分工合作": "将工作分开，各人负责一部分，再一齐配合完成。",
    "安守本分": "指守住自己本分，唔乱来越界。",
    "安於現狀": "习惯眼前状态，唔太想改变。",
    "安然度過": "平安顺利咁捱过某段日子或者难关。",
    "導人向善": "引导人朝住好嘅方向去做。",
    "度身定做": "按对象需要特别订做，啱啱好。",
    "心安理得": "自己觉得做得啱，所以心里面好安乐。",
    "心意相通": "指两个人心里明白对方，沟通好顺。",
    "心理準備": "事前先在心里面准备好可能发生的情况。",
    "成本效益": "讲投入几多成本，换返几多效果值唔值。",
    "打通關係": "靠人脉或者关系，令事情更容易办。",
    "捫心自問": "自己认真问返自己内心点睇。",
    "撫心自問": "静下来问返自己，心里面到底点谂。",
    "正氣凜然": "形容人一身正气，态度正直有骨气。",
    "浩然正氣": "形容堂堂正正、好有正气嘅气势。",
    "目定口呆": "惊到望实晒，连口都开埋，讲唔出嘢。",
    "目標人物": "被重点留意、跟进或者针对嘅人。",
    "目無表情": "脸上冇乜表情，睇唔出情绪。",
    "知人善任": "识得拣啱人去做啱嘅事。",
    "知錯能改": "知道自己错咗，而且愿意改正。",
    "自作多情": "自己一厢情愿，以为别人对自己有意思或重视自己。",
    "表情管理": "指控制自己面部表情，唔俾情绪乱咁流出来。",
}

GENERATED_EXPRESSION_GLOSS_OVERRIDES = {
    "冇乜嘢": "表示冇咩特别事、冇大碍，等于「没什么」。",
    "唔夠佢嚟": "表示同对方比都仲差一截，完全唔够人来。",
    "嗰啲嘢": "口语里笼统指某类东西、某啲事，唔讲到太白。",
    "要乜冇乜": "想要咩都冇，形容样样都唔齐。",
    "冇嗰樣整嗰樣": "冇现成嗰样就临时搵第二样顶住。",
    "乜嘢料呀": "问对方咩来头、咩水平，常带试探语气。",
    "平嘢冇好嘢": "表示平价货通常冇好品质。",
    "冇咁好氣": "表示自己冇咁好脾气，唔会咁容易让步。",
    "冇咁嬲": "表示火气已经细咗，冇之前咁生气。",
    "冇你咁好氣": "表示自己唔似你咁好脾气、咁肯忍。",
    "冇聲冇氣": "形容冇乜反应、冇晒气力，静到出奇。",
    "唔聲唔氣": "一句声都唔出，静静鸡咁。",
    "弊弊都冇咁弊": "再差都唔会差到咁，带夸张吐槽。",
    "冇乜兩句": "讲唔多两句就会点样，指情况好快发生。",
    "扮嗰樣似嗰樣": "扮得好似，学乜似乜。",
    "咁耐以嚟": "指由以前到而家呢段时间以来。",
    "唔係咁講": "表示前面讲法唔啱，想纠正或者换个角度讲。",
    "話冇咁快": "表示事情唔会咁快发生或者做到。",
    "話冇咁易": "表示件事冇想像中咁容易。",
    "乜唔係": "带惊讶反问，意思接近「唔係咩？」。",
    "乜嘢話": "表示听唔清楚或者觉得惊讶，要对方再讲一次。",
    "做乜嘢": "问人点解要咁做，等于「做什么」。",
    "冇乜點": "表示情况普通、冇乜特别。",
    "冇佢符": "表示拿某人某事冇办法。",
    "唔喺度": "表示人唔在场，或者眼前唔存在。",
    "嚟唔切": "表示来不及，赶唔上。",
    "乜嘢環境": "问当前到底系咩情况。",
    "冇乜大用": "表示作用唔大，帮唔到太多。",
    "冇嘢好講": "表示真系无话可说，可能系服咗或者顶唔顺。",
    "吹佢唔脹": "表示点激都激佢唔到，奈佢唔何。",
    "搞乜鬼呀": "带火气或者惊讶问对方搞咩。",
    "有乜唔妥": "问边度有问题、边样唔对路。",
    "唔理得咁多": "表示唔再顾咁多后果，照做先。",
    "咁就差唔多": "表示大致上已经到位，八九不离十。",
    "咩風吹你嚟": "惊讶对方点解会突然出现。",
    "有嗰句講嗰句": "照直讲心里话，有一说一。",
    "食飽飯冇嘢做": "形容人太得闲，先会去做某啲无聊事。",
    "嚟嚟去去": "表示翻来覆去都系嗰几个选择或者嗰个样。",
    "上氣唔接下氣": "形容喘到接唔上气。",
    "唔知頭唔知路": "形容对情况完全唔熟，唔知点入手。",
    "搞搞震冇幫襯": "只会搞乱档，帮唔到手。",
    "冇頭冇尾": "形容讲嘢或做事唔完整，前因后果都唔清楚。",
}

WORD_USAGE_OVERRIDES = {
    "點樣": "多用来问方法、状态或者结果，后面通常直接接动词。",
    "明白": "多用在回应别人解释、确认自己听懂，或者讲自己而家明唔明白。",
    "朋友": "多用在介绍关系、约人，或者讲自己同边个熟唔熟。",
    "香港": "多用在讲住边、去边、边度出身或者边度发生嘢。",
    "廣東話": "多用在讲自己识唔识讲、想唔想学，或者讲语言环境。",
    "飲水": "多用在提醒人补水，或者讲日常习惯。",
    "放工": "多用来讲几时收工、收工之后去边，通常同时间一齐出现。",
    "天氣": "多用来讲冷热、落雨、转天或者出门前安排。",
    "落雨": "多用来讲眼前天气变化，或者解释点解要带遮、改行程。",
    "學校": "多用在讲返学、接送、校园里面发生嘅事。",
    "醫院": "多用在讲睇医生、探病、做检查或者住院。",
    "老師": "多用来称呼教书嘅人，或者讲学校里面边个负责教你。",
    "容易": "多用在判断件事难唔难、顺唔顺手、好唔好处理。",
    "一定": "多放在判断句里，强调自己觉得件事好确定。",
    "緊要": "多用来讲边样最重要、最赶急，常见于提醒同判断。",
    "其實": "多放句首，表示想补返真实情况，或者轻轻修正前面讲法。",
    "小心": "多用来提醒对方留意环境、动作或者后果。",
    "覺得": "多用来讲自己意见、感受或者判断。",
    "逐樣": "多用来讲一项项处理、一件件讲清楚。",
    "人工智能": "多用来讲科技系统识唔识自己学、自己分析，工作同新闻场景都好常见。",
    "個人資料": "多用在登记、交表、核对身份同联络方式时。",
    "分工合作": "开会、做 project、分配工作时特别常见。",
    "心理準備": "多用来讲事前先调整心态，准备面对某个结果。",
    "成本效益": "多用来比较值唔值、划唔划算，工作场景尤其常见。",
    "表情管理": "多用来讲人要唔要收住面色，或者镜头前控制表情。",
    "最近": "多放句首讲近排情况，或者讲某件事离而家有几近。",
    "覺形": "多用来讲自己大概感觉到个轮廓，未必已经完全睇清。",
    "節奏": "多用在讲说话、做事、行程或者音乐快慢点样安排。",
    "韻母": "多用在讲一个音节后半部分，或者比较两个音尾有咩分别。",
    "改善": "多用来讲状态、做法或者表现慢慢变好。",
    "應該": "多用在判断句里，表示按道理会系咁或者应该咁做。",
    "同人": "多用在讲自己同别人一齐做嘢、倾偈或者比较时。",
}

EXPRESSION_USAGE_OVERRIDES = {
    "冇乜嘢": "多用来回应别人关心，表示冇大碍、唔使太担心。",
    "唔係咁講": "多放在纠正讲法、补充自己真正意思之前。",
    "做乜嘢": "多用来追问对方点解要咁做，语气可以平和也可以带火。",
    "嚟唔切": "多用在赶时间、赶车、交嘢赶唔上的场景。",
    "咩風吹你嚟": "多用在熟人突然出现时，带少少惊喜或者打趣。",
    "有嗰句講嗰句": "多放在准备讲真话、直说自己看法之前。",
}

GENERATED_WORD_EXAMPLE_OVERRIDES = {
    "善解人意": "佢好善解人意，我未讲完佢就知我想点。",
    "心理關口": "你过到自己个心理關口，后面就会顺好多。",
    "本能反應": "见到热嘢弹埋来，缩手系本能反應。",
    "自然反應": "突然听到爆响，转头望过去系自然反應。",
    "通情達理": "佢好通情達理，讲清楚之后就会明白。",
    "自作自受": "你之前唔听人讲，而家出事都算自作自受。",
    "一本正經": "佢讲笑都一本正經，搞到人分唔清真假。",
    "人工智能": "而家好多公司都用人工智能处理资料。",
    "人心肉做": "你讲嘢唔好咁尽，人心肉做㗎。",
    "人際關係": "做团队合作，人際關係处理得好好紧要。",
    "個人資料": "交表之前，记得再核对一次個人資料。",
    "分工合作": "今次活动靠大家分工合作先搞得掂。",
    "心安理得": "你咁样推责任比人，都真系心安理得。",
    "心理準備": "医生叫佢先做好心理準備，再听报告。",
    "成本效益": "呢个方案成本效益高，老板会容易接受。",
    "目定口呆": "我听到个价钱即刻目定口呆。",
    "知錯能改": "人最紧要知錯能改，唔系死撑。",
    "自作多情": "你唔好咁快入戏，费事最后变成自作多情。",
    "表情管理": "开会时记得做好表情管理，唔好全部写晒喺块面。",
}

GENERATED_EXPRESSION_EXAMPLE_OVERRIDES = {
    "冇乜嘢": "你放心啦，我冇乜嘢。",
    "嗰啲嘢": "嗰啲嘢你唔使理，我自己搞掂。",
    "要乜冇乜": "呢间铺要乜冇乜，真系唔掂。",
    "乜嘢料呀": "新嚟嗰个咁自信，到底乜嘢料呀？",
    "平嘢冇好嘢": "我一早话平嘢冇好嘢，而家坏咗啦。",
    "冇咁好氣": "我今日冇咁好氣，你唔好再搞我。",
    "唔係咁講": "唔係咁講，我意思系要再睇清楚先。",
    "話冇咁快": "你而家问结果？我都話冇咁快啦。",
    "話冇咁易": "想一日内搞掂？話冇咁易。",
    "做乜嘢": "你无啦啦笑成咁，做乜嘢？",
    "冇佢符": "我同佢讲咗几次都唔听，真系冇佢符。",
    "嚟唔切": "快啲啦，再慢就嚟唔切上车。",
    "乜嘢環境": "一开门见到咁乱，我都想问乜嘢環境。",
    "冇嘢好講": "你今次做成咁好，我真系冇嘢好講。",
    "有乜唔妥": "你由头到尾黑晒面，系咪有乜唔妥？",
    "唔理得咁多": "而家先救人要紧，唔理得咁多啦。",
    "咩風吹你嚟": "你平时都唔出现，今日咩風吹你嚟？",
    "有嗰句講嗰句": "有嗰句講嗰句，我觉得呢个做法唔稳阵。",
    "嚟嚟去去": "我哋倾咗成晚，嚟嚟去去都系嗰几个方案。",
    "上氣唔接下氣": "佢跑上嚟嗰阵上氣唔接下氣，连说话都断断续续。",
}

WORD_SUFFIX_GLOSSES = {
    "反應": "指遇到事情时自然做出的反应。",
    "關係": "指人与人之间的关系，或者事情之间嘅联系。",
    "資料": "指登记、工作或个人相关的资料和信息。",
    "合作": "指几个人分工配合，一齐完成事情。",
    "準備": "指事前先有心理准备或者实际安排。",
    "效益": "指投入同结果之间值唔值、划唔划算。",
    "管理": "指控制、整理或者维持好某方面状态。",
    "關口": "比喻心理上或者过程上要跨过的一关。",
    "現狀": "指眼前目前嘅状况。",
    "人物": "指某个具体人物，或者被留意嘅对象。",
    "表情": "指人面上表现出来嘅神情。",
    "能力": "指做某件事嘅本事同能力。",
    "方向": "指事情要朝边个方向行。",
}

WORD_SUFFIX_USAGES = {
    "反應": "多用来讲第一下感觉、本能动作或者临场应对。",
    "關係": "多用来讲人与人之间相处、合作，或者事情之间有咩关联。",
    "資料": "多用在登记、交文件、核对信息时。",
    "合作": "开会、做 project、安排分工时好常用。",
    "準備": "多用在做大事之前，先讲自己心理上或实际安排好未。",
    "效益": "多用在比较值唔值、抵唔抵时。",
    "管理": "多用在讲控制状态、整理流程或者收好自己表现时。",
}

QUESTION_MARKERS = ("點", "乜", "咩", "乜嘢")
NEGATIVE_PREFIXES = ("冇", "無", "唔", "未")
EMOTION_MARKERS = ("驚", "嬲", "煩", "慌", "緊張", "心", "意", "情", "氣", "癮", "火", "悶")
WORK_MARKERS = ("工", "資料", "進度", "效益", "方案", "分工", "管理", "成本", "交代", "處理", "收尾")
TIME_MARKERS = ("日", "時", "陣", "近", "即", "終", "刻", "瞬")


def is_low_info_gloss(text: str, display_text: str = "") -> bool:
    stripped = str(text or "").strip()
    if not stripped:
        return True
    if stripped == str(display_text or "").strip():
        return True
    if re.search(r"[A-Za-z]", stripped):
        return True
    return any(marker in stripped for marker in LOW_INFO_GLOSS_MARKERS)


def is_low_info_usage(text: str) -> bool:
    stripped = str(text or "").strip()
    if not stripped:
        return True
    return any(marker in stripped for marker in LOW_INFO_USAGE_MARKERS)


def build_better_gloss(display_text: str, category: str, entry_type: str, source_label: str) -> str:
    if entry_type == "expression":
        return _build_expression_gloss(display_text, category)
    return _build_word_gloss(display_text, category)


def build_better_usage(display_text: str, category: str, entry_type: str, source_label: str) -> str:
    if entry_type == "expression":
        return _build_expression_usage(display_text, category)
    return _build_word_usage(display_text, category)


def build_generated_guidance_text(display_text: str, category: str, entry_type: str) -> str:
    gloss = build_better_gloss(display_text, category, entry_type, "generated")
    usage = build_better_usage(display_text, category, entry_type, "generated")
    lines = [
        f"意思：{gloss}",
        f"用法：{usage}",
    ]
    if entry_type == "expression":
        example = GENERATED_EXPRESSION_EXAMPLE_OVERRIDES.get(display_text)
    else:
        example = GENERATED_WORD_EXAMPLE_OVERRIDES.get(display_text)
    if example:
        lines.append(f"例句：{example}")
    return "\n".join(lines)


def _build_word_gloss(display_text: str, category: str) -> str:
    if display_text in GENERATED_WORD_GLOSS_OVERRIDES:
        return GENERATED_WORD_GLOSS_OVERRIDES[display_text]
    for suffix, gloss in WORD_SUFFIX_GLOSSES.items():
        if display_text.endswith(suffix):
            return gloss
    if display_text.startswith("心理"):
        return "多指人内心感受、心理状态，或者心理上要过嘅关。"
    if display_text.startswith("本能"):
        return "指出于本能，自然出现嘅动作或者反应。"
    if display_text.startswith("自然"):
        return "指顺住情况自然出现嘅反应、状态或者做法。"
    if display_text.startswith("人際"):
        return "指人与人之间点样来往、相处同维持关系。"
    if display_text.startswith("表情"):
        return "同面上神情有关，讲人点样显露或者收住情绪。"
    if display_text.startswith("時間") or any(marker in display_text for marker in TIME_MARKERS):
        return "同时间先后、长短或者临近程度有关。"
    if any(marker in display_text for marker in WORK_MARKERS):
        return "多指工作、安排、资料或者处理方式。"
    if any(marker in display_text for marker in EMOTION_MARKERS):
        return "多用来讲感受、心态、情绪或者当下反应。"
    if "人" in display_text:
        return "多用来形容一个人嘅性格、处事方式，或者人与人之间关系。"
    if len(display_text) >= 4:
        return f"多用来概括一种状态、做法或者结果；重点唔止识读，仲要明白「{display_text}」讲紧咩。"
    return f"常见词，讲紧「{display_text}」呢类情况或者意思。"


def _build_word_usage(display_text: str, category: str) -> str:
    if display_text in WORD_USAGE_OVERRIDES:
        return WORD_USAGE_OVERRIDES[display_text]
    for suffix, usage in WORD_SUFFIX_USAGES.items():
        if display_text.endswith(suffix):
            return usage
    if category == "工作场景":
        return "多用在开会、交代事情、讲方案或者讲进度时。"
    if category == "学习场景":
        return "多用在上堂、提问、复述内容或者解释概念时。"
    if category == "情绪表达":
        return "多用来讲自己感觉点样，或者评价别人当下状态。"
    if category == "时间表达":
        return "多放句首或者动词前，先交代时间先后。"
    if category == "口语场景":
        return "多出现在对话里，用来接话、解释或者补充。"
    return "多放在日常判断句或者叙述句里，讲人、事情、状态或者眼前情况。"


def _build_expression_gloss(display_text: str, category: str) -> str:
    if display_text in GENERATED_EXPRESSION_GLOSS_OVERRIDES:
        return GENERATED_EXPRESSION_GLOSS_OVERRIDES[display_text]
    if any(marker in display_text for marker in QUESTION_MARKERS):
        return "一句追问情况、原因或者来历嘅口语说法。"
    if display_text.endswith("先"):
        return "表示而家先做呢一步，迟啲再算或者先拖住。"
    if display_text.startswith(("冇", "無")):
        return "表示冇出现、冇办法、冇所谓，或者情况唔系咁。"
    if display_text.startswith(("唔", "未")):
        if display_text.endswith("切"):
            return "表示时间上赶唔切，来不及。"
        if display_text.endswith("快"):
            return "表示件事唔会咁快发生。"
        if display_text.endswith("易"):
            return "表示件事一点都唔容易。"
        if display_text.endswith("妥"):
            return "表示有问题、唔对路。"
        return "一句带否定意思嘅口语说法，用来讲唔得、唔要或者唔认同。"
    if "嚟嚟去去" in display_text:
        return "表示翻来覆去都系嗰几样，变化唔大。"
    if category == "俚语表达":
        return "一句好口语嘅讲法，多数用来回应眼前场面、吐槽或者表达态度。"
    if category == "情绪表达":
        return "用来直接讲感觉、火气、紧张或者受唔受得住。"
    if category == "工作场景":
        return "工作上用来讲安排、处理方式或者进度。"
    return "一句对话里好常见嘅口语表达。"


def _build_expression_usage(display_text: str, category: str) -> str:
    if display_text in EXPRESSION_USAGE_OVERRIDES:
        return EXPRESSION_USAGE_OVERRIDES[display_text]
    if any(marker in display_text for marker in QUESTION_MARKERS):
        return "多放在追问、质疑或者确认情况时，前后句通常都唔长。"
    if display_text.endswith("先"):
        return "多放句尾收住语气，表示先咁样、迟啲再算。"
    if display_text.startswith(NEGATIVE_PREFIXES):
        return "多用来否定、拒绝、讲做唔到，或者直接吐槽眼前情况。"
    if category == "俚语表达":
        return "多放在熟人对话、吐槽、插嘴或者即时反应里。"
    if category == "情绪表达":
        return "多用来讲自己顶唔顶得顺、惊唔惊、嬲唔嬲。"
    if category == "工作场景":
        return "多用于讲安排、交代下一步或者收尾。"
    return "多放在真对话语境里，当场回应或者补一句态度。"
