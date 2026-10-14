# 公开汇总结果

- [主结果 CSV](main_results.csv)：A、B、严格 C1、C2、C3、过滤模式与 C4；空值表示未适用或未重新评分。
- [内部负控代理指标 CSV](negative_control_proxy.csv)：仅保存聚合的非 TED 阳性体征出现数与比例，不含病例标识。
- [结果解释](../docs/results-and-analysis.md)。

字段中的 `keyword_count_proxy` 不是临床准确率；`disagreement` 是 TED 子集体征决策分歧；`any_positive_proxy` 不是核实过的逐体征 FP。定义和分母见 [指标说明](../docs/metric-definitions.md)。

主表与负控表来自不同聚合来源，未确认每个同名行严格同运行。不要按模型名直接拼接为同一试验的配对结果。
