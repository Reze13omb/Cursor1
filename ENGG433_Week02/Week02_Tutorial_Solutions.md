# ENGG433/956 Week 2 Tutorial Solutions

**Questions:** E1.7 · P1.3 · E2.3 · P2.1 (Weygandt)

---

## 做题总逻辑（先掌握再做题）

会计恒等式始终成立：

\[
\text{Assets} = \text{Liabilities} + \text{Owner's Equity}
\]

Owner's Equity 会因以下项目变动：

| 项目 | 对 Owner's Equity 的影响 |
|------|--------------------------|
| Owner investment（业主投资） | ↑ |
| Revenue（收入） | ↑ |
| Expense（费用） | ↓ |
| Drawings（业主提款） | ↓ |

**借方 / 贷方规则（Debit / Credit）：**

| 账户类型 | 增加记 | 减少记 | 正常余额 |
|----------|--------|--------|----------|
| Asset（资产） | Debit | Credit | Debit |
| Liability（负债） | Credit | Debit | Credit |
| Owner's Capital | Credit | Debit | Credit |
| Owner's Drawings | Debit | Credit | Debit |
| Revenue | Credit | Debit | Credit |
| Expense | Debit | Credit | Debit |

**日记账（Journal）写法：** 先写 Debit 账户（左对齐），再写 Credit 账户（缩进），Debit 合计 = Credit 合计。

---

## E1.7 — 分析交易对 Assets / Liabilities / Owner's Equity 的影响

### 题目要求

对每笔交易，选出对应字母：

- **(a)** Assets ↑ 且 Assets ↓（资产内部一增一减）
- **(b)** Assets ↑ 且 Owner's Equity ↑
- **(c)** Assets ↑ 且 Liabilities ↑
- **(d)** Assets ↓ 且 Owner's Equity ↓
- **(e)** Assets ↓ 且 Liabilities ↓
- **(f)** Owner's Equity ↓ 且 Liabilities ↑

### 解题步骤

对每一笔交易问三件事：

1. 哪些账户变了？
2. 每个账户是增还是减？
3. 它属于 Asset / Liability / OE 中的哪一类？

然后对照 (a)–(f)。

### 逐笔解答

| # | 交易 | 分析 | 答案 |
|---|------|------|------|
| 1 | 赊购电脑 $20,000 | Equipment ↑（资产）; Accounts Payable ↑（负债） | **(c)** |
| 2 | 付租金现金 $4,000 | Cash ↓（资产）; Rent Expense ↑ → OE ↓ | **(d)** |
| 3 | 收回上月已开票应收款 $17,000 | Cash ↑（资产）; Accounts Receivable ↓（资产） | **(a)** |
| 4 | 提供服务收到现金 $4,000 | Cash ↑（资产）; Service Revenue ↑ → OE ↑ | **(b)** |
| 5 | 付电费现金 $11,000 | Cash ↓（资产）; Utilities/Energy Expense ↑ → OE ↓ | **(d)** |
| 6 | 业主追加投资 $29,000 | Cash ↑（资产）; Owner's Capital ↑ → OE ↑ | **(b)** |
| 7 | 付清第1笔赊购款 | Cash ↓（资产）; Accounts Payable ↓（负债） | **(e)** |
| 8 | 广告费 $1,200 记在账上（未付） | Advertising Expense ↑ → OE ↓; Accounts Payable ↑（负债） | **(f)** |

### 易错点

- **第3笔不是收入**：服务已在 April 确认过收入；现在只是 Cash 与 AR 互换 → **(a)**，不是 (b)。
- **第8笔没有动资产**：费用发生但未付现金 → 只影响 OE 和负债 → **(f)**。

**答案汇总：** 1-(c), 2-(d), 3-(a), 4-(b), 5-(d), 6-(b), 7-(e), 8-(f)

---

## P1.3 — Divine Designs Co.（编制三张报表）

### 已知数据（June 30, 2027）

| 账户 | 金额 | 账户 | 金额 |
|------|------|------|------|
| Cash | $10,150 | Notes Payable | $9,000 |
| Accounts Receivable | 2,800 | Accounts Payable | 1,200 |
| Supplies | 2,000 | Service Revenue | 6,500 |
| Equipment | 10,000 | Advertising Expense | 500 |
| | | Rent Expense | 1,600 |
| | | Gasoline Expense | 200 |
| | | Utilities Expense | 150 |

- June 1 初始投资：$12,000
- 本月无追加投资
- Drawings：$1,300

### 做题逻辑

报表编制顺序固定：

1. **Income Statement** → 得到 Net Income
2. **Owner's Equity Statement** → 用 Net Income + Investment − Drawings 得到期末资本
3. **Balance Sheet** → Assets = Liabilities + Owner's Equity（用期末资本验算）

---

### (a) 按现有数据编制

#### Step 1 — Income Statement

**Divine Designs Co.**  
**Income Statement**  
**For the Month Ended June 30, 2027**

| | | |
|--|--|--|
| Revenues | | |
| &nbsp;&nbsp;Service revenue | | **$6,500** |
| Expenses | | |
| &nbsp;&nbsp;Rent expense | $1,600 | |
| &nbsp;&nbsp;Advertising expense | 500 | |
| &nbsp;&nbsp;Gasoline expense | 200 | |
| &nbsp;&nbsp;Utilities expense | 150 | |
| &nbsp;&nbsp;Total expenses | | **2,450** |
| **Net income** | | **$4,050** |

计算：\(6{,}500 - (1{,}600+500+200+150) = 6{,}500 - 2{,}450 = 4{,}050\)

#### Step 2 — Owner's Equity Statement

**Divine Designs Co.**  
**Owner's Equity Statement**  
**For the Month Ended June 30, 2027**

| | | |
|--|--|--|
| Owner's capital, June 1 | | $0 |
| Add: Investments | $12,000 | |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Net income | 4,050 | |
| | | 16,050 |
| | | 16,050 |
| Less: Drawings | | 1,300 |
| **Owner's capital, June 30** | | **$14,750** |

公式：  
\(\text{期末资本} = 0 + 12{,}000 + 4{,}050 - 1{,}300 = 14{,}750\)

#### Step 3 — Balance Sheet

**Divine Designs Co.**  
**Balance Sheet**  
**June 30, 2027**

**Assets**

| | |
|--|--|
| Cash | $10,150 |
| Accounts receivable | 2,800 |
| Supplies | 2,000 |
| Equipment | 10,000 |
| **Total assets** | **$24,950** |

**Liabilities and Owner's Equity**

| | |
|--|--|
| Liabilities | |
| &nbsp;&nbsp;Notes payable | $9,000 |
| &nbsp;&nbsp;Accounts payable | 1,200 |
| &nbsp;&nbsp;Total liabilities | 10,200 |
| Owner's equity | |
| &nbsp;&nbsp;Owner's capital | 14,750 |
| **Total liabilities and owner's equity** | **$24,950** |

验算：\(10{,}200 + 14{,}750 = 24{,}950\) ✓（左右平衡，说明 (a) 正确）

---

### (b) 加入两项遗漏后重编 IS 与 OE Statement

遗漏信息：

1. 已提供服务并开票但未收款 **$900** → 增加 Service Revenue（同时增加 AR，但本题 (b) 不要求 Balance Sheet）
2. 已发生汽油费但未支付 **$150** → 增加 Gasoline Expense（同时增加 AP）

#### Income Statement (b)

| | | |
|--|--|--|
| Revenues | | |
| &nbsp;&nbsp;Service revenue \(($6{,}500 + $900)\) | | **$7,400** |
| Expenses | | |
| &nbsp;&nbsp;Rent expense | $1,600 | |
| &nbsp;&nbsp;Advertising expense | 500 | |
| &nbsp;&nbsp;Gasoline expense \(($200 + $150)\) | 350 | |
| &nbsp;&nbsp;Utilities expense | 150 | |
| &nbsp;&nbsp;Total expenses | | **2,600** |
| **Net income** | | **$4,800** |

#### Owner's Equity Statement (b)

| | | |
|--|--|--|
| Owner's capital, June 1 | | $0 |
| Add: Investments | $12,000 | |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Net income | 4,800 | |
| | | 16,800 |
| | | 16,800 |
| Less: Drawings | | 1,300 |
| **Owner's capital, June 30** | | **$15,500** |

逻辑要点：应计制（accrual）下，**收入在赚取时确认，费用在发生时确认**，与是否收到/支付现金无关。所以 (b) 的净利更高。

---

## E2.3 — M. Acosta（日记账 Journalize）

### 已知交易

| 日期 | 交易 |
|------|------|
| Jan. 2 | 投资现金 $10,000 |
| 3 | 用现金 $3,000 购买二手车供业务使用 |
| 9 | 赊购用品 $600 |
| 11 | 向客户开票服务费 $2,400 |
| 16 | 付广告费现金 $350 |
| 20 | 收回 Jan.11 客户款 $900 |
| 23 | 向债权人付现 $300 |
| 28 | 业主提款 $1,000 |

### 做题逻辑（每笔都走这三步）

1. **识别账户**：涉及哪两个（或更多）账户？
2. **判断增减**：每个账户增还是减？
3. **套用 Debit/Credit 规则** 并保证借贷相等

### General Journal — J1

| Date | Account Titles and Explanation | Debit | Credit |
|------|--------------------------------|------:|-------:|
| Jan. 2 | Cash | 10,000 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Owner's Capital | | 10,000 |
| 3 | Equipment | 3,000 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 3,000 |
| 9 | Supplies | 600 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Accounts Payable | | 600 |
| 11 | Accounts Receivable | 2,400 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Service Revenue | | 2,400 |
| 16 | Advertising Expense | 350 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 350 |
| 20 | Cash | 900 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Accounts Receivable | | 900 |
| 23 | Accounts Payable | 300 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 300 |
| 28 | Owner's Drawings | 1,000 | |
| | &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 1,000 |

### 逐笔逻辑说明

| 日期 | 为什么这样记 |
|------|--------------|
| Jan. 2 | 现金资产↑ → Debit Cash；业主资本↑ → Credit Capital |
| 3 | 设备（车）是业务用资产↑ → Debit Equipment；现金↓ → Credit Cash |
| 9 | 用品资产↑ → Debit Supplies；未付款 → Credit Accounts Payable |
| 11 | 已赚取收入但未收款 → Debit AR；收入↑ → Credit Service Revenue |
| 16 | 费用↑ → Debit Advertising Expense；现金↓ → Credit Cash |
| 20 | 收回应收款：Cash↑、AR↓ → Debit Cash，Credit AR（**不是新收入**） |
| 23 | 偿还负债：AP↓ → Debit AP；Cash↓ → Credit Cash |
| 28 | 提款减少权益 → Debit Drawings；Cash↓ → Credit Cash（**不是费用**） |

---

## P2.1 — Holz Disc Golf Course（系列日记账）

### 可用账户

Cash, Prepaid Insurance, Land, Buildings, Equipment, Accounts Payable, Unearned Service Revenue, Owner's Capital, Owner's Drawings, Service Revenue, Advertising Expense, Salaries and Wages Expense

### 关键交易与分录

#### Mar. 1 — 投资 $20,000

| Account | Debit | Credit |
|---------|------:|-------:|
| Cash | 20,000 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Owner's Capital | | 20,000 |

逻辑：业主投入现金，资产与资本同时增加。

#### Mar. 3 — 一次性购买土地包（复合分录）

总价 $15,000 现金，拆分为：Land $12,000 + Shed(Buildings) $2,000 + Equipment $1,000

| Account | Debit | Credit |
|---------|------:|-------:|
| Land | 12,000 | |
| Buildings | 2,000 | |
| Equipment | 1,000 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 15,000 |

逻辑：一笔交易影响多个资产账户，必须做 **compound entry**；棚屋记入 Buildings。

#### Mar. 5 — 付广告费 $900

| Account | Debit | Credit |
|---------|------:|-------:|
| Advertising Expense | 900 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 900 |

#### Mar. 6 — 付一年保险 $600

| Account | Debit | Credit |
|---------|------:|-------:|
| Prepaid Insurance | 600 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 600 |

逻辑：保险预付尚未耗用 → 记 **资产** Prepaid Insurance，不是费用。

#### Mar. 10 — 赊购设备 $1,050

| Account | Debit | Credit |
|---------|------:|-------:|
| Equipment | 1,050 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Accounts Payable | | 1,050 |

#### Mar. 18 — 收到高尔夫费现金 $1,100

| Account | Debit | Credit |
|---------|------:|-------:|
| Cash | 1,100 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Service Revenue | | 1,100 |

#### Mar. 19 — 出售优惠券册 150 × $10 = $1,500

| Account | Debit | Credit |
|---------|------:|-------:|
| Cash | 1,500 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Unearned Service Revenue | | 1,500 |

逻辑：钱已收，但服务（打球）尚未提供 → 记 **负债** Unearned Service Revenue，**不是** Service Revenue。客户凭券以后打球时才确认收入。

#### Mar. 25 — 业主提款 $800

| Account | Debit | Credit |
|---------|------:|-------:|
| Owner's Drawings | 800 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 800 |

#### Mar. 30 — 付工资 $250

| Account | Debit | Credit |
|---------|------:|-------:|
| Salaries and Wages Expense | 250 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 250 |

#### Mar. 30 — 全额付清 Stevenson

| Account | Debit | Credit |
|---------|------:|-------:|
| Accounts Payable | 1,050 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Cash | | 1,050 |

逻辑：结清 Mar.10 的应付账款。

#### Mar. 31 — 收到高尔夫费 $2,700

| Account | Debit | Credit |
|---------|------:|-------:|
| Cash | 2,700 | |
| &nbsp;&nbsp;&nbsp;&nbsp;Service Revenue | | 2,700 |

### P2.1 易错对照

| 情形 | 正确处理 | 常见错误 |
|------|----------|----------|
| 一年保险 | Prepaid Insurance（资产） | 直接记 Insurance Expense |
| 优惠券预售 | Unearned Service Revenue（负债） | 直接记 Service Revenue |
| 业主提款 | Owner's Drawings | 记成 Salaries Expense |
| Mar.3 土地包 | Land + Buildings + Equipment | 全部记入 Land |

---

## 填 Excel 模板时的对应关系

| 模板文件 | 对应题 | 填什么 |
|----------|--------|--------|
| `excel templates1_3.xlsx` | P1.3 | (a) IS → OE Statement → BS；(b) IS → OE Statement |
| `Excel template 2_3.xlsx` | E2.3 | Jan.2–28 共 8 组分录 |
| `Excel template P2_1.xlsx` | P2.1 | Mar.1–31 各组分录（含两笔 Mar.30） |

---

## 快速答案卡

**E1.7:** 1-c, 2-d, 3-a, 4-b, 5-d, 6-b, 7-e, 8-f

**P1.3 (a):** NI = $4,050；期末资本 = $14,750；总资产 = $24,950  
**P1.3 (b):** NI = $4,800；期末资本 = $15,500

**E2.3 / P2.1:** 见上方完整日记账
