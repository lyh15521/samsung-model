# Samsung Financial Model

三星电子财务模型 - 自动更新股价版本

## 功能特性

- 📊 可视化财务模型，完整复刻Excel钩稽关系
- 🟡 黄色可编辑单元格（2026E、2027E预测数据）
- 🔄 自动更新股价和市值数据（每天韩国股市收盘后）
- 📈 实时计算PE、EPS等关键指标

## 股票代码

- **Yahoo Finance**: 005930.KS
- **Bloomberg**: 005930 KS Equity
- **交易所**: KRX (韩国交易所)

## 自动更新设置

已配置GitHub Actions，每天自动运行：
- **时间**: 15:30 KST (韩国时间)
- **频率**: 周一至周五（股市交易日）
- **数据源**: Yahoo Finance

## 本地开发

```bash
# 启动本地服务器
python -m http.server 8080

# 访问 http://localhost:8080
```

## 文件结构

```
.
├── index.html              # 主网页
├── .github/
│   └── workflows/
│       └── update-stock.yml # 自动更新工作流
├── scripts/
│   └── update_stock.py     # 股价更新脚本
├── stock_data.json         # 股价数据（自动更新）
└── README.md
```

## 技术栈

- 前端: HTML5 + CSS3 + Vanilla JavaScript
- 自动化: GitHub Actions + Python
- 数据源: Yahoo Finance API

## License

MIT
