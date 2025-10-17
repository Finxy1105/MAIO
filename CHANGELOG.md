## v0.1 (Baseline)

- 建立可复现训练流程：StandardScaler + LinearRegression，固定随机种子
- 训练/测试拆分，保存模型与指标（RMSE）到 `models/`
- 提供 FastAPI `/health` 与 `/predict` 接口
- 提供 Dockerfile（内置模型）、基础健康检查
- CI: PR/Push 触发的 lint、测试、训练烟囱并上传模型工件

指标（示例，实际以 CI 输出为准）
```
rmse: ~53-56 (seed=42)
```

后续 v0.2 计划：
- 尝试 Ridge 或 RandomForestRegressor
- 可能加入阈值转换为“高风险”标记，并报告 precision/recall
- 在此文件中展示 v0.1 -> v0.2 的指标对比与改动理由

## v0.2 (Improvement)

- 增加命令行参数与多模型选择：`--model lin|ridge|rf`，默认 v0.2 使用 `ridge`
- 工作流根据 Tag 版本自动选择训练参数，发布 Release 附上对应 `metrics-v0.2.json`
- 目标：在 RMSE 上较 v0.1 有可观下降（数值以 CI 训练结果为准）

对比（占位，发布后填入具体数值）：
```
v0.1 RMSE: <x.xx>
v0.2 RMSE: <y.yy>  (Δ = <x.xx - y.yy>)
```



