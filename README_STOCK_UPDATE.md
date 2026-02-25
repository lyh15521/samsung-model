# 三星财务模型 - 自动股价更新系统

## 系统架构

### 1. 数据来源
由于免费API的限制，系统使用以下方式获取三星(005930.KS)股价：

**主要方案**: Yahoo Finance API (通过Python脚本)
- 股票代码: 005930.KS
- 数据包括: 当前价格、开盘价、最高价、最低价、前收盘价
- 更新频率: 韩国股市收盘后

**备用方案**: 手动更新JSON文件
- 文件位置: `samsung_stock.json`
- 格式: `{"price_krw": 205000, "market_cap_usd": 1213.53, "updated_at": "2024-01-01 15:30:00"}`

### 2. 自动更新设置

已配置的Cron任务:
- **时间**: 每天下午3:00 (韩国时间 KST)
- **频率**: 周一至周五 (股市交易日)
- **时区**: Asia/Seoul
- **任务ID**: 3cffc717-bd89-41df-9844-b99a246d93c9

### 3. 韩国股市交易时间
- **早盘**: 09:00 - 12:00 KST
- **午盘**: 13:00 - 15:30 KST
- **收盘**: 15:30 KST

Cron设置在15:00运行，确保收盘数据可用。

### 4. 文件说明

| 文件 | 说明 |
|------|------|
| `samsung_model.html` | 主网页文件，包含可视化模型 |
| `fetch_stock.py` | 股价获取脚本 |
| `samsung_stock.json` | 股价数据存储文件 |
| `README_STOCK_UPDATE.md` | 本说明文件 |

### 5. 手动更新股价

如果自动获取失败，可以手动创建/更新 `samsung_stock.json`:

```json
{
  "symbol": "005930.KS",
  "price_krw": 205000,
  "market_cap_usd": 1213.53,
  "previous_close": 200000,
  "open": 202500,
  "high": 206000,
  "low": 201000,
  "currency": "KRW",
  "timestamp": 1704067200,
  "updated_at": "2024-01-01 15:30:00"
}
```

### 6. 网页自动刷新

网页会:
1. 加载时自动读取 `samsung_stock.json` 中的股价和市值
2. 每5分钟自动刷新一次数据
3. 显示上次更新时间

### 7. 免费API限制说明

由于使用的是免费数据源，可能会遇到:
- 请求频率限制 (Rate Limit)
- 偶尔的数据延迟
- IP封禁风险

如遇问题，建议:
- 使用手动更新JSON文件
- 或购买付费API服务 (如Alpha Vantage、Bloomberg等)

### 8. 更新Cron任务

如需修改自动更新时间:

```bash
# 查看当前任务
openclaw cron list

# 删除旧任务
openclaw cron remove --id 3cffc717-bd89-41df-9844-b99a246d93c9

# 添加新任务 (例如改为每天15:30)
openclaw cron add --name "Samsung Stock Update" --schedule "30 15 * * 1-5" --timezone "Asia/Seoul" --command "python3 /root/.openclaw/workspace/fetch_stock.py"
```

## 技术细节

### 市值计算
```
市值(亿美元) = 股价(KRW) × 总股本(5.968B) / 汇率(约1300) / 10000
```

### PE计算
```
PE = 股价 / EPS
```

其中EPS来自财务模型计算:
```
EPS = Net Income × 1000 / Shares
```
