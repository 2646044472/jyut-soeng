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
    "多用来概括一种状态、做法或者结果",
    "常见词，讲紧",
    "一句好口语嘅讲法",
    "通常唔系逐个字照字面解",
    "一个固定词语，要连前后文一齐先容易明白讲紧乜",
    "多数唔系讲字面",
    "呢类讲法通常靠前后文先完整",
    "一句追问情况、原因或者来历嘅口语说法",
    "一句带否定意思嘅口语说法",
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
    "先谂清楚佢通常形容边类人、边种事",
    "多放在日常判断句或者叙述句里",
    "多放在熟人对话、吐槽、插嘴或者即时反应里",
    "多用来讲自己感觉点样，或者评价别人当下状态",
    "多用来否定、拒绝、讲做唔到，或者直接吐槽眼前情况",
    "多放在追问、质疑或者确认情况时，前后句通常都唔长",
    "多半系熟人之间顺口爆出来",
    "多系当场拒绝、讲做唔到",
    "通常系跟住眼前情况顺口讲出",
    "多数系讲完件事之后",
)

FAKE_EXAMPLE_PREFIXES = ("意思：", "用法：", "例句：")
FAKE_EXAMPLE_FRAGMENTS = (
    "朋友倾偈时，可以直接讲",
    "先用「",
    "先用\"",
    "讲到呢一步",
    "当场回应或者补一句态度",
    "朋友見到眼前個情況",
    "真係遇到嗰下，講句",
    "你問我點睇，我只可以講句",
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
    "差唔多": "表示大致上已经到位，或者离完成只差少少。",
    "走唔甩": "表示点都避唔开，迟早都要面对或者中招。",
    "做唔住": "表示再咁落去撑唔住，做唔落手或者顶唔顺。",
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


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def _match_reduplicated_dei(display_text: str) -> str:
    if not display_text.endswith("哋"):
        return ""
    core = display_text[:-1]
    if len(core) < 2 or len(core) % 2 != 0:
        return ""
    half = len(core) // 2
    if core[:half] != core[half:]:
        return ""
    return core[:half]


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


def is_fake_example_sentence(text: str, display_text: str = "") -> bool:
    stripped = str(text or "").strip()
    if not stripped:
        return True
    if stripped == str(display_text or "").strip():
        return True
    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    if not lines:
        return True
    if any(line.startswith(FAKE_EXAMPLE_PREFIXES) for line in lines):
        return True
    return any(fragment in stripped for fragment in FAKE_EXAMPLE_FRAGMENTS)


def build_better_gloss(display_text: str, category: str, entry_type: str, source_label: str) -> str:
    if entry_type == "expression":
        return _build_expression_gloss(display_text, category)
    return _build_word_gloss(display_text, category)


def build_better_usage(display_text: str, category: str, entry_type: str, source_label: str, gloss: str = "") -> str:
    if entry_type == "expression":
        return _build_expression_usage(display_text, category, gloss)
    return _build_word_usage(display_text, category, gloss)

def build_better_example(
    display_text: str,
    category: str,
    entry_type: str,
    gloss: str,
    usage: str,
) -> str:
    if entry_type == "expression":
        return _build_expression_example(display_text, category, gloss, usage)
    return _build_word_example(display_text, category, gloss, usage)


def _build_word_gloss(display_text: str, category: str) -> str:
    if display_text in GENERATED_WORD_GLOSS_OVERRIDES:
        return GENERATED_WORD_GLOSS_OVERRIDES[display_text]
    if display_text.endswith("經理人"):
        return "负责帮艺人、运动员或者创作者接工作、谈安排嗰个人。"
    if display_text.endswith("方向感"):
        return "指人识唔识分方向、会唔会容易迷路。"
    if display_text.endswith("成功感"):
        return "做成一件事之后，心里面觉得满足又有成就。"
    if display_text.endswith("節奏感"):
        return "对快慢、停顿同轻重有感觉，知道点样先顺。"
    if display_text.endswith("閱讀理解"):
        return "读完一段文字之后，明唔明里面真正讲紧咩。"
    if display_text.endswith("選擇題"):
        return "畀你喺几个答案入面拣一个嘅题型。"
    if display_text.endswith("反效果"):
        return "本来想帮手，结果做完反而更差。"
    if display_text.endswith("反方向"):
        return "同原本目标相反嘅方向。"
    if display_text.endswith("反間計"):
        return "故意放消息或者设局，令对方自己人互相猜疑。"
    if display_text.endswith("情意結"):
        return "对某个人、旧事或者某段经历长期放唔低。"
    for suffix, gloss in WORD_SUFFIX_GLOSSES.items():
        if display_text.endswith(suffix):
            return gloss
    if display_text.startswith("心理"):
        return "指人内心点谂、点感受，或者心理上过唔过到某一关。"
    if display_text.startswith("本能"):
        return "指出于本能，自然出现嘅动作或者反应。"
    if display_text.startswith("自然"):
        return "指顺住情况自然出现嘅反应、状态或者做法。"
    if display_text.startswith("人際"):
        return "指人与人之间点样来往、相处同维持关系。"
    if display_text.startswith("表情"):
        return "同面上神情有关，讲人点样显露或者收住情绪。"
    if _contains_any(display_text, ("講", "話", "口", "問", "答", "聲")):
        return "同讲话方式、当场点回应人，或者把口讲出来嘅效果有关。"
    if _contains_any(display_text, ("情", "心", "意", "感", "緒")):
        return "同人内心点谂、受唔受影响，或者对人对事有咩感觉有关。"
    if _contains_any(display_text, ("法", "律", "院", "權", "幣", "規")):
        return "同规则、法律、权责或者制度点样运作有关。"
    if _contains_any(display_text, ("學", "課", "術", "題", "讀", "寫", "考")):
        return "同学习、考试、知识内容，或者理解吸收做成点有关。"
    if _contains_any(display_text, ("程", "式", "機", "器", "電", "資", "料", "工")):
        return "同工具、系统、资料处理，或者做事流程点样运作有关。"
    if display_text.startswith("時間") or any(marker in display_text for marker in TIME_MARKERS):
        return "同时间先后、长短，或者件事几快发生有关。"
    if any(marker in display_text for marker in WORK_MARKERS):
        return "多讲工作点样分工、跟进、处理，或者做法值唔值得继续。"
    if any(marker in display_text for marker in EMOTION_MARKERS):
        return "多讲人当下个情绪、心口顶唔顶得顺，或者受刺激后会点反应。"
    if "人" in display_text:
        return "多讲一个人做人做事嘅样、同人点相处，或者畀人点样睇。"
    if len(display_text) >= 4:
        return "多半系整组连住用，讲一个完整判断、结果或者状态。"
    return "要连埋前后文先最容易听得出，讲紧边种情况。"


def _build_word_usage(display_text: str, category: str, gloss: str = "") -> str:
    if display_text in WORD_USAGE_OVERRIDES:
        return WORD_USAGE_OVERRIDES[display_text]
    for suffix, usage in WORD_SUFFIX_USAGES.items():
        if display_text.endswith(suffix):
            return usage
    if "形容人" in gloss:
        return f"多用来评价一个人处事点样；赞人定踩人，要睇前后文。"
    if "自己搞出来的后果" in gloss or "自己用错做法" in gloss:
        return "多用来追住件后果讲，语气通常带少少责备或者无奈。"
    if "一时冲动" in gloss:
        return "多用来劝人唔好俾脾气带住走，或者事后解释点解会做错决定。"
    if "知道自己斤两" in gloss or "识得自量" in gloss:
        return "多用来提醒人先认清自己位置，唔好高估自己。"
    if "经过一轮努力之后" in gloss:
        return "多用在长期努力后终于有成果嗰下，讲得会有种苦尽甘来嘅感觉。"
    if "结果超出一般预料" in gloss or "结果超出想像" in gloss:
        return "多放在结果句后面，强调件事比原先估计更夸张或者更突然。"
    if "守住自己本分" in gloss:
        return "多用来讲一个人知分寸、唔越界，职场同家庭场景都常见。"
    if "平安顺利咁捱过" in gloss:
        return "多用在病痛、风险或者困难时期，讲最后总算平安过关。"
    if "引导人朝住好嘅方向" in gloss:
        return "多用来评价老师、长辈、作品或者环境对人有正面影响。"
    if "按对象需要特别订做" in gloss:
        return "多用来讲方案、衣服、训练计划呢类专门为某个人整嘅嘢。"
    if "一身正气" in gloss or "堂堂正正" in gloss:
        return "多用来赞人企得正、唔怕事，成个人好有骨气。"
    if "被重点留意" in gloss or "跟进或者针对" in gloss:
        return "多出现在调查、保安或者新闻语境，讲边个已经被盯上。"
    if "识得拣啱人" in gloss:
        return "多用来赞带队嗰个人识用人，安排得啱位。"
    if "知道自己错咗" in gloss and "愿意改正" in gloss:
        return "多用来评价人肯认错、肯改，比死撑顺眼好多。"
    if "读完一段文字之后" in gloss:
        return "多用在上堂、考试或者补习时，讲一个人睇文章明唔明。"
    if "做完反而更差" in gloss:
        return "多用来批评做法帮倒忙，本来想救，结果越搞越衰。"
    if "相反嘅方向" in gloss or "相反方向" in gloss:
        return "多用在行路、开车或者讲思路走歪时，提醒人已经行错边。"
    if "长期放唔低" in gloss:
        return "多用来讲旧情、旧怨或者心结，一路都未完全放低。"
    if "心里面觉得满足又有成就" in gloss:
        return "多用在做成一件事之后，讲嗰种『辛苦都值返』嘅感觉。"
    if "分方向" in gloss or "容易迷路" in gloss:
        return "多用来讲人识唔识认路，去到陌生地方会唔会乱。"
    if "对快慢、停顿同轻重有感觉" in gloss:
        return "多用来讲说话、唱歌、跳舞或者做动作够唔够顺。"
    if "负责帮艺人" in gloss:
        return "多用在娱乐圈、体育或者商务合作场景，讲负责接洽工作嗰个人。"
    if "畀你喺几个答案入面拣一个" in gloss:
        return "多用在考试、测验或者 app 练习模式，讲题型唔系填空。"
    if "故意放消息或者设局" in gloss:
        return "多用来讲斗争、计谋或者剧情里面挑拨离间嘅做法。"
    if category == "工作场景":
        return "多系开会、分工、讲方案或者追进度时会讲出口。"
    if category == "学习场景":
        return "多用喺上堂、考试、做练习或者解释概念嗰阵。"
    if category == "情绪表达":
        return "自己紧张、火滚、委屈，或者想讲别人个状态时就会用到。"
    if category == "时间表达":
        return "通常摆喺句头或者动词前面，先讲明几时发生。"
    if category == "口语场景":
        return "多半系接住对方嗰句再补充，等语气听落去冇咁书面。"
    return f"通常会跟住前面件事一齐讲，用「{display_text}」概括最后个状态、判断或者结果。"


def _build_word_example(display_text: str, category: str, gloss: str, usage: str) -> str:
    if display_text in GENERATED_WORD_EXAMPLE_OVERRIDES:
        return GENERATED_WORD_EXAMPLE_OVERRIDES[display_text]
    if display_text.endswith("關係"):
        return f"做嘢唔只睇能力，{display_text}都好重要。"
    if display_text.endswith("資料"):
        return f"交表之前，記得再核對一次{display_text}。"
    if display_text.endswith("合作"):
        return f"今次活動靠大家{display_text}先搞得掂。"
    if display_text.endswith("準備"):
        return f"聽日要見客，你今晚最好先做好{display_text}。"
    if display_text.endswith("效益"):
        return f"老細最關心呢個方案有冇{display_text}。"
    if display_text.endswith("管理"):
        return f"見客之前做好{display_text}，塊面唔好咁多戲。"
    if display_text.endswith("關口"):
        return f"你過到自己個{display_text}，後面就會順好多。"
    if display_text.endswith("方向"):
        return f"我而家最想先定好個{display_text}。"
    if display_text.endswith("能力"):
        return f"做呢份工，{display_text}真係好重要。"
    if display_text.endswith("反應"):
        return f"一聽到爆響，佢第一個{display_text}就係擰轉頭。"
    if display_text.endswith("現狀"):
        return f"如果一直停喺{display_text}，就好難再進步。"
    if display_text.endswith("人物"):
        return f"警方而家已經將佢列做{display_text}。"
    if display_text.endswith("表情"):
        return f"佢聽完整件事都冇乜{display_text}。"
    if "形容人" in gloss:
        return f"佢真係{display_text}，相處落去會舒服好多。"
    if "自己搞出来的后果" in gloss or "自己搞出來的後果" in gloss or "自己搞出嚟嘅後果" in gloss:
        return f"件事搞成咁，都算係{display_text}。"
    if "超出" in gloss and "预料" in gloss:
        return f"個結果真係{display_text}，全場都估唔到。"
    if "一时冲动" in gloss or "一時衝動" in gloss:
        return f"你唔好因為{display_text}就亂咁應承人。"
    if "守住自己本分" in gloss:
        return f"喺公司做好自己份內事，{display_text}已經唔簡單。"
    if "平安顺利" in gloss or "平安順利" in gloss:
        return f"希望屋企人今次都可以{display_text}。"
    if category == "工作场景":
        return f"开会倾到卡住嗰阵，大家就会开始讲{display_text}。"
    if category == "学习场景":
        return f"老师讲到呢部分，会特登停低解释{display_text}。"
    if category == "情绪表达":
        return f"听完佢咁讲，我有呢种{display_text}都好正常。"
    if category == "进阶表达":
        return f"件事发展到呢一步，用{display_text}去形容最贴。"
    return f"而家个情况几明显，用{display_text}去讲会最顺口。"


def _build_expression_gloss(display_text: str, category: str) -> str:
    if display_text in GENERATED_EXPRESSION_GLOSS_OVERRIDES:
        return GENERATED_EXPRESSION_GLOSS_OVERRIDES[display_text]
    dei_base = _match_reduplicated_dei(display_text)
    if dei_base:
        return f"表示有少少「{dei_base}」嗰种倾向或者感觉，未去到好严重。"
    if display_text.startswith("唔使"):
        return "表示件事唔需要做，或者叫对方唔好白担心、白费心机。"
    if display_text.startswith("唔知"):
        return "表示完全唔清楚情况、摸唔到门路，或者估唔到点会搞成咁。"
    if display_text.startswith("唔好"):
        return "用来劝人唔好咁做，或者先打个底提醒后果会唔好。"
    if display_text.startswith("唔夠"):
        return "表示数量、火候、能力或者气势差一截，未够班。"
    if display_text.startswith("唔啱"):
        return "表示唔合适、唔夹，摆埋一齐点都唔顺。"
    if display_text.startswith("唔怪"):
        return "表示『难怪会咁』，后面通常接一个已经出现咗嘅结果。"
    if display_text.startswith("唔關"):
        return "表示同某个人或某件事无关，唔好乱咁拉埋一齐。"
    if display_text.startswith("冇得"):
        return "表示已经冇条件、冇空间再做后面嗰步，只可以死心或者认数。"
    if display_text.startswith("冇幾"):
        return "表示数量唔多、时间唔长，或者呢种情况其实好少出现。"
    if display_text.startswith("冇聲"):
        return "表示静晒冇回应，或者人成个虚晒，连声都出唔到。"
    if display_text.startswith("冇厘"):
        return "表示一点都冇后面嗰种样、状态或者心机。"
    if display_text.startswith("冇奶油"):
        return "表示点谂都觉得冇可能，太离谱，根本唔信会发生。"
    if display_text.startswith("冇家教"):
        return "闹人冇礼貌、冇分寸，做法似系屋企冇教好。"
    if display_text.startswith(("冇辦法", "冇法子")):
        return "表示真系冇其他办法，只可以硬食眼前安排。"
    if display_text.startswith("冇理由"):
        return "表示照计唔应该会咁，带住『点会咁㗎』嘅语气。"
    if display_text.startswith("冇相干"):
        return "表示同件事拉唔上关系，完全唔关事。"
    if any(marker in display_text for marker in QUESTION_MARKERS):
        return "用来追问对方到底想点、发生乜事，或者确认自己有冇听错。"
    if "咁" in display_text:
        if display_text.endswith("口"):
            return "形容个口形、表情或者个呆样夸张到一眼就睇得出。"
        if display_text.endswith("眼"):
            return "形容眼神、望人个样或者双眼状态好有画面。"
        if display_text.endswith("聲"):
            return "形容把声听落古怪、尖细、扭拧或者特别难听。"
        if display_text.endswith("手"):
            return "形容出手动作、手势或者做嘢手法有种特别嘅样。"
        if display_text.endswith("舞"):
            return "形容动作夸张、周身郁动，做起来唔会静定。"
        if display_text.endswith("食"):
            return "形容食相或者反应夸张，好似进入咗某种状态。"
        if "大場面" in display_text:
            return "形容场面阵仗夸张，排场大到过晒火位。"
        if display_text.endswith("腳"):
            return "形容脚步、动作或者走位急急脚，郁得特别快。"
        if display_text.endswith("早"):
            return "形容时间早得夸张，早到令人唔想起身。"
        if display_text.endswith("多"):
            return "形容数量多定少去到某个夸张程度，一讲就有画面。"
        if display_text.endswith("亂"):
            return "形容现场、摆位或者做法乱成一团。"
        if display_text.endswith("蠢"):
            return "直接闹人蠢得夸张，做法令人睇到摇头。"
        if display_text.endswith("遠"):
            return "形容距离远到夸张，去一转都嫌辛苦。"
        return "用一个好有画面嘅比喻，讲个样、动作或者程度夸张成点。"
    if "嚟" in display_text and "去" in display_text:
        return "表示来来回回重复同一个动作、状态或者过程。"
    if "頭" in display_text and "尾" in display_text:
        return "同开头结尾、前因后果或者做事收尾有关。"
    if "有" in display_text and "冇" in display_text:
        return "表示一边有、一边冇，前后状态唔平衡或者唔完整。"
    if "心" in display_text and "口" in display_text:
        return "同心里面点谂、把口点讲，前后系咪一致有关。"
    if display_text.endswith("先"):
        return "表示而家先做呢一步，迟啲再算或者先拖住。"
    if display_text.startswith(("冇", "無")):
        return "表示真系欠缺后面嗰样条件、分寸、本事或者后着，唔系单纯讲『冇』。"
    if display_text.startswith(("唔", "未")):
        if display_text.endswith("切"):
            return "表示时间上赶唔切，来不及。"
        if display_text.endswith("快"):
            return "表示件事唔会咁快发生。"
        if display_text.endswith("易"):
            return "表示件事一点都唔容易。"
        if display_text.endswith("妥"):
            return "表示有问题、唔对路。"
        return "表示后面嗰样唔成立、唔够，或者成件事根本行唔通。"
    if "嚟嚟去去" in display_text:
        return "表示翻来覆去都系嗰几样，变化唔大。"
    if category == "俚语表达":
        return "多用来当场形容人个样、件事离唔离谱，或者顺手爆一句表达态度。"
    if category == "情绪表达":
        return "直接讲人受唔受得住、个心情顶唔顶得顺，情绪会出得几明显。"
    if category == "工作场景":
        return "多同做法、安排、收尾或者现场处理手法有关。"
    return "通常一句就讲中个态度、判断或者反应，熟人对话特别常见。"


def _build_expression_usage(display_text: str, category: str, gloss: str = "") -> str:
    if display_text in EXPRESSION_USAGE_OVERRIDES:
        return EXPRESSION_USAGE_OVERRIDES[display_text]
    dei_base = _match_reduplicated_dei(display_text)
    if dei_base:
        return "多用来轻轻形容人个样、状态或者感觉有少少偏向后面嗰样，未算好重。"
    if display_text.startswith(("嗰個", "嗰隻", "嗰啲")):
        return "一时谂唔起个名，或者懒得讲到太白时，就会用呢类讲法笼统带过。"
    if display_text.startswith("唔使"):
        return "多用来叫停对方，话畀人知唔需要再做，或者唔使再谂咁多。"
    if display_text.startswith("唔知"):
        return "多用在一头雾水、唔识点入手，或者对眼前情况完全冇底时。"
    if display_text.startswith("唔夠"):
        return "多用来讲份量、能力、耐性或者火候未够，差少少先到位。"
    if display_text.startswith("冇得"):
        return "多用在局势已经定咗、后路封晒嗰阵，讲咩都要面对现实。"
    if display_text.startswith("冇幾"):
        return "多用来讲次数少、时间短，或者『其实唔係成日会咁』。"
    if display_text.startswith("冇聲"):
        return "多用在对方突然冇反应、全场静晒，或者人成个攰到虚脱嗰阵。"
    if display_text.startswith("冇厘"):
        return "多用来踩人冇心机、冇精神、冇个样，语气通常几口语。"
    if display_text.startswith(("冇辦法", "冇法子")):
        return "多用在明知唔想都要照做，或者真系冇第二条路嗰阵。"
    if display_text.startswith("冇理由"):
        return "多用在觉得件事太离谱，直觉上完全唔合理嗰阵。"
    if display_text.startswith("冇相干"):
        return "多用来划清界线，讲某个人某件事唔应该被扯埋落水。"
    if "平价货通常冇好品质" in gloss:
        return "买平价货出事、质量差或者后悔悭错钱时最常讲。"
    if "再差都唔会差到咁" in gloss:
        return "多用来顶唔顺个情况太离谱，语气夸张得嚟又带吐槽。"
    if "扮得好似" in gloss:
        return "多用来讲人学人学得似，语气可以系赞都可以系笑佢。"
    if "由以前到而家呢段时间" in gloss:
        return "多放句首或者句中，先交代呢段时间一路都系咁。"
    if "唔会咁快发生" in gloss:
        return "多用来叫人唔好催咁紧，件事冇可能即刻有结果。"
    if "冇想像中咁容易" in gloss:
        return "多用来泼一泼冷水，提醒人唔好将件事睇得太简单。"
    if "奈佢唔何" in gloss:
        return "多用来讲一个人好难搞，点劝点闹都冇反应。"
    if "大致上已经到位" in gloss:
        return "多用在收尾、对数或者睇完成品时，表示八九不离十。"
    if "太得闲" in gloss:
        return "多用来笑人无聊生事，冇事搵事做。"
    if "翻来覆去都系嗰几个" in gloss:
        return "多用在开会、拣方案或者日常抱怨，讲来讲去都冇新意。"
    if "喘到接唔上气" in gloss:
        return "跑完、赶完路或者爬楼梯之后，形容自己喘到讲唔到完整句。"
    if "只会搞乱档" in gloss or "帮唔到手" in gloss:
        return "多用来闹人净系搞事唔帮手，越插手越乱。"
    if "突然出现" in gloss:
        return "多用在熟人好耐冇见，突然蒲头时打趣一句。"
    if "照直讲心里话" in gloss:
        return "多放在准备直讲意见之前，先打个底话自己唔兜圈。"
    if "点激都激佢唔到" in gloss:
        return "多用来讲对方面皮厚或者完全唔受你影响。"
    if "听唔清楚" in gloss:
        return "听漏咗、太突然，或者怀疑自己听错时会即刻追问。"
    if "无话可说" in gloss or "冇話可講" in gloss:
        return "多用来表示服咗、顶唔顺，或者见到个结果真系讲唔出声。"
    if any(marker in display_text for marker in QUESTION_MARKERS):
        return "多系听到某件事即刻反问一句，想追究原因或者确认自己有冇听错。"
    if "咁" in display_text:
        return "通常系见到个样、个动作或者个程度好夸张时，顺手拎个比喻嚟讲，会比直白讲法更有画面。"
    if "嚟" in display_text and "去" in display_text:
        return "多用喺讲人重复郁嚟郁去、谂嚟谂去，或者件事来回折腾停唔落嚟。"
    if "頭" in display_text and "尾" in display_text:
        return "多用喺讲前因后果、做事手尾或者想由头到尾睇清楚嗰阵。"
    if "有" in display_text and "冇" in display_text:
        return "多用嚟点出前后唔平衡，一边有料，另一边就差一截。"
    if "心" in display_text and "口" in display_text:
        return "多用喺讲人真心定假意，或者把口同心里面谂法系咪一致。"
    if display_text.endswith("先"):
        return "通常摆句尾，表示而家先咁处理，下一步迟啲再讲。"
    if display_text.startswith(NEGATIVE_PREFIXES):
        return "多用来直接表明唔赞成、唔接受，或者指出眼前个情况根本行唔通。"
    if category == "俚语表达":
        return "多用喺熟人之间讲人个样、顶一句嘴，或者见到离谱场面时即刻爆出嚟。"
    if category == "情绪表达":
        return "多用喺情绪顶到上心口嗰阵，想直接交代自己而家顶唔顶得住。"
    if category == "工作场景":
        return "多用来交代下一步点做、边个跟进，或者现场要点样收科。"
    return f"通常系见到个情况啱啱好中晒，就顺手用「{display_text}」讲中个意思。"


def _build_expression_example(display_text: str, category: str, gloss: str, usage: str) -> str:
    if display_text in GENERATED_EXPRESSION_EXAMPLE_OVERRIDES:
        return GENERATED_EXPRESSION_EXAMPLE_OVERRIDES[display_text]
    dei_base = _match_reduplicated_dei(display_text)
    if dei_base:
        return f"我觉得佢今日有啲{display_text}，同平时唔係几一样。"
    if display_text.startswith("唔使"):
        return f"呢啲我自己搞得掂，{display_text}你帮手。"
    if display_text.startswith("唔知"):
        return f"第一次去嗰边开会，我真系{display_text}。"
    if display_text.startswith("唔夠"):
        return f"你而家仲{display_text}，再练多几次先上场啦。"
    if display_text.startswith("冇得"):
        return f"老板都拍板咗，而家{display_text}再改。"
    if display_text.startswith("冇幾"):
        return f"呢种机会{display_text}会再嚟，你谂清楚先。"
    if display_text.startswith("冇聲"):
        return f"我讲完成个计划之后，佢即刻{display_text}。"
    if display_text.startswith(("冇辦法", "冇法子")):
        return f"巴士停驶，我都{display_text}，唯有搭的士。"
    if display_text.startswith("冇理由"):
        return f"讲好咗一齐去，佢{display_text}临时放飞机㗎。"
    if display_text.startswith("冇相干"):
        return f"呢件事同阿May{display_text}，你唔好拉埋佢落水。"
    if display_text.startswith("冇乜"):
        return f"佢問我有冇事，我話{display_text}。"
    if display_text.startswith(("冇", "無")) and "大用" in display_text:
        return f"呢招對佢嚟講{display_text}，不如諗第二個辦法。"
    if display_text.startswith("冇奶油"):
        return "你叫我而家先由头再做过，冇奶油啦。"
    if display_text.startswith("冇交易"):
        return "你想我临收工先再改第三次？冇交易。"
    if display_text.startswith("冇下扒"):
        return "你而家先叫我一个人顶晒成单嘢，我真系冇下扒。"
    if display_text.startswith("冇了賴"):
        return "讲到证据都摆埋出嚟，佢仲想赖，根本冇了賴。"
    if display_text.startswith("冇你符"):
        return "同佢讲咗成晚都唔听，我真系冇你符。"
    if display_text.startswith("冇來由"):
        return "佢无啦啦黑晒面，真系冇來由。"
    if display_text.startswith("冇分寸"):
        return "喺长辈面前咁样讲笑，真系太冇分寸。"
    if display_text.startswith("冇命賠"):
        return "叫我揸到咁快？我真系冇命賠。"
    if display_text.startswith("冇埞企"):
        return "成屋人都企晒出嚟，逼到我冇埞企。"
    if display_text.startswith("冇定性"):
        return "佢份份工都做唔够三个月，真系几冇定性。"
    if display_text.startswith("冇定準"):
        return "佢今日讲东听日讲西，完全冇定準。"
    if display_text.startswith("冇家教"):
        return "食饭一路拣餸一路拍枱，真系冇家教。"
    if display_text.startswith("冇彎轉"):
        return "呢条路行到尾先发觉冇彎轉，要原路折返。"
    if display_text.startswith("冇情講"):
        return "一到计钱嗰阵，老板真系冇情講。"
    if display_text.startswith("冇把炮"):
        return "连个时间都未夹好就话搞活动，成件事冇把炮。"
    if display_text.startswith("冇為意"):
        return "头先太赶，我真系冇為意你已经走咗。"
    if display_text.startswith("冇省起"):
        return "你唔提我都冇省起，原来听日要交租。"
    if display_text.startswith("冇着落"):
        return "份工仲未有回音，我个心一直冇着落。"
    if display_text.startswith("冇研究"):
        return "股票嗰啲我冇研究，你问第二个好过。"
    if display_text.startswith(("冇", "無")):
        return f"件事搞成咁，真系{display_text}。"
    if display_text.startswith(("唔", "未")) and any(marker in display_text for marker in QUESTION_MARKERS):
        return f"你无啦啦咁样做，我即刻问你：{display_text}？"
    if display_text.startswith(("唔", "未")):
        return f"我而家真係{display_text}，你等我缓一缓先。"
    if any(marker in display_text for marker in QUESTION_MARKERS):
        return f"见到个场面咁古怪，我第一句就问：{display_text}？"
    if "咁" in display_text:
        if display_text.endswith("口"):
            return f"佢一聽到個消息就{display_text}，成句嘢都講唔出。"
        if display_text.endswith("眼"):
            return f"你唔好再{display_text}望住我啦，有嘢就直接講。"
        if display_text.endswith("聲"):
            return f"佢今日成把聲都{display_text}，聽到人好辛苦。"
        if display_text.endswith("手"):
            return f"佢一緊張就{display_text}，連杯水都拎唔穩。"
        if display_text.endswith("舞"):
            return f"你唔使{display_text}啦，講清楚重點就得。"
        if display_text.endswith("食"):
            return f"佢餓到{display_text}，兩啖就食晒個飯盒。"
        if "大場面" in display_text:
            return f"食個飯啫，唔使搞到{display_text}。"
        if display_text.endswith("腳"):
            return f"一聽到有人叫，佢即刻{display_text}走咗。"
        if display_text.endswith("早"):
            return f"你{display_text}打嚟，我仲未瞓醒。"
        if display_text.endswith("多"):
            return f"得{display_text}，點夠大家分。"
        return f"个场面夸张成咁，我真系会讲{display_text}。"
    if "嚟" in display_text and "去" in display_text:
        return f"佢成晚{display_text}，完全坐唔定。"
    if "頭" in display_text and "尾" in display_text:
        return f"你先{display_text}睇清楚，費事漏咗重點。"
    if "有" in display_text and "冇" in display_text:
        return f"佢做嘢成日{display_text}，睇落去點都唔平衡。"
    if "心" in display_text and "口" in display_text:
        return f"你個樣都寫晒出嚟，擺明就係{display_text}。"
    if display_text.endswith("先"):
        return f"我而家未得閒，{display_text}。"
    if category == "俚语表达":
        return f"呢下场面一出，我即刻谂起「{display_text}」呢句。"
    if category == "情绪表达":
        return f"佢个样已经说明晒，根本就系{display_text}。"
    return f"个情况一出现，顺口讲{display_text}就最贴地。"
