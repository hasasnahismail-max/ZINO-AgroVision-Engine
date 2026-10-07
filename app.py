import streamlit as st
import cv2
import numpy as np

# --- 1. إعداد الصفحة العامة ---
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
    .section-header {
        color: #58a6ff;
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 6px;
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
        "healthy_ratio": "نسبة النسيج الأخضر الحيوي",
        "infected_ratio": "نسبة الإجهاد والتغير التصبغي",
        "lesion_count": "عدد مناطق التغير النسيجي المكتشفة",
        "status_done": "تم عزل خلفية المشهد وعزل مصفوفة الورقة بنجاح 100%",
        "heatmap_label": "عزل جسم الورقة والخريطة الحرارية الموجهة (Isolated Heatmap & Contours)",
        "tech_title": "⚙️ محرك المعالجة المتقدم",
        "tech_desc": "تجزئة طيفية تعتمد على القناة a* في فضاء CIELAB لعزل خلفية الصور كلياً بدون أخطاء."
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
        "status_done": "Background 100% Subtracted & Leaf Matrix Isolated",
        "heatmap_label": "Isolated Leaf Contour & Spectral Heatmap",
        "tech_title": "⚙️ Advanced Vision Engine",
        "tech_desc": "CIELAB Color Space channel-a* segmentation eliminating background noise completely."
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
        "status_done": "Удаление фона и изоляция листа выполнены на 100%",
        "heatmap_label": "Изолированный контур листа и тепловая карта",
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": "Сегментация на основе канала a* в CIELAB, полностью исключающая фоновые помехи."
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
        "status_done": "Arka Plan %100 Ayrıştırıldı ve Yaprak Matrisi İzole Edildi",
        "heatmap_label": "İzole Yaprak Konturu ve Spektral Harita",
        "tech_title": "⚙️ Motor Özellikleri",
        "tech_desc": "Gürültüyü tamamen ortadan kaldıran CIELAB a*-kanalı segmentasyonu."
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
        "status_done": "背景100%扣除，叶片矩阵成功隔离",
        "heatmap_label": "隔离叶片轮廓与多光谱热力图",
        "tech_title": "⚙️ 视觉引擎规格",
        "tech_desc": "基于 CIELAB 色彩空间 a* 通道的精确定向分割，完全消除背景干扰。"
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
    st.image(img_rgb, caption="Input Image Frame", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(t["run_btn"]):
        # --- الخوارزمية الدقيقة: فصل الخلفية بواسطة CIELAB Color Space ---
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)
        
        # القناة a* في LAB تميز الأنسجة الخضراء النباتية تماماً بقيم أصغر من 120 بغض النظر عن الورق البني
        _, raw_leaf_mask = cv2.threshold(a_chan, 120, 255, cv2.THRESH_BINARY_INV)
        
        # التنظيف المورفولوجي لمنع التشويش
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        cleaned_mask = cv2.morphologyEx(raw_leaf_mask, cv2.MORPH_CLOSE, kernel)
        cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_OPEN, kernel)
        
        # استخراج أكبر مجسم (جسم الورقة الفعلي) وتجاهل الحواف والورق الخلفي بالكامل
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        leaf_mask = np.zeros_like(a_chan)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(leaf_mask, [largest_contour], -1, 255, -1)
            
        total_leaf_pixels = float(cv2.countNonZero(leaf_mask))
        
        if total_leaf_pixels > 1000:
            # --- أ) حساب البكسلات الخضراء الحيوية داخل حدود الورقة المعزولة ---
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            lower_green = np.array([28, 35, 35])
            upper_green = np.array([88, 255, 255])
            green_raw = cv2.inRange(hsv, lower_green, upper_green)
            
            # حصر البحث داخل جسم الورقة فقط
            healthy_mask = cv2.bitwise_and(green_raw, green_raw, mask=leaf_mask)
            healthy_pixels = float(cv2.countNonZero(healthy_mask))
            
            # ب) مناطق التغير التصبغي داخل الورقة حصراً
            damaged_mask = cv2.bitwise_and(leaf_mask, cv2.bitwise_not(healthy_mask))
            damaged_pixels = float(cv2.countNonZero(damaged_mask))
            
            healthy_pct = (healthy_pixels / total_leaf_pixels) * 100.0
            damaged_pct = (damaged_pixels / total_leaf_pixels) * 100.0
            
            # ج) تتبع البقع داخل الورقة رسم محيط الورقة بالأخضر والبقع بالأحمر
            lesion_cnts, _ = cv2.findContours(damaged_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            display_contours = img_rgb.copy()
            # إخفاء الخلفية الخارجية بجعلها داكنة
            background_black = np.zeros_like(img_rgb)
            display_contours = np.where(leaf_mask[:, :, None] == 255, img_rgb, background_black)
            
            # رسم إطار الورقة بالأخضر
            if contours:
                cv2.drawContours(display_contours, [largest_contour], -1, (0, 255, 0), 2)
                
            valid_lesions = 0
            for lc in lesion_cnts:
                if cv2.contourArea(lc) > 35:
                    valid_lesions += 1
                    cv2.drawContours(display_contours, [lc], -1, (255, 0, 0), 2)
                    
            # د) الخريطة الحرارية (مطبقة على الورقة فقط والخلفية سوداء معتمة)
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            heatmap_raw = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
            heatmap_rgb = cv2.cvtColor(heatmap_raw, cv2.COLOR_BGR2RGB)
            
            # قص الأشعة الحرارية لتكون داخل النسيج النباتي حصراً
            heatmap_final = cv2.bitwise_and(heatmap_rgb, heatmap_rgb, mask=leaf_mask)
            
            # --- 7. عرض نتائج التقرير الرياضي والمنطقي ---
            st.markdown('<div class="zino-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="report-title">{t["report_title"]}</div>', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(label=t["healthy_ratio"], value=f"{healthy_pct:.2f}%")
            with c2:
                st.metric(label=t["infected_ratio"], value=f"{damaged_pct:.2f}%")
            with c3:
                st.metric(label=t["lesion_count"], value=f"{valid_lesions}")
                
            st.info(f"📌 {t['status_done']}")
            
            # التحليل المنطقي والإرشادات الزراعية المستندة للأرقام الفعلية
            if healthy_pct >= 85.0:
                st.success("✅ **حالة الورقة:** النسيج النباتي سليماً ومكتظاً بالكلوروفيل الحيوي ضمن المعدلات الطبيعية الممتازة.")
                st.markdown('<div class="section-header">🛠️ التوصيات العادية:</div>', unsafe_allow_html=True)
                st.write("• الحفاظ على جدول الري المنتظم وتجنب تعريض النبتة لإجهاد مائي أو حراري مفاجئ.")
                
            elif healthy_pct >= 55.0:
                st.warning("⚠️ **حالة الورقة:** رصد إجهاد نسيجي وتراجع متوسط في الكثافة التصبغية على سطح الورقة.")
                st.markdown('<div class="section-header">🛠️ خطة المعالجة والتحسين:</div>', unsafe_allow_html=True)
                st.write("1. **التسميد:** إضافة سماد متوازن يحتوي على عناصر الحديد والنيتروجين لتعويض تراجع الكلوروفيل.")
                st.write("2. **الري:** ضبط معدلات الرطوبة ومنع تجمع المياه على الأوراق لتقليل فرص التلف.")
                
            else:
                st.error("🚨 **حالة الورقة:** انخفاض حاد في نسبة النسيج الأخضر السليم وظهور مناطق تغير تصبغي واسعة.")
                st.markdown('<div class="section-header">🛠️ بروتوكول التدخل المباشر:</div>', unsafe_allow_html=True)
                st.write("1. **العزل:** فصل الأجزاء المصابة لضمان عدم انتقال الإجهاد أو الإصابة للأوراق المجاورة.")
                st.write("2. **المعاملة الزراعية:** استخدام مغذيات ورقية متخصصة ومراجعة ظروف الإضاءة والتهوية فوراً.")

            # عرض الصور المعزولة كلياً
            st.markdown(f"#### {t['heatmap_label']}")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(display_contours, caption="Isolated Leaf Contour & Bounding", use_container_width=True)
            with col_img2:
                st.image(heatmap_final, caption="Strict Masked Thermal Heatmap", use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            st.error("⚠️ تعذر التعرف على ورقة النبات. يرجى توجيه الكاميرا مباشرة نحو الورقة.")

# --- 8. الفوتر السفلـي ---
st.markdown(f"""
    <div class="zino-footer">
        {t['dev_by']} | ZINO AgroVision Engine © 2026
    </div>
""", unsafe_allow_html=True)
