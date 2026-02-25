#!/usr/bin/env python3
"""
三星股价自动更新脚本
使用多个数据源获取三星电子(005930.KS / 005930 KS Equity)的实时股价
"""

import urllib.request
import json
import ssl
import time
import os

def get_stock_from_yahoo():
    """从Yahoo Finance获取数据 - 三星电子 005930.KS (005930 KS Equity)"""
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/005930.KS?interval=1d&range=1d'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            data = json.loads(response.read().decode())
            result = data['chart']['result'][0]
            meta = result['meta']
            
            return {
                'price': meta.get('regularMarketPrice', 0),
                'previous_close': meta.get('previousClose', 0),
                'open': meta.get('regularMarketDayOpen', 0),
                'high': meta.get('regularMarketDayHigh', 0),
                'low': meta.get('regularMarketDayLow', 0),
                'currency': meta.get('currency', 'KRW'),
                'timestamp': meta.get('regularMarketTime', 0)
            }
    except Exception as e:
        print(f'Yahoo Finance error: {e}')
        return None

def get_stock_from_google():
    """从Google Finance获取数据 - 三星电子 005930:KRX"""
    url = 'https://www.google.com/finance/quote/005930:KRX'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
            html = response.read().decode('utf-8')
            
            # 提取股价数据
            import re
            # 查找 ["205000"] 格式
            match = re.search(r'\[(\d{5,6})\]', html)
            if match:
                price = int(match.group(1))
                return {
                    'price': price,
                    'previous_close': 0,
                    'open': 0,
                    'high': 0,
                    'low': 0,
                    'currency': 'KRW',
                    'timestamp': int(time.time())
                }
    except Exception as e:
        print(f'Google Finance error: {e}')
        return None

def get_samsung_stock():
    """
    获取三星电子(005930.KS / 005930 KS Equity)股价
    尝试多个数据源
    """
    # 尝试Yahoo Finance
    data = get_stock_from_yahoo()
    if data and data['price'] > 0:
        return data
    
    # 尝试Google Finance
    data = get_stock_from_google()
    if data and data['price'] > 0:
        return data
    
    return None

def save_stock_data(data):
    """保存股价数据到JSON文件"""
    if not data:
        return
    
    # 计算市值 (亿美元)
    # 三星总股本约 5.968 billion shares
    shares = 5.968
    market_cap_usd = data['price'] * shares / 10000 / 1300  # 简算汇率1300
    
    output = {
        'symbol': '005930.KS',
        'price_krw': data['price'],
        'market_cap_usd': round(market_cap_usd, 2),
        'previous_close': data['previous_close'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'currency': data['currency'],
        'timestamp': data['timestamp'],
        'updated_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    }
    
    with open('/root/.openclaw/workspace/samsung_stock.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Stock data saved: {output['price_krw']:,} KRW, Market Cap: {output['market_cap_usd']}B USD")

if __name__ == '__main__':
    print(f"Fetching Samsung stock data at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
    data = get_samsung_stock()
    if data:
        save_stock_data(data)
        print(f"Success: Price = {data['price']:,} KRW")
    else:
        print("Failed to fetch stock data")
