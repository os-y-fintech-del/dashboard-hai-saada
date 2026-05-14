#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Server - حي السعادة 132
تطبيق ويب حي يعرض بيانات الإكسل بشكل مستمر
"""

from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)

# ===== CONFIGURATION =====
EXCEL_FILE = "dashboard_data.xlsx"

def extract_dashboard_value(df, label_text, column_index=2):
    """استخراج قيمة من شيت Dashboard"""
    try:
        for idx, row in df.iterrows():
            if pd.notna(row[1]):
                cell_value = str(row[1]).strip()
                if label_text in cell_value:
                    if pd.notna(row[column_index]):
                        return float(row[column_index])
        return 0
    except:
        return 0

def get_dashboard_data():
    """قراءة بيانات Dashboard من الإكسل"""
    try:
        if not os.path.exists(EXCEL_FILE):
            return None
            
        df_dashboard = pd.read_excel(EXCEL_FILE, sheet_name='Dashboard', header=None)
        
        total_sales = extract_dashboard_value(df_dashboard, "إجمالي المبيعات لكامل المشروع")
        collected = extract_dashboard_value(df_dashboard, "الدفعات المحصلة")
        collection_rate = extract_dashboard_value(df_dashboard, "نسبة التحصيل من كامل المشروع") * 100
        completion = extract_dashboard_value(df_dashboard, "نسبة الإنجاز الفعلية") * 100
        trust_total = extract_dashboard_value(df_dashboard, "الإجمالي", 4)
        
        # قراءة الوحدات
        df_units = pd.read_excel(EXCEL_FILE, sheet_name='العملاء والوحدات')
        
        total_units = 0
        sold_units = 0
        
        for idx, row in df_dashboard.iterrows():
            if pd.notna(row[1]):
                cell_value = str(row[1]).strip()
                if "عدد الوحدات" in cell_value and "المباعة" not in cell_value:
                    if pd.notna(row[2]):
                        total_units = int(float(row[2]))
                elif "عدد الوحدات المباعة" in cell_value:
                    if pd.notna(row[2]):
                        sold_units = int(float(row[2]))
        
        data = {
            'total_sales': total_sales,
            'collected': collected,
            'collection_rate': collection_rate,
            'completion': completion,
            'trust_total': trust_total,
            'charity': total_sales * 0.02,
            'total_units': total_units,
            'sold_units': sold_units,
            'available_units': total_units - sold_units,
            'remaining_sales': total_sales - collected,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return data
    except Exception as e:
        print(f"خطأ: {e}")
        return None

def format_number(num):
    """تنسيق الأرقام"""
    if num is None or num == 0:
        return "0"
    return f"{num:,.0f}"

@app.route('/api/data')
def api_data():
    """API لإرجاع البيانات JSON"""
    data = get_dashboard_data()
    if data:
        return jsonify(data)
    return jsonify({'error': 'No data'}), 500

@app.route('/')
def dashboard():
    """الصفحة الرئيسية للداش بورد"""
    data = get_dashboard_data()
    
    if not data:
        return "خطأ في تحميل البيانات", 500
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة البيانات | قصر القصور</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        :root {{
            --white: #FFFFFF;
            --cream: #F5F2EB;
            --gold: #B8915F;
            --gold-l: #D4AE7E;
            --gold-d: #8A6A3F;
            --slate: #2A2D33;
            --black: #0F1114;
            --text: #0F1114;
            --muted: #8B8F96;
            --line: #E8E5DD;
            --success: #4A7C5B;
            --success-bg: #E8F1EB;
            --danger: #B85959;
            --danger-bg: #F5E6E6;
        }}
        
        body {{
            font-family: "Cairo", sans-serif;
            background: linear-gradient(135deg, #F5F2EB 0%, #E8E2D2 100%);
            color: var(--text);
            direction: rtl;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1420px;
            margin: 0 auto;
            background: var(--white);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 24px 80px rgba(15, 17, 20, 0.15);
            border: 1px solid var(--line);
        }}
        
        .topbar {{
            background: linear-gradient(135deg, var(--white) 0%, var(--cream) 100%);
            border-bottom: 1px solid var(--line);
            padding: 22px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
        }}
        
        .topbar::before {{
            content: "";
            position: absolute;
            bottom: 0; right: 0; left: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--gold) 0%, var(--gold-l) 50%, var(--gold) 100%);
        }}
        
        .brand {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .brand-logo {{
            width: 72px;
            height: 72px;
            border-radius: 14px;
            overflow: hidden;
            background: var(--white);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 6px;
            box-shadow: 0 4px 14px rgba(15, 17, 20, 0.15);
            border: 1px solid var(--line);
            font-size: 40px;
        }}
        
        .brand-text h1 {{
            font-size: 20px;
            font-weight: 800;
            color: var(--black);
            letter-spacing: -0.3px;
            line-height: 1.2;
        }}
        
        .brand-text p {{
            font-size: 12px;
            color: var(--muted);
            margin-top: 4px;
        }}
        
        .topbar-badge {{
            background: linear-gradient(135deg, var(--gold), var(--gold-d));
            color: var(--white);
            font-size: 11px;
            font-weight: 700;
            padding: 7px 14px;
            border-radius: 24px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        .main {{
            padding: 28px;
            background: var(--cream);
        }}
        
        .hero {{
            background: linear-gradient(135deg, var(--black) 0%, var(--slate) 100%);
            border-radius: 18px;
            overflow: hidden;
            margin-bottom: 26px;
            padding: 32px 36px;
            min-height: 280px;
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
            align-items: center;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
        }}
        
        .hero-tag {{
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            color: var(--gold-l);
            background: rgba(184, 145, 95, 0.15);
            padding: 5px 12px;
            border-radius: 20px;
            margin-bottom: 16px;
            letter-spacing: 1px;
        }}
        
        .hero h2 {{
            font-size: 32px;
            font-weight: 900;
            color: var(--white);
            line-height: 1.25;
            margin-bottom: 12px;
        }}
        
        .hero .lead {{
            font-size: 14px;
            color: rgba(245, 242, 235, 0.75);
            line-height: 1.75;
            margin-bottom: 20px;
        }}
        
        .hero-meta {{
            display: flex;
            gap: 12px;
            margin-top: 22px;
            flex-wrap: wrap;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--cream);
            font-size: 12px;
            font-weight: 600;
            padding: 6px 12px;
            background: rgba(184, 145, 95, 0.1);
            border-radius: 8px;
            border: 1px solid rgba(184, 145, 95, 0.25);
        }}
        
        .section-title {{
            font-size: 17px;
            font-weight: 800;
            color: var(--black);
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .section-title::before {{
            content: "";
            width: 5px;
            height: 22px;
            background: linear-gradient(180deg, var(--gold), var(--gold-d));
            border-radius: 3px;
        }}
        
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .kpi-card {{
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 20px;
            position: relative;
            overflow: hidden;
            transition: transform 0.25s, box-shadow 0.25s;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(15, 17, 20, 0.1);
        }}
        
        .kpi-card::before {{
            content: "";
            position: absolute;
            top: 0;
            right: 0;
            width: 4px;
            height: 100%;
        }}
        
        .kpi-card.gold::before {{ background: linear-gradient(180deg, var(--gold-l), var(--gold-d)); }}
        .kpi-card.danger::before {{ background: linear-gradient(180deg, #D08585, var(--danger)); }}
        .kpi-card.success::before {{ background: linear-gradient(180deg, #5A9B6E, var(--success)); }}
        
        .kpi-icon {{
            width: 38px;
            height: 38px;
            background: var(--cream);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-bottom: 12px;
        }}
        
        .kpi-label {{
            font-size: 12px;
            color: var(--muted);
            font-weight: 600;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .kpi-value {{
            font-size: 24px;
            font-weight: 900;
            color: var(--black);
            display: flex;
            align-items: baseline;
            gap: 4px;
            margin-bottom: 8px;
            word-break: break-word;
        }}
        
        .kpi-value span {{
            font-size: 12px;
            color: var(--muted);
            font-weight: 600;
        }}
        
        .kpi-delta {{
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 600;
            display: inline-block;
        }}
        
        .kpi-delta.up {{ background: var(--success-bg); color: var(--success); }}
        .kpi-delta.neutral {{ background: var(--danger-bg); color: var(--danger); }}
        
        .card {{
            background: var(--white);
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 18px;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            direction: rtl;
        }}
        
        table tr {{
            border-bottom: 1px solid var(--line);
        }}
        
        table td {{
            padding: 12px;
            text-align: right;
        }}
        
        table td:first-child {{
            color: var(--muted);
            font-weight: 600;
        }}
        
        table tr:last-child td {{
            border-bottom: none;
        }}
        
        footer {{
            background: var(--cream);
            border-top: 1px solid var(--line);
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: var(--muted);
            margin-top: 40px;
        }}
        
        footer strong {{
            color: var(--black);
            font-weight: 700;
        }}
        
        @media (max-width: 1200px) {{
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
        
        @media (max-width: 768px) {{
            .kpi-grid {{ grid-template-columns: 1fr; }}
            .hero {{ padding: 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- TOPBAR -->
        <div class="topbar">
            <div class="brand">
                <div class="brand-logo">🏢</div>
                <div class="brand-text">
                    <h1>قصر القصور</h1>
                    <p>نبني بجودة واحسان</p>
                </div>
            </div>
            <div class="topbar-badge">📊 نسخة مباشرة (Live)</div>
        </div>
        
        <!-- MAIN CONTENT -->
        <div class="main">
            <!-- HERO -->
            <div class="hero">
                <div class="hero-content">
                    <div class="hero-tag">نظرة عامة</div>
                    <h2>حي السعادة 132</h2>
                    <p class="lead">مشروع سكني متطور في قلب الرياض، يجمع بين الجودة والابتكار</p>
                    <div class="hero-meta">
                        <div class="meta-item">
                            <span>📅</span>
                            <span>بدأ: 2025-06-01</span>
                        </div>
                        <div class="meta-item">
                            <span>⏱️</span>
                            <span>المدة: 15 شهر</span>
                        </div>
                        <div class="meta-item">
                            <span>📍</span>
                            <span>الرياض</span>
                        </div>
                        <div class="meta-item">
                            <span>✓</span>
                            <span>الإنجاز: {data['completion']:.0f}%</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- KPI CARDS -->
            <div class="section-title">المؤشرات الرئيسية</div>
            <div class="kpi-grid">
                <!-- الأعمال الخيرية -->
                <div class="kpi-card danger">
                    <div class="kpi-icon">❤️</div>
                    <div class="kpi-label">الأعمال الخيرية</div>
                    <div class="kpi-value">{format_number(data['charity'])} <span>ر.س</span></div>
                    <div class="kpi-delta neutral">2% من المبيعات</div>
                </div>
                
                <!-- إجمالي المبيعات -->
                <div class="kpi-card gold">
                    <div class="kpi-icon">📊</div>
                    <div class="kpi-label">إجمالي المبيعات</div>
                    <div class="kpi-value">{format_number(data['total_sales'])} <span>ر.س</span></div>
                    <div class="kpi-delta up">{data['sold_units']} وحدة مباعة</div>
                </div>
                
                <!-- الدفعات المحصلة -->
                <div class="kpi-card gold">
                    <div class="kpi-icon">💵</div>
                    <div class="kpi-label">الدفعات المحصلة</div>
                    <div class="kpi-value">{format_number(data['collected'])} <span>ر.س</span></div>
                    <div class="kpi-delta neutral">المبلغ المستلم فعلياً</div>
                </div>
                
                <!-- رصيد حساب الضمان -->
                <div class="kpi-card success">
                    <div class="kpi-icon">💰</div>
                    <div class="kpi-label">رصيد الضمان</div>
                    <div class="kpi-value">{format_number(data['trust_total'])} <span>ر.س</span></div>
                    <div class="kpi-delta up">متاح للصرف</div>
                </div>
                
                <!-- نسبة التحصيل -->
                <div class="kpi-card gold">
                    <div class="kpi-icon">📈</div>
                    <div class="kpi-label">نسبة التحصيل</div>
                    <div class="kpi-value">{data['collection_rate']:.1f}<span>%</span></div>
                    <div class="kpi-delta neutral">من إجمالي المبيعات</div>
                </div>
            </div>
            
            <!-- ANALYSIS CARD -->
            <div class="card">
                <div class="section-title">تحليل الأداء</div>
                <table>
                    <tr style="border-bottom: 1px solid var(--line);">
                        <td style="color: var(--muted); font-weight: 600;">المؤشر</td>
                        <td style="color: var(--muted); font-weight: 600;">القيمة</td>
                        <td style="color: var(--muted); font-weight: 600;">الملاحظة</td>
                    </tr>
                    <tr>
                        <td>نسبة الإنجاز</td>
                        <td style="font-weight: 700;">{data['completion']:.0f}%</td>
                        <td style="color: var(--success);">✓ على المسار الصحيح</td>
                    </tr>
                    <tr>
                        <td>نسبة التحصيل</td>
                        <td style="font-weight: 700;">{data['collection_rate']:.1f}%</td>
                        <td style="color: var(--gold-d);">قيد المتابعة</td>
                    </tr>
                    <tr>
                        <td>المتبقي من المبيعات</td>
                        <td style="font-weight: 700;">{format_number(data['remaining_sales'])} ر.س</td>
                        <td style="color: var(--muted);">مستهدف الربع القادم</td>
                    </tr>
                    <tr>
                        <td>الوحدات المتاحة</td>
                        <td style="font-weight: 700;">{data['available_units']} وحدة</td>
                        <td style="color: var(--muted);">من أصل {data['total_units']}</td>
                    </tr>
                </table>
            </div>
        </div>
        
        <!-- FOOTER -->
        <footer>
            <strong>حي السعادة · مشروع 132</strong> · شركة قصر القصور للاستثمار · الرياض
            <br>
            <small>تم التحديث: {data['timestamp']}</small>
        </footer>
    </div>
    
    <script>
        // تحديث الصفحة كل 10 ثوانٍ
        setInterval(function() {{
            location.reload();
        }}, 10000);
    </script>
</body>
</html>"""
    
    return html

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 تطبيق الداش بورد جاهز!")
    print("=" * 60)
    print("📍 الرابط: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
