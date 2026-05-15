好的，这是基于您提供的课程章节内容生成的知识地图（MOC），采用 Markdown 格式，适合在 Obsidian 等笔记软件中使用。

---

# MIT_14.01_Principles_of_Microeconomics_MOC

这是 MIT 14.01 微观经济学原理的知识地图（Map of Content）。它旨在将课程的核心概念组织成一个结构化的网络，便于理解和复习。

## 核心支柱

-   [[#1. 微观经济学核心框架 (The Core Framework)]]
-   [[#2. 消费者理论与需求 (The Demand Side)]]
-   [[#3. 厂商理论与供给 (The Supply Side)]]
-   [[#4. 市场均衡、效率与福利 (Equilibrium, Efficiency & Welfare)]]
-   [[#5. 不完全竞争与市场失灵 (Imperfect Competition & Market Failure)]]
-   [[#6. 要素市场 (Factor Markets)]]
-   [[#7. 理论扩展 (Extensions of Microeconomic Theory)]]

---

## 1. 微观经济学核心框架 (The Core Framework)

-   **核心问题**: **约束下的最优化 (Constrained Optimization)**
    -   **目标函数 (Objective Function)**: 行为人希望最大化的量 (如: 效用, 利润)。
    -   **约束条件 (Constraints)**: 行为人面临的限制 (如: 收入, 成本, 时间)。
    -   **基本概念**:
        -   **稀缺性 (Scarcity)**: 经济学研究的根本前提。
        -   **权衡取舍 (Trade-offs)**: 每一个决策都包含选择。
        -   **机会成本 (Opportunity Cost)**: 为选择某选项而放弃的次优选项的价值。
-   **分析工具**:
    -   **实证分析 (Positive Analysis)**: 描述“世界是什么样” (Is)。
    -   **规范分析 (Normative Analysis)**: 探讨“世界应该是什么样” (Ought)。
        -   *注: 严谨的规范分析必须以坚实的实证分析为基础。*

## 2. 消费者理论与需求 (The Demand Side)

-   **章节笔记**: [[Ch_01_消费者理论与市场需求基础]]
-   **目标**: 推导市场需求曲线。
-   **消费者偏好 (Preferences)**
    -   **理性偏好三公理 (Axioms of Rational Preference)**:
        1.  **完备性 (Completeness)**: 总能对消费束进行比较 ($A \succ B$, $B \succ A$, or $A \sim B$)。
        2.  **传递性 (Transitivity)**: 若 $A \succ B$ 且 $B \succ C$, 则 $A \succ C$。
        3.  **非饱和性 (Non-satiation)**: "More is Better"。
    -   **无差异曲线 (Indifference Curves)**: 效用水平相同的消费束集合。
        -   **性质**:
            1.  更高曲线代表更高用。
            2.  向下倾斜。
            3.  不能相交。
            4.  通常凸向原点。
        -   **核心概念**: **边际替代率 (Marginal Rate of Substitution, MRS)**
            -   **定义**: 保持效用不变，消费者愿意用一种商品交换另一商品的比例。
            -   **公式**: $MRS_{XY} = - \frac{\Delta Y}{\Delta X} \bigg|_{\bar{U}} = \frac{MU_X}{MU_Y}$
-   **消费者选择 (Consumer Choice)**
    -   **约束**: **预算约束线 (Budget Constraint)**: $P_X X + P_Y Y \le I$
    -   **最优化问题**: 在预算约束下，达到最高的无差异曲线。
    -   **最优解**:
        -   **条件**: $MRS = \frac{P_X}{P_Y}$ 或 $\frac{MU_X}{P_X} = \frac{MU_Y}{P_Y}$
        -   **含义**: 每单位货币花费在任何商品上带来的边际效用相等。
-   **需求 (Demand)**
    -   **个人需求曲线**: 由消费者最优化问题导出，显示价格与需求量关系。
    -   **市场需求曲线**: 所有个人需求曲线的水平加总。

## 3. 厂商理论与供给 (The Supply Side)

-   **章节笔记**: [[Ch_02_厂商理论_生产_成本与完全竞争]]
-   **目标**: 推导市场供给曲线。
-   **生产理论 (Production)**
    -   **目标**: **利润最大化 (Profit Maximization)**: $\pi = TR - TC$
    -   **生产函数**: $q = f(L, K)$
    -   **时间维度**:
        -   **短期 (Short Run)**: 至少一种要素固定 (通常是 $K$)。
        -   **长期 (Long Run)**: 所有要素均可变。
    -   **短期生产**:
        -   **边际产量 (Marginal Product, MP)**: $MP_L = \frac{\partial q}{\partial L}$
        -   **边际报酬递减规律 (Law of Diminishing Marginal Returns)**
    -   **长期生产**:
        -   **等产量线 (Isoquant)**: 产出水平相同的投入组合。
        -   **边际技术替代率 (MRTS)**: $MRTS_{LK} = - \frac{\Delta K}{\Delta L} \bigg|_{\bar{q}} = \frac{MP_L}{MP_K}$
-   **成本理论 (Costs)**
    -   **成本最小化 (Cost Minimization)**:
        -   **条件**: $\frac{MP_L}{w} = \frac{MP_K}{r}$ (每美元投入的边际产出相等)
        -   **(跨章节联系 -> [[#6. 要素市场 (Factor Markets)]])**: 该条件是要素市场需求的基础。
    -   **核心成本概念**:
        -   **边际成本 (Marginal Cost, MC)**: $MC = \frac{dTC}{dq}$
        -   **平均总成本 (ATC)**, **平均可变成本 (AVC)**
-   **完全竞争市场 (Perfect Competition)**
    -   **特征**: 价格接受者 (Price Taker)。
    -   **利润最大化条件**: $P = MR = MC$
    -   **企业供给曲线**: 短期为 $AVC$ 以上的 $MC$ 曲线；长期为 $ATC$ 以上的 $MC$ 曲线。
    -   **市场供给曲线**: 所有企业供给曲线的水平加总。

## 4. 市场均衡、效率与福利 (Equilibrium, Efficiency & Welfare)

-   **章节笔记**: [[Ch_03_市场均衡_效率与福利经济学]]
-   **市场均衡**: 供给曲线与需求曲线相交点，决定均衡价格 $P^*$ 和均衡数量 $Q^*$。
-   **福利经济学 (Welfare Economics)**
    -   **核心度量**:
        -   **消费者剩余 (Consumer Surplus, CS)**: 支付意愿与实际支付之差。$CS = \int_0^{Q^*} P_D(Q) dQ - P^*Q^*$
        -   **生产者剩余 (Producer Surplus, PS)**: 实际收入与可变成本之差。$PS = P^*Q^* - \int_0^{Q^*} P_S(Q) dQ$
        -   **社会总福利 (Total Welfare, W)**: $W = CS + PS$
    -   **福利经济学第一基本定理**:
        -   **内容**: 完全竞争市场均衡是**帕累托有效 (Pareto Efficient)** 的，并能最大化社会总福利。
        -   **效率条件**: 在均衡点，$P_D(Q^*) = P_S(Q^*)$，意味着**边际支付意愿 (MWTP) = 边际成本 (MC)**。

## 5. 不完全竞争与市场失灵 (Imperfect Competition & Market Failure)

-   **章节笔记**: [[Ch_04_不完全竞争市场]], [[Ch_07_市场失灵与政府干预]]
-   **核心问题**: 市场无法实现帕累托最优。
-   **不完全竞争**:
    -   **垄断 (Monopoly)**: 单一生产者，具有**市场势力 (Market Power)**。
        -   **利润最大化**: $MR = MC$
        -   **关键区别**: $MR < P$ (因为存在“毒化效应”)。
        -   **公式**: $MR = P(1 + \frac{1}{\varepsilon_D})$
        -   **勒纳指数 (Lerner Index)**: 衡量市场势力 $\frac{P-MC}{P} = -\frac{1}{\varepsilon_D}$
        -   **结果**: 产生**无谓损失 (Deadweight Loss, DWL)**。
-   **市场失灵 (Market Failures)**
    -   **税收 (Taxation)**
        -   **税收归宿 (Tax Incidence)**: 经济负担的分配，由**弹性**决定，与法定归宿无关。**缺乏弹性的一方承担更多税负**。
        -   **结果**: 产生无谓损失，扭曲市场。
    -   **外部性 (Externalities)**: 市场交易影响第三方。
        -   **问题**: 市场价格不反映全部社会成本/收益 ($SMC \neq MC$ 或 $SMB \neq MB$)。
        -   **解决方案**:
            -   **庇古税/补贴 (Pigouvian Tax/Subsidy)**: 使外部成本/收益内部化。
            -   **科斯定理 (Coase Theorem)**: 在无交易成本下，产权界定清晰即可通过协商解决。
    -   **信息不对称 (Asymmetric Information)**
        -   **逆向选择 (Adverse Selection)**: 交易前的信息不对称 (e.g., 二手车市场)。
        -   **道德风险 (Moral Hazard)**: 交易后的行为不可观测 (e.g., 医疗保险)。

## 6. 要素市场 (Factor Markets)

-   **章节笔记**: [[Ch_05_要素市场_劳动与资本]]
-   **目标**: 内生化要素价格 (工资 $w$, 资本租金率 $r$)。
-   **要素需求 (Factor Demand)**
    -   **性质**: **派生需求 (Derived Demand)**。
    -   **优化条件**: 企业雇佣/租用要素直到其边际贡献等于其边际成本。
        -   **劳动**: $MRP_L = w$
        -   **资本**: $MRP_K = r$
    -   **核心概念**: **边际收益产量 (Marginal Revenue Product, MRP)**
        -   **公式**: $MRP_L = MR \times MP_L$
        -   在完全竞争产出品市场中: $MRP_L = P \times MP_L$
    -   **(跨章节联系 -> [[#3. 厂商理论与供给 (The Supply Side)]])**: 利润最大化条件 ($MRP_L=w, MRP_K=r$) 隐含了成本最小化条件 ($\frac{MP_L}{w} = \frac{MP_K}{r}$)。
-   **要素供给 (Factor Supply)**
    -   **劳动供给**: 来自于个人的**劳动-闲暇权衡 (Labor-Leisure Trade-off)**。
    -   **资本供给**: 来自于家庭的**跨期消费选择 (储蓄决策)**。
        -   **(跨章节联系 -> [[#7. 理论扩展 (Extensions of Microeconomic Theory)]])**: 与跨期选择模型直接相关。

## 7. 理论扩展 (Extensions of Microeconomic Theory)

-   **章节笔记**: [[Ch_06_微观经济理论的扩展]]
-   **跨期选择与资本市场 (Intertemporal Choice)**
    -   **核心工具**:
        -   **现值 (Present Value, PV)**: $PV = \frac{FV}{(1+i)^t}$
        -   **永续年金 (Perpetuity)**: $PV = \frac{F}{i}$
    -   **投资决策**:
        -   **净现值法则 (Net Present Value, NPV)**: $NPV = -I_0 + \sum \frac{C_t}{(1+i)^t}$
        -   **法则**: 如果 $NPV > 0$，则投资。
    -   **资本市场均衡**:
        -   **资本供给 (储蓄)**: 利率 $i$ 的增函数 (通常)。
        -   **资本需求 (投资)**: 利率 $i$ 的减函数。
        -   均衡利率 $i^*$ 由 $S(i) = D(i)$ 决定。
-   **其他扩展主题**:
    -   **国际贸易 (International Trade)**
    -   **不确定性下的选择 (Choice Under Uncertainty)**
    -   **公平与效率的权衡 (Equity vs. Efficiency)**