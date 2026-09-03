#!/usr/bin/env python3
"""Generate a plain, clear Chinese PDF for the New TOEFL one-month sprint plan."""

from pathlib import Path

from fpdf import FPDF

FONT = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
OUT = Path(__file__).resolve().parent / "新托福一个月冲刺计划.pdf"


class PlanPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("cn", "", FONT)
        self.add_font("cn", "B", FONT)
        self.set_margins(16, 16, 16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("cn", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "新托福一个月冲刺计划（97 → 5.5/6）", align="R")
        self.ln(8)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-14)
        self.set_font("cn", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"{self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)

    def _reset_x(self):
        self.set_x(self.l_margin)

    def h1(self, text):
        self._reset_x()
        self.set_font("cn", "B", 18)
        self.multi_cell(0, 10, text)
        self.ln(2)

    def h2(self, text):
        self._reset_x()
        self.ln(3)
        self.set_font("cn", "B", 13)
        self.set_fill_color(240, 240, 240)
        self.multi_cell(0, 8, f"  {text}", fill=True)
        self.ln(2)

    def h3(self, text):
        self._reset_x()
        self.ln(1)
        self.set_font("cn", "B", 11)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def p(self, text):
        self._reset_x()
        self.set_font("cn", "", 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text, indent=6):
        self.set_font("cn", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.epw - indent, 6, f"• {text}")
        self._reset_x()

    def check(self, text, indent=6):
        self.set_font("cn", "", 10)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.epw - indent, 6, f"[ ] {text}")
        self._reset_x()

    def kv_table(self, rows, col_widths=None):
        if col_widths is None:
            n = len(rows[0])
            col_widths = [self.epw / n] * n
        line_h = 5.5
        pad = 1.5
        for i, row in enumerate(rows):
            is_header = i == 0
            self.set_font("cn", "B" if is_header else "", 9)

            # Estimate row height from wrapped lines
            max_lines = 1
            for j, cell in enumerate(row):
                text = f" {cell} "
                # rough wrap count by width
                avail = max(col_widths[j] - 2 * pad, 8)
                chars_per_line = max(int(avail / (self.font_size * 0.9)), 1)
                # Chinese chars ~ font_size wide in this font; use get_string_width
                width = self.get_string_width(text)
                lines = max(1, int(width / avail) + (1 if width % avail else 0))
                # safer: simulate with split by characters
                lines = 1
                acc = ""
                for ch in text:
                    if self.get_string_width(acc + ch) > avail:
                        lines += 1
                        acc = ch
                    else:
                        acc += ch
                max_lines = max(max_lines, lines)
            h = max_lines * line_h + 2

            if self.get_y() + h > self.page_break_trigger:
                self.add_page()
                self.set_font("cn", "B" if is_header else "", 9)

            if is_header:
                self.set_fill_color(45, 45, 45)
                self.set_text_color(255, 255, 255)
            else:
                self.set_fill_color(248, 248, 248) if i % 2 == 0 else self.set_fill_color(255, 255, 255)
                self.set_text_color(0, 0, 0)

            y0 = self.get_y()
            x0 = self.l_margin
            # draw backgrounds/borders first
            for j in range(len(row)):
                self.rect(x0 + sum(col_widths[:j]), y0, col_widths[j], h, style="DF")
            # draw text
            for j, cell in enumerate(row):
                self.set_xy(x0 + sum(col_widths[:j]) + pad, y0 + 1)
                self.multi_cell(col_widths[j] - 2 * pad, line_h, str(cell), border=0)
            self.set_xy(x0, y0 + h)
        self.set_text_color(0, 0, 0)
        self.set_x(self.l_margin)
        self.ln(3)

    def day_block(self, title, items):
        self.h3(title)
        for item in items:
            self.check(item)


def build():
    pdf = PlanPDF()
    pdf.add_page()

    # Cover
    pdf.h1("新托福一个月冲刺计划")
    pdf.set_font("cn", "B", 14)
    pdf.multi_cell(0, 8, "旧托福 97  →  新托福总分 5.5（冲刺 6）")
    pdf.ln(2)
    pdf.p("这份 PDF 把四周怎么练写清楚：先定目标，再按周执行。主目标是总分 5.5；6 分只作冲刺上限。")
    pdf.p("核心原则：新制总分 = 四科平均后四舍五入到 0.5。偏科会被拖死——每天追四科均衡，不追单科虚高。")

    pdf.h2("一、你现在在哪，要到哪")
    pdf.kv_table(
        [
            ["项目", "对应关系"],
            ["旧托福 97", "约新制 5.0（CEFR C1 门槛）"],
            ["主目标 5.5", "约旧制 107+，四科都要稳在高分段"],
            ["冲刺 6", "约旧制 114+，容错极低，一个月内作上限"],
        ],
        col_widths=[45, pdf.epw - 45],
    )
    pdf.p("安全过线示例：5.5 + 5.5 + 5.0 + 5.0 = 平均 5.25 → 总分 5.5")
    pdf.p("偏科吃亏示例：6 + 6 + 5.0 + 4.5 = 平均 5.375 → 总分仍可能只有 5.5；短板会卡死更高分。")
    pdf.p("默认假设：每天有效学习 4–6 小时（按 5 小时排）。常见画像是读/听相对强、说/写相对弱；若相反，把弱科时间对调。")

    pdf.h2("二、新考试必须先搞清的规则")
    pdf.bullet("顺序：阅读 → 听力 → 写作 → 口语（约 1.5–2 小时）")
    pdf.bullet("自适应：只有阅读、听力。Module 1 正确率决定能否进高难 Module 2。冲 5.5/6 几乎必须进 Upper。")
    pdf.bullet("进入 Module 2 后不能返回 Module 1；模块内可用 Review 查漏改答案。")
    pdf.bullet("写作新题：Build a Sentence（造句）+ Write an Email（邮件）+ Academic Discussion（学术讨论）")
    pdf.bullet("口语新题：Listen and Repeat（听音复述）+ Take an Interview（模拟面试，约 45 秒/题）")
    pdf.bullet("客观题心态：冲 5.5 大约最多错约 3 题量级；冲 6 大约最多错约 1 题。几乎不能送分。")

    pdf.h2("三、四周总节奏")
    pdf.kv_table(
        [
            ["周次", "主题", "你要交出什么"],
            ["Week 1", "诊断 + 新题型上手", "摸底、错题画像、说写模板成型"],
            ["Week 2", "自适应攻关 + 输出提分", "Module1 正确率拉高；说写稳在 5.5 档"],
            ["Week 3", "全真节奏 + 弱项加压", "隔日全真；口语流利与听口联动"],
            ["Week 4", "模拟冲刺 + 稳定发挥", "3–4 次全真；只修高频错点，不学新招"],
        ],
        col_widths=[28, 55, pdf.epw - 83],
    )
    pdf.p("每周结构：周一至周五分科精练 → 周六全真/半套 → 周日错题复盘 + 半天休息。")

    pdf.h2("四、每天怎么练（5 小时模板）")
    pdf.kv_table(
        [
            ["时段", "内容", "时长"],
            ["块1", "阅读自适应 Module / 错题精析", "70–80 分钟"],
            ["块2", "听力 Module + 精听 1 段", "70–80 分钟"],
            ["块3", "写作：造句 15 分钟 + 邮件或讨论 1 篇", "50–60 分钟"],
            ["块4", "口语：复述 + 面试 4 题录音", "40–50 分钟"],
            ["收尾", "错题本 + 明日弱项一句", "15–20 分钟"],
        ],
        col_widths=[22, pdf.epw - 52, 30],
    )
    pdf.p("只有 3 小时：保弱输出科 + 读听各半 Module。有 6+ 小时：只加一项弱科加压，不要全加。")
    pdf.p("弱科倾斜：最低两科每天各 +20–30 分钟。")

    pdf.h2("五、四科怎么攻")

    pdf.h3("1. 阅读（目标单项 5.5–6）")
    pdf.bullet("第一优先：Module 1 正确率。宁可慢，不要因赶时间乱选。")
    pdf.bullet("每天 1 个 Module 或等量题；错题按类型归类：词汇 / 指代 / 细节 / 推理 / 主旨。")
    pdf.bullet("先题干定位再精读；不确定题做标记，模块内 Review；进 Module 2 前绝不留空。")

    pdf.h3("2. 听力（目标单项 5.5–6）")
    pdf.bullet("同样保 Module 1；笔记只记结构信号：观点、对比、因果、例子。不要整句抄。")
    pdf.bullet("精听 + 做题交替。错题回听：是「没听到」还是「听到但推理错」。")
    pdf.bullet("校园对话/通知等生活化新题不能掉以轻心——基础题失分容易被送进 Lower。")

    pdf.h3("3. 写作（97→5.5 的关键变量）")
    pdf.bullet("造句：每天 10–20 题。练语序、主谓一致、从句、冠词、介词。这是送分题。")
    pdf.bullet("邮件：准备 3 套骨架——请求 / 道歉说明 / 建议安排。目的清晰、语气得体、信息完整。")
    pdf.bullet("学术讨论：立场一句 → 理由+例子 → 回应同学一句。清晰完整优先于华丽。")
    pdf.p("邮件骨架（默写）：")
    pdf.bullet("请求：称呼+目的 → 背景 → 具体请求 → 感谢落款", indent=12)
    pdf.bullet("道歉说明：道歉/变更 → 原因（短）→ 补救方案 → 确认+感谢", indent=12)
    pdf.bullet("建议安排：回应目的 → 建议+理由 → 备选 → 请确认", indent=12)

    pdf.h3("4. 口语（新题型适应最快见效）")
    pdf.bullet("听音复述：每天 15–20 分钟。完整复述、重音节奏；犯错也不要回头改。")
    pdf.bullet("模拟面试：每题约 45 秒。结构锁死——观点 → 理由 → 具体例子。")
    pdf.bullet("主题库覆盖：学习校园、科技生活、观点对比、人物经历。录音回听盯卡顿和空内容。")
    pdf.bullet("听口联动：听力材料当天抽 2–3 句做复述。")

    pdf.h2("六、四周逐日做什么")

    pdf.h3("开练前 48 小时（Day 0）")
    for t in [
        "查出旧托福四科分项，标出最低两科",
        "预约考试日，倒推 28 天，标出全真日",
        "下载 ETS 新制样题，按新顺序跑通界面",
        "建三个文件夹：错题 / 口语录音 / 写作终稿",
        "做一次新制全真摸底，只定 3 条可执行改进",
        "主目标写死：总分 5.5；冲刺上限：6",
    ]:
        pdf.check(t)

    pdf.h3("Week 1（D1–D7）：新题型上手")
    pdf.day_block("目标", [
        "每天必做：造句 + 听音复述（不可隔天）",
        "三套邮件骨架各写至少 1 次",
        "Interview 录音累计 ≥20 条",
        "D6 半套或全真；D7 复盘 + 半天休息",
    ])
    pdf.p("逐日焦点：D1 自适应节奏 → D2 邮件B+面试结构 → D3 学术讨论限时 → D4 Review 习惯 → D5 模板收束 → D6 模考 → D7 复盘。")
    pdf.p("造句正确率目标：Week1 末 ≥85%。")

    pdf.h3("Week 2（D8–D14）：正确率 + 输出升档")
    pdf.day_block("目标", [
        "读/听多数练习自评「能进 Upper」",
        "造句周正确率 ≥90%",
        "邮件与讨论用 5.5 检查表连续过关 3 次",
        "D13 全真：四科估分均 ≥5.0，至少一科 5.5",
    ])
    pdf.p("逐日焦点：D8 阅读 Module1 专项 → D9 听力 Module1 专项 → D10 输出升档 → D11 弱科双倍 → D12 说写限时连考 → D13 全真 → D14 复盘出口。")

    pdf.h3("说写 5.5 档过关标准（连续 3 次全过才算稳）")
    pdf.p("邮件：目的句在前 2 句内；对方要做什么清楚；关键细节齐全；语气匹配；限时完成。")
    pdf.p("讨论：首句有立场；有具体例子；回应同学至少一句；限时完成。")
    pdf.p("面试：45 秒内观点→理由→例子完整；例子具体；无明显长时间卡顿。")

    pdf.h3("Week 3（D15–D21）：隔日全真")
    pdf.p("节奏：全真 → 弱科加压 → 全真 → 次弱科加压 → 全真 → 听口联动 → 全真/半套。")
    pdf.day_block("目标", [
        "至少 3 次高质量全真（建议 D15 / D17 / D19）",
        "每次全真后只改 1 个习惯，不列十条改进",
        "加压日真正打在最低科上",
        "按准考试日作息彩排（睡眠、热身、顺序）",
    ])
    pdf.p("全真日流程：考前 30 分钟确认设备与目标 → 严格按读听写说考完 → 休息 30–60 分钟 → 估分、统计错题、只定 1 个习惯。")
    pdf.p("崩盘预案：Module1 连续不会就标记跳过末尾回改；造句卡住选最通顺不空题；邮件空白先写目的句+三条要点；复述漏了不重来；面试超时就缩短例子保证收尾。")

    pdf.h3("Week 4（D22–D28）：只稳发挥")
    pdf.day_block("铁律", [
        "不学新大招、不换新模板体系",
        "只修错题本 Top 3 高频错点",
        "全真质量大于数量；累了减量",
        "睡眠优先于额外套题",
    ])
    pdf.p("安排：D22 全真 → D23 修错点 → D24 全真 → D25 轻量+早睡 → D26 全真 → D27 休息或半套 → D28 考试/热身。")
    pdf.p("考试日精简流程：起床 → 早餐 → 5 题造句 + 3 句复述开嗓 → 出发/登录 → 默念 3 条纪律 → 开考。")

    pdf.h2("七、模考与达标线")
    pdf.bullet("Week1 第 1–2 天：新制全真摸底")
    pdf.bullet("之后每周至少 1 次全真；Week3 隔日；Week4 增至 3–4 次")
    pdf.bullet("冲 5.5：四科估分尽量都 ≥5.0，且至少两科稳定 5.5；客观题进入「Module2 Upper 且错题少」状态")
    pdf.bullet("冲 6：四科都持续贴近 5.5–6，几乎无低级失误")
    pdf.p("模考后只做三件事：① 统计题型错误率 ② 改 1 个可执行习惯 ③ 第二天针对该习惯练。")

    pdf.h2("八、资料怎么选")
    pdf.bullet("主材料：ETS 新版样题 / 官方指南配套练习（优先级最高）")
    pdf.bullet("辅材料：含自适应与新说写题型的高质量新制模考")
    pdf.bullet("旧 TPO 学术阅读/讲座可补充输入量，但不能替代新题型训练")
    pdf.bullet("必做工具：错题本（按题型）、口语录音、写作终稿（你自己的过关版，不是抄范文）")

    pdf.h2("九、最容易失败的五件事")
    pdf.kv_table(
        [
            ["风险", "怎么破"],
            ["只练旧题型", "Week1 起每天必有造句 + 听音复述"],
            ["Module1 求快留空", "正确率优先；提交前 Review"],
            ["说写不录音/不限时", "每次输出必须计时 + 回放"],
            ["Week4 还学新模板", "停止扩容，只修 Top3 错点"],
            ["偏科硬冲单科满分", "先把最低科拉到 5.0/5.5"],
        ],
        col_widths=[55, pdf.epw - 55],
    )

    pdf.h2("十、28 天全真日怎么排")
    pdf.p("把考试日定死后，至少标出这些全真：")
    pdf.bullet("摸底 1 次（诊断期）")
    pdf.bullet("Week1：1 次（D6）")
    pdf.bullet("Week2：1 次（D13）")
    pdf.bullet("Week3：3 次（D15 / D17 / D19，D21 可半套）")
    pdf.bullet("Week4：3 次（D22 / D24 / D26）")

    pdf.ln(4)
    pdf.set_font("cn", "B", 11)
    pdf.multi_cell(0, 7, "一句话执行口令")
    pdf.ln(1)
    pdf.set_font("cn", "", 10)
    pdf.multi_cell(
        0,
        6,
        "每天：读听保 Module1 不送分 → 造句+邮件/讨论限时写 → 复述+面试录音。"
        "每周：至少一套全真。全程：抬最低科，稳总分 5.5。",
    )

    pdf.ln(6)
    pdf.set_font("cn", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "配套详细表格与逐日清单见仓库文件夹 toefl-sprint-97-to-5.5/（诊断表、错题本、分数追踪、各周 daily-plan）。",
    )

    pdf.output(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
