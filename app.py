import streamlit as st
import cv2
import numpy as np

# --- 1. تهيئة إعدادات الصفحة ---
st.set_page_config(
    page_title="ZINO AgroVision Engine",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. التصميم البصري (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f1c40f !important;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .zino-header {
        background-color: #0d1117;
        border: 2px solid #000000;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
    }
    .zino-title-pill {
        background: linear-gradient(90deg, #f39c12, #f1c40f);
        color: #000000;
        display: inline-block;
        padding: 8px 28px;
        border-radius: 25px;
        font-weight: 900;
        font-size: 2.1rem;
        margin-bottom: 8px;
    }
    .zino-subtitle {
        color: #c9d1d9;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 600;
    }
    .zino-dev-badge {
        display: inline-block;
        background-color: #161b22;
        color: #f1c40f;
        border: 1px solid #f1c40f;
        border-radius: 20px;
        padding: 5px 18px;
        font-size: 0.9rem;
        font-weight: 700;
        margin-top: 10px;
    }
    .zino-card {
        background-color: #0d1117;
        border: 2px solid #161b22;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        color: #f0f6fc;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.35);
    }
    div.stButton > button {
        background: linear-gradient(90deg, #0052d4, #4364f7, #6fb1fc) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        padding: 16px 24px !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 16px rgba(0, 82, 212, 0.5) !important;
        cursor: pointer !important;
    }
    .report-title {
        color: #f1c40f;
        font-size: 1.35rem;
        font-weight: bold;
        margin-bottom: 14px;
        border-bottom: 1.5px solid #30363d;
        padding-bottom: 8px;
    }
    .zino-footer {
        background-color: #0d1117;
        border: 1.5px solid #161b22;
        border-radius: 10px;
        text-align: center;
        padding: 14px;
        color: #f1c40f;
        font-weight: bold;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. القاموس المعتمد للغات الخمس ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "تصميم وتطوير إسماعيل حساسنة",
        "upload_label": "قم برفع صورة ورقة النبات للتحليل المكتبي والدقيق",
        "run_btn": "🔬 تشغيل تحليل الرؤية الحاسوبية والحساب الرقمي",
        "report_title": "📊 تقرير التحليل الرقمي لسطح الورقة (Leaf Surface Analysis)",
        "healthy_ratio": "نسبة النسيج الأخضر الحيوية",
        "infected_ratio": "نسبة التجهد والتغير التصبغي",
        "lesion_count": "عدد مناطق التغير النسيجي",
        "status_done": "تم معالجة مصفوفة البكسلات وعزل الخلفية بنجاح",
        "heatmap_label": "تجزئة جسم الورقة وتحديد مناطق التجهد (Leaf Isolation & Stress Mapping)",
        "tech_title": "⚙️ محرك المعالجة الرياضية",
        "tech_desc": "محرك يعتمد على عزل خلفية المشهد ومقاييس الألوان الطيفية ببيئة HSV بكسل ببكسل."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "Designed and Developed by Ismail Hassasneh",
        "upload_label": "Upload Leaf Image for Quantitative Analysis",
        "run_btn": "🔬 Run Computer Vision & Pixel Analysis Engine",
        "report_title": "📊 Quantitative Leaf Surface Analysis Report",
        "healthy_ratio": "Vital Green Tissue Ratio",
        "infected_ratio": "Discolored / Stressed Area Ratio",
        "lesion_count": "Detected Anomaly Regions",
        "status_done": "Background Segmented & Pixel Matrix Processed",
        "heatmap_label": "Leaf Contour Segmentation & Stress Mapping",
        "tech_title": "⚙️ Vision Engine Specs",
        "tech_desc": "Strict background-subtracted spatial analysis using HSV color spaces and contour topology."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Система компьютерного зрения | Количественная диагностика поверхности листа",
        "dev_by": "Дизайн и разработка: Исмаил Хассасне",
        "upload_label": "Загрузить изображение листа для анализа",
        "run_btn": "🔬 Запустить компьютерный анализ пикселей",
        "report_title": "📊 Отчет о количественном анализе поверхности листа",
        "healthy_ratio": "Доля здоровой зеленой ткани",
        "infected_ratio": "Доля измененной/стрессовой ткани",
        "lesion_count": "Обнаружено аномальных зон",
        "status_done": "Сегментация фона и анализ пикселей завершены",
        "heatmap_label": "Сегментация контура листа и карта стресса",
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": "Пространственный анализ с удалением фона на основе цветовых пространств HSV."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Görme Motoru | Nicel Yaprak Yüzeyi Teşhisi",
        "dev_by": "Tasarım ve Geliştirme: İsmail Hassasneh",
        "upload_label": "Nicel Analiz İçin Yaprak Resmi Yükleyin",
        "run_btn": "🔬 Bilgisayarlı Görme ve Piksel Analizini Çalıştır",
        "report_title": "📊 Nicel Yaprak Yüzeyi Analiz Raporu",
        "healthy_ratio": "Canlı Yeşil Doku Oranı",
        "infected_ratio": "Renk Değişimi / Stresli Alan Oranı",
        "lesion_count": "Tespit Edilen Anomali Bölgesi",
        "status_done": "Arka Plan Ayrıştırıldı ve Piksel Matrisi İşlendi",
        "heatmap_label": "Yaprak Kontur Segmentasyonu ve Stres Haritası",
        "tech_title": "⚙️ Motor Özellikleri",
        "tech_desc": "HSV renk alanları ve kontur topolojisi kullanılarak yapılan arka plan çıkarmalı analiz."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业视觉引擎 | 叶片表面定量诊断",
        "dev_by": "设计与开发：Ismail Hassasneh",
        "upload_label": "上传叶片图像进行定量分析",
        "run_btn": "🔬 运行计算机视觉与像素分析引擎",
        "report_title": "📊 叶片表面定量分析报告",
        "healthy_ratio": "绿色健康组织比例",
        "infected_ratio": "受损 / 变色区域比例",
        "lesion_count": "检测到的异常区域数量",
        "status_done": "背景分割与像素矩阵处理完成",
        "heatmap_label": "叶片轮廓分割与应力热力图",
        "tech_title": "⚙️ 视觉引擎规格",
        "tech_desc": "基于 HSV 色彩空间和轮廓拓扑的前景背景分割与定量空间分析。"
    }
}

# --- 4. الشريط الجانبي ---
lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English", "Русский", "Türkçe", "中文"])
t = TEXTS[lang]

st.sidebar.markdown(f"### 👨‍💻 {t['dev_by']}")
st.sidebar.markdown("---")
st.sidebar.subheader(t["tech_title"])
st.sidebar.info(t["tech_desc"])

# --- 5. الهيدر الرئيسي ---
st.markdown(f"""
    <div class="zino-header">
        <div class="zino-title-pill">🌱 {t['title']}</div>
        <p class="zino-subtitle">{t['subtitle']}</p>
        <div class="zino-dev-badge">{t['dev_by']}</div>
    </div>
""", unsafe_allow_html=True)

# --- 6. رفع الصورة والتفعيل ---
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    st.markdown('<div class="zino-card">', unsafe_allow_html=True)
    st.image(img_rgb, caption="Input Leaf Image", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(t["run_btn"]):
        # --- خوارزمية عزل خلفية الورقة الدقيقة (Leaf Isolation Pipeline) ---
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        
        # 1. تحديد نطاقات اللون الخاص بجسم الورقة الكلي (الأخضر والأصفر والداكن)
        lower_leaf = np.array([15, 25, 20])
        upper_leaf = np.array([95, 255, 255])
        raw_leaf_mask = cv2.inRange(hsv, lower_leaf, upper_leaf)
        
        # التنظيف المورفولوجي لمنع الضوضاء
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        cleaned_leaf_mask = cv2.morphologyEx(raw_leaf_mask, cv2.MORPH_CLOSE, kernel)
        cleaned_leaf_mask = cv2.morphologyEx(cleaned_leaf_mask, cv2.MORPH_OPEN, kernel)
        
        # استخراج أكبر مجسم (جسم الورقة الرئيسي فقط) وإلغاء خلفية الكرتون/الطاولة
        contours_leaf, _ = cv2.findContours(cleaned_leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        leaf_mask = np.zeros_like(cleaned_leaf_mask)
        if contours_leaf:
            largest_contour = max(contours_leaf, key=cv2.contourArea)
            cv2.drawContours(leaf_mask, [largest_contour], -1, 255, -1)
        else:
            leaf_mask = cleaned_leaf_mask

        # 2. قياس المساحة الإجمالية لجسم الورقة فقط (Leaf Surface Area)
        total_leaf_pixels = float(cv2.countNonZero(leaf_mask))
        
        if total_leaf_pixels > 0:
            # 3. عزل البكسلات الخضراء الحيوية داخل حدود الورقة حصراً
            lower_green = np.array([28, 40, 40])
            upper_green = np.array([85, 255, 255])
            green_mask_raw = cv2.inRange(hsv, lower_green, upper_green)
            healthy_leaf_mask = cv2.bitwise_and(green_mask_raw, green_mask_raw, mask=leaf_mask)
            
            healthy_pixels = float(cv2.countNonZero(healthy_leaf_mask))
            
            # 4. حساب مناطق التجهد/التغير التصبغي داخل الورقة حصراً
            stressed_leaf_mask = cv2.bitwise_and(cv2.bitwise_not(green_mask_raw), cv2.bitwise_not(green_mask_raw), mask=leaf_mask)
            
            # 5. تتبع محيطات التغيرات التصبغية داخل جسم الورقة
            contours_stress, _ = cv2.findContours(stressed_leaf_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            contoured_img = img_rgb.copy()
            valid_anomalies = 0
            for cnt in contours_stress:
                # رسم التحديد فقط إذا كانت البقعة داخل حدود الورقة ومساحتها واضحة
                if cv2.contourArea(cnt) > 25:
                    valid_anomalies += 1
                    cv2.drawContours(contoured_img, [cnt], -1, (255, 0, 0), 2)
            
            # 6. الرياضيات الحسابية لمساحة الورقة الحقيقية
            healthy_pct = (healthy_pixels / total_leaf_pixels) * 100.0
            stressed_pct = max(0.0, 100.0 - healthy_pct)
            
            # 7. تطبيق الخريطة الحرارية الموجهة لجسم الورقة فقط
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            heatmap_full = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
            heatmap_rgb = cv2.cvtColor(heatmap_full, cv2.COLOR_BGR2RGB)
            heatmap_masked = cv2.bitwise_and(heatmap_rgb, heatmap_rgb, mask=leaf_mask)
            
            # --- 8. عرض نتائج التقرير المعتمد ---
            st.markdown('<div class="zino-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="report-title">{t["report_title"]}</div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(label=t["healthy_ratio"], value=f"{healthy_pct:.2f}%")
            with c2:
                st.metric(label=t["infected_ratio"], value=f"{stressed_pct:.2f}%")
            with c3:
                st.metric(label=t["lesion_count"], value=f"{valid_anomalies}")
                
            st.info(f"📌 {t['status_done']}")
            
            # التقييم بناءً على النسب الرقمية المحسوبة
            if healthy_pct >= 80.0:
                st.success("✅ **مؤشر النسيج:** النسيج النباتي الأخضر غني جداً بالكلوروفيل وفي حالة نمو ممتازة.")
            elif healthy_pct >= 50.0:
                st.warning("⚠️ **مؤشر النسيج:** تم رصد تغيرات تصبغية متوسطة وتراجع في كثافة الكلوروفيل عبر سطح الورقة.")
            else:
                st.error("🚨 **مؤشر النسيج:** انخفاض حاد في نسبة النسيج السليم وجود جفاف أو تلف تصبغي واسع.")
                
            # عرض الصور بعد التصفية التامة للخلفية
            st.markdown(f"#### {t['heatmap_label']}")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(contoured_img, caption="Lesion Bounding (Leaf Surface Only)", use_container_width=True)
            with col_img2:
                st.image(heatmap_masked, caption="Segmented Thermal Heatmap", use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("⚠️ لم يتم التعرف على ورقة الشجر بشكل واضح، يرجى التقاط الصورة على خلفية تباين مناسبة.")

# --- 9. الفوتر السفلـي ---
st.markdown(f"""
    <div class="zino-footer">
        {t['dev_by']} | ZINO AgroVision Engine © 2026
    </div>
""", unsafe_allow_html=True)
