# ENGG433/956 Week 4 Tutorial Solutions

**Questions:** E17.2 · E17.12 · E18.4 · E18.9 (Weygandt)

配套 Excel：

- `Cashflow_statement_template.xlsx` — E17.2 分类 + E17.12 直接法付现
- `excel_template_18.4.xlsx` — E18.4 垂直分析（含公式与图表）
- `E18.9_Lendell_ratios.xlsx` — E18.9 六个指标（含公式）

---

## 做题总逻辑（先掌握再做题）

本周两块内容：

1. **现金流量表 Statement of Cash Flows（第 17 章）**
2. **财务报表分析 Financial Statement Analysis（第 18 章）** — 垂直分析 + 比率

### 现金流量表的四个去处

每一笔业务只问两件事：**有没有现金进出？现金从哪类活动来/去？**

| 分类 | 记什么 | 典型例子 |
|------|--------|----------|
| **Operating**（间接法） | 从 Net Income 出发，把“进了利润但不走现金 / 走了现金但不进利润”的项目调回去 | 折旧加回、摊销加回、处置损失加回、处置利得减去；营运资本变动 |
| **Investing** | 长期资产、对外投资的现金 | 买/卖土地、厂房、设备、专利；放贷/收回贷款 |
| **Financing** | 与股东、长期债权人的现金 | 发行股票、发债、还债、付现金股利 |
| **Significant noncash investing and financing** | 重大、但不碰现金的投融资 | 土地换专利、发债券换土地、债券转普通股。**不进三张现金分部，另附 schedule / notes** |

间接法记忆口诀（Operating）：

\[
\text{Cash from operations} = \text{NI} + \text{非现金费用} + \text{损失} - \text{利得} \pm \text{营运资本}
\]

营运资本方向：

| 项目变动 | 对 Operating cash 的影响 |
|----------|--------------------------|
| 流动资产 ↑（存货、应收、预付） | 现金被占用 → **减** |
| 流动资产 ↓ | 现金被释放 → **加** |
| 流动负债 ↑（应付、应计） | 还没付 → **加** |
| 流动负债 ↓ | 多付了 → **减** |

直接法不从 NI 出发，而是把利润表的应计项目“还原成付了多少现金”。E17.12 就是这个。

### 垂直分析与比率

- **Vertical analysis（common-size）**：利润表每一行 ÷ **Net sales**（Net sales = 100%）。便于跨期、跨公司比结构，不受规模干扰。
- **比率**：先分清分子分母用的是**时点**还是**期间**。周转率用**平均值**（年初+年末）/2；流动比率用**年末**时点。

---

## E17.2 — Classify transactions by type of activity（Hailey Corp.）

### 题目要求

指出下列各项在**间接法现金流量表**中应列示的位置，四选一：

1. Operating activity（作为 NI 的调整项）
2. Investing activity
3. Financing activity
4. Significant noncash investing and financing activity

题目说明：除非另有说明，均涉及现金。

### 逐项解答

| 项 | 交易 | 分类 | 理由 |
|----|------|------|------|
| **a** | Exchange of land for patent | **Significant noncash investing and financing** | 土地换专利，两边都是长期资产，**没有现金**。附注披露。 |
| **b** | Sale of building at book value | **Investing** | 处置长期资产收到现金。按账面价值出售 → 无损益，Operating 无需调整。 |
| **c** | Payment of dividends | **Financing** | 向股东分配现金。 |
| **d** | Depreciation of plant assets | **Operating** | 折旧减少了 NI，但没有付出现金。间接法 **加回**。 |
| **e** | Conversion of bonds into common stock | **Significant noncash investing and financing** | 负债转权益，**没有现金**。 |
| **f** | Issuance of capital stock | **Financing** | 向股东发行股票收到现金。 |
| **g** | Amortization of patent | **Operating** | 与折旧相同：非现金费用，**加回** NI。 |
| **h** | Issuance of bonds for land | **Significant noncash investing and financing** | 一边取得土地（investing）、一边发行债券（financing），但现金未动。 |
| **i** | Purchase of land | **Investing** | 用现金购买长期资产。 |
| **j** | Loss on disposal of plant assets | **Operating** | 损失已减少 NI，但不是经营活动现金流出。间接法 **加回损失**。处置收到的现金本身记 Investing。 |
| **k** | Retirement of bonds | **Financing** | 用现金偿还长期债务本金。 |

### 答案汇总

a noncash · b investing · c financing · d operating · e noncash · f financing · g operating · h noncash · i investing · j operating · k financing

### 易错点

- **j 不是 Investing。** “Loss on disposal” 说的是损益数字，不是售价现金。售价现金才是 Investing；损失加回才是 Operating。
- **a / e / h 不要硬塞进 Investing 或 Financing 正表。** 没有现金进出，只能进 noncash schedule。
- **b 按账面出售**：没有 gain/loss，所以 Operating 不用调，只在 Investing 记现金流入。

---

## E17.12 — Compute cash payments（direct method）· McDonald's 2027

金额单位：**$ millions**。

### 已知

| 项目 | 金额 |
|------|------|
| Cost of goods sold | 5,178.0 |
| Operating expenses（含折旧） | 10,725.7 |
| 其中 Depreciation expense | 1,216.2 |
| Inventory **decreased** | 5.3 |
| Prepaid expenses **increased** | 42.2 |
| Accounts payable（存货供应商）**increased** | 15.6 |
| Accrued expenses payable **increased** | 199.8 |

### (a) Cash payments to suppliers

先还原“本年购货”，再还原“本年付给供应商的现金”。

\[
\begin{aligned}
\text{Purchases} &= \text{COGS} - \text{Decrease in inventory} \\
&= 5{,}178.0 - 5.3 = 5{,}172.7
\end{aligned}
\]

存货下降：卖掉的货里有一部分来自期初库存，所以本年购货 < COGS。

\[
\begin{aligned}
\text{Cash paid to suppliers} &= \text{Purchases} - \text{Increase in AP} \\
&= 5{,}172.7 - 15.6 = \mathbf{5{,}157.1}
\end{aligned}
\]

应付账款上升：有一部分购货还没付，所以付现 < 购货。

一条公式：

\[
\text{Cash paid to suppliers} = \text{COGS} - \Delta\text{Inventory↓} - \Delta\text{AP↑} = 5{,}178.0 - 5.3 - 15.6 = \mathbf{5{,}157.1}
\]

**答案 (a)：$5,157.1 million**

### (b) Cash payments for operating expenses

折旧从未付现，必须先从 Operating expenses 里拿掉；再按预付、应计调整。

\[
\begin{aligned}
\text{Opex excluding depreciation} &= 10{,}725.7 - 1{,}216.2 = 9{,}509.5 \\
\text{Add: prepaid expenses ↑} &= +42.2 \quad \text{（多付了预付款）} \\
\text{Less: accrued expenses ↑} &= -199.8 \quad \text{（费用入账但还没付）} \\
\text{Cash paid for operating expenses} &= 9{,}509.5 + 42.2 - 199.8 = \mathbf{9{,}351.9}
\end{aligned}
\]

一条公式：

\[
\text{Cash paid for opex} = \text{Operating expenses} - \text{Depreciation} + \Delta\text{Prepaids↑} - \Delta\text{Accrued↑}
\]

**答案 (b)：$9,351.9 million**

### 方向口诀（直接法付现）

| 调整 | 存货/预付（资产） | 应付/应计（负债） |
|------|-------------------|-------------------|
| 增加 | 付现 **多于** 费用 → 加上 | 付现 **少于** 费用 → 减去 |
| 减少 | 付现 **少于** 费用 → 减去 | 付现 **多于** 费用 → 加上 |

---

## E18.4 — Prepare vertical analysis · Joshua Corporation

垂直分析：每一行金额 ÷ **当年 Net sales**，保留 **1 位小数**。

先补全多步利润表中间行（题目只给了费用和 NI，模板通常要求写出 Gross profit 等）：

| | 2027 Amount | 2026 Amount |
|--|-------------|-------------|
| Net sales | 800,000 | 600,000 |
| Cost of goods sold | 520,000 | 408,000 |
| **Gross profit** | 280,000 | 192,000 |
| Selling expenses | 120,000 | 72,000 |
| Administrative expenses | 60,000 | 48,000 |
| **Total operating expenses** | 180,000 | 120,000 |
| **Income before income taxes** | 100,000 | 72,000 |
| Income tax expense | 30,000 | 24,000 |
| **Net income** | 70,000 | 48,000 |

验算：\(800{,}000-520{,}000-120{,}000-60{,}000-30{,}000=70{,}000\)；\(600{,}000-408{,}000-72{,}000-48{,}000-24{,}000=48{,}000\)。

### JOSHUA CORPORATION — Condensed Income Statement

百分比 = Amount / Net sales。注意 \(30{,}000/800{,}000=3.75\%\rightarrow\mathbf{3.8\%}\)，\(70{,}000/800{,}000=8.75\%\rightarrow\mathbf{8.8\%}\)。

| | 2027 Amount | 2027 % | 2026 Amount | 2026 % |
|--|-------------|--------|-------------|--------|
| Net sales | $800,000 | **100.0%** | $600,000 | **100.0%** |
| Cost of goods sold | 520,000 | 65.0 | 408,000 | 68.0 |
| Gross profit | 280,000 | 35.0 | 192,000 | 32.0 |
| Selling expenses | 120,000 | 15.0 | 72,000 | 12.0 |
| Administrative expenses | 60,000 | 7.5 | 48,000 | 8.0 |
| Total operating expenses | 180,000 | 22.5 | 120,000 | 20.0 |
| Income before income taxes | 100,000 | 12.5 | 72,000 | 12.0 |
| Income tax expense | 30,000 | **3.8** | 24,000 | 4.0 |
| Net income | $70,000 | **8.8%** | $48,000 | **8.0%** |

### 怎么读这张表

- 毛利率 32.0% → 35.0%（COGS 占比下降 3 个百分点）——产品成本控制变好，或售价/组合改善。
- 销售费用 12.0% → 15.0% —— 吃掉了大部分毛利改善。
- 管理费用 8.0% → 7.5% —— 销售额增 33%，管理费有固定成本杠杆。
- 净利率 8.0% → 8.8% —— 整体更赚钱，但要盯住销售费用。

Excel 中百分比列全部用公式 `=金额/$Net_sales`，单元格格式 `0.0%`，不要手填。

---

## E18.9 — Compute selected ratios · Lendell Company（31 Dec 2027）

### 先整理计算用的中间量

**流动资产（年末）** = Cash + AR + Inventory = \(15{,}000+70{,}000+60{,}000=145{,}000\)

**流动负债（年末）** = Accounts payable = \(50{,}000\)  
（Bonds payable due **2040** → 非流动，不算进 current ratio 分母。）

**Net credit sales** = Sales on account − returns = \(375{,}000-25{,}000=350{,}000\)

**Average AR** = \((70{,}000+60{,}000)/2=65{,}000\)

**Average inventory** = \((60{,}000+50{,}000)/2=55{,}000\)

教材惯例：周转率先四舍五入到 1 位小数，再用该数去除 365。

### (a) Current ratio

\[
\frac{\text{Current assets}}{\text{Current liabilities}} = \frac{145{,}000}{50{,}000} = \mathbf{2.9 : 1}
\]

每 1 美元流动负债对应 2.9 美元流动资产，短期偿债能力充足。

### (b) Accounts receivable turnover

\[
\frac{\text{Net credit sales}}{\text{Average AR}} = \frac{350{,}000}{65{,}000} = 5.3846\ldots = \mathbf{5.4\ \text{times}}
\]

### (c) Average collection period

\[
\frac{365}{5.4} = \mathbf{67.6\ \text{days}}
\]

（若不用四舍五入的 5.4，而用 \(365 \times 65{,}000 / 350{,}000 = 67.8\) 天。作业按 Wiley：用已入的 5.4。）

### (d) Inventory turnover

\[
\frac{\text{COGS}}{\text{Average inventory}} = \frac{198{,}000}{55{,}000} = \mathbf{3.6\ \text{times}}
\]

### (e) Days in inventory

\[
\frac{365}{3.6} = \mathbf{101.4\ \text{days}}
\]

### (f) Free cash flow

\[
\begin{aligned}
\text{FCF} &= \text{Net cash from operating activities} - \text{Capital expenditures} - \text{Cash dividends} \\
&= 48{,}000 - 25{,}000 - 10{,}000 = \mathbf{\$13{,}000}
\end{aligned}
\]

经营现金 48,000 覆盖了维持产能的资本支出和股利后，还剩 13,000。

### 答案汇总

| | 指标 | 答案 |
|--|------|------|
| a | Current ratio | **2.9 : 1** |
| b | Accounts receivable turnover | **5.4 times** |
| c | Average collection period | **67.6 days** |
| d | Inventory turnover | **3.6 times** |
| e | Days in inventory | **101.4 days** |
| f | Free cash flow | **$13,000** |

### 易错点

- 分母不要把 **bonds payable** 算进流动负债。
- 周转率必须用 **average**，不能只用年末。
- AR 周转的分子是 **净赊销**（扣退货），不是毛销售 375,000。
- 收账天数 / 存货天数用 **已四舍五入的周转率**，否则会和标准答案差 0.2 天。

---

## 交作业时建议带上的三句话

1. **E17.2：** 先问“有没有现金”；没有 → noncash schedule；有 → 再问是日常经营调整、买长期资产，还是股东/债权人。
2. **E17.12：** 直接法付现 = 应计费用 ± 存货/预付 ± 应付/应计；折旧永远先剔除。
3. **E18.4 / E18.9：** 垂直分析全部除以销售额；比率先分清时点 vs 期间、要不要平均、债是不是流动。
