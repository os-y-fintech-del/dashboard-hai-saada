#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from datetime import datetime

app = Flask(__name__)

def get_data():
    return {
        'total_sales': 14304084,
        'collected': 8415474.1,
        'collection_rate': 58.8,
        'completion': 56,
        'trust_total': 7928625.1,
        'charity': 286081.68,
        'total_units': 40,
        'sold_units': 25,
        'remaining_sales': 5888610,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def format_number(num):
    if num == 0:
        return "0"
    return f"{num:,.0f}"

@app.route('/')
def dashboard():
    data = get_data()
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة البيانات | قصر القصور</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: "Cairo", sans-serif; background: linear-gradient(135deg, #F5F2EB 0%, #E8E2D2 100%); color: #0F1114; direction: rtl; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1420px; margin: 0 auto; background: #FFF; border-radius: 20px; overflow: hidden; box-shadow: 0 24px 80px rgba(15, 17, 20, 0.15); }}
        .topbar {{ background: linear-gradient(135deg, #FFF 0%, #F5F2EB 100%); border-bottom: 1px solid #E8E5DD; padding: 22px 32px; display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ display: flex; align-items: center; gap: 16px; }}
        .brand-text h1 {{ font-size: 20px; font-weight: 800; }}
        .brand-text p {{ font-size: 12px; color: #8B8F96; margin-top: 4px; }}
        .badge {{ background: linear-gradient(135deg, #B8915F, #8A6A3F); color: #FFF; font-size: 11px; font-weight: 700; padding: 7px 14px; border-radius: 24px; }}
        .main {{ padding: 28px; background: #F5F2EB; }}
        .hero {{ background: linear-gradient(135deg, #0F1114 0%, #2A2D33 100%); border-radius: 18px; padding: 32px 36px; margin-bottom: 26px; color: #FFF; }}
        .hero h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 12px; }}
        .section-title {{ font-size: 17px; font-weight: 800; margin-bottom: 16px; display: flex; align-items: center; gap: 12px; }}
        .section-title::before {{ content: ""; width: 5px; height: 22px; background: linear-gradient(180deg, #B8915F, #8A6A3F); border-radius: 3px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
        .kpi-card {{ background: #FFF; border: 1px solid #E8E5DD; border-radius: 14px; padding: 20px; position: relative; overflow: hidden; }}
        .kpi-card::before {{ content: ""; position: absolute; top: 0; right: 0; width: 4px; height: 100%; }}
        .kpi-card.gold::before {{ background: linear-gradient(180deg, #D4AE7E, #8A6A3F); }}
        .kpi-card.danger::before {{ background: linear-gradient(180deg, #D08585, #B85959); }}
        .kpi-card.success::before {{ background: linear-gradient(180deg, #5A9B6E, #4A7C5B); }}
        .kpi-icon {{ font-size: 24px; margin-bottom: 12px; }}
        .kpi-label {{ font-size: 12px; color: #8B8F96; font-weight: 600; margin-bottom: 6px; text-transform: uppercase; }}
        .kpi-value {{ font-size: 24px; font-weight: 900; color: #0F1114; margin-bottom: 8px; }}
        .card {{ background: #FFF; border: 1px solid #E8E5DD; border-radius: 14px; padding: 22px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        table tr {{ border-bottom: 1px solid #E8E5DD; }}
        table td {{ padding: 12px; text-align: right; }}
        table td:first-child {{ color: #8B8F96; font-weight: 600; }}
        footer {{ background: #F5F2EB; border-top: 1px solid #E8E5DD; padding: 20px; text-align: center; font-size: 12px; color: #8B8F96; }}
        @media (max-width: 768px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="topbar">
            <div class="brand">
                <div><div style="font-size: 40px;">🏢</div></div>
                <div class="brand-text">
                    <h1>قصر القصور</h1>
                    <p>نبني بجودة واحسان</p>
                </div>
            </div>
            <div class="badge">📊 Live</div>
        </div>
        
        <div class="main">
            <div class="hero">
                <h2>حي السعادة 132</h2>
                <p>مشروع سكني متطور في الرياض</p>
            </div>
            
            <div class="section-title">المؤشرات الرئيسية</div>
            <div class="kpi-grid">
                <div class="kpi-card danger">
                    <div class="kpi-icon">❤️</div>
                    <div class="kpi-label">الأعمال الخيرية</div>
                    <div class="kpi-value">{format_number(data['charity'])} ر.س</div>
                </div>
                <div class="kpi-card gold">
                    <div class="kpi-icon">📊</div>
                    <div class="kpi-label">إجمالي المبيعات</div>
                    <div class="kpi-value">{format_number(data['total_sales'])} ر.س</div>
                </div>
                <div class="kpi-card gold">
                    <div class="kpi-icon">💵</div>
                    <div class="kpi-label">الدفعات المحصلة</div>
                    <div class="kpi-value">{format_number(data['collected'])} ر.س</div>
                </div>
                <div class="kpi-card success">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-label">رصيد الضمان</div>
                    <div class="kpi-value">{format_number(data['trust_total'])} ر.س</div>
                </div>
                <div class="kpi-card gold">
                    <div class="kpi-icon">📈</div>
                    <div class="kpi-label">نسبة التحصيل</div>
                    <div class="kpi-value">{data['collection_rate']:.1f}%</div>
                </div>
            </div>
            
            <div class="card">
                <div class="section-title">تحليل الأداء</div>
                <table>
                    <tr><td>نسبة الإنجاز</td><td style="font-weight: 700;">{data['completion']:.0f}%</td></tr>
                    <tr><td>نسبة التحصيل</td><td style="font-weight: 700;">{data['collection_rate']:.1f}%</td></tr>
                    <tr><td>الوحدات المباعة</td><td style="font-weight: 700;">{data['sold_units']} من {data['total_units']}</td></tr>
                    <tr><td>المتبقي من المبيعات</td><td style="font-weight: 700;">{format_number(data['remaining_sales'])} ر.س</td></tr>
                </table>
            </div>
        </div>
        
        <footer>
            <strong>حي السعادة 132</strong> · شركة قصر القصور · الرياض
            <br><small>تم التحديث: {data['timestamp']}</small>
        </footer>
    </div>
    <script>setInterval(function() {{ location.reload(); }}, 10000);</script>
</body>
</html>"""
    
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
