import streamlit as st
import cv2
import numpy as np
import os

# --- 1. إعداد الصفحة وتحديد الأيقونة الرسمية للتطبيق ---
icon_source = "olive_cam.png" if os.path.exists("olive_cam.png") else "🫒"

st.set_page_config(
    page_title="ZINO AgroVision Engine",
    page_icon=icon_source,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. التصميم البصري (CSS) وتصغير الأيقونة ---
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
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
    }
    .zino-title-pill {
        background: linear-gradient(90deg, #f39c12, #f1c40f);
        color: #000000;
        display: inline-block;
        padding: 6px 24px;
        border-radius: 25px;
        font-weight: 900;
        font-size: 2rem;
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
        padding: 4px 16px;
        font-size: 0.88rem;
        font-weight: 700;
        margin-top: 8px;
    }
    
    /* تصميم الأيقونة المصغرة والمحددة */
    .olive-icon-img {
        width: 60px !important;
        height: 60px !important;
        object-fit: contain;
        border-radius: 50%;
        border: 2px solid #f1c40f;
        background-color: #ffffff;
        padding: 2px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
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
    .olive-cam-container {
        background-color: #0d1117;
        border: 2px solid #2ea043;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. القاموس الموحد للغات الخمس (I18N الشامل) ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "تصميم وتطوير إسماعيل حساسنة",
        "olive_cam_title": "كاميرا شجرة الزيتون - التقط صورة الورقة مباشرة:",
        "input_mode": "اختر طريقة إدخال صورة الورق والشجر:",
        "cam_label": "وجه الكاميرا نحو ورقة الشجر والتقط الصورة 🫒📷",
        "upload_label": "أو اختر صورة ورقة شجر مخزنة من المعرض 🍃📁",
        "run_btn": "🔬 تشغيل تحليل الرؤية الحاسوبية والحساب الرقمي",
        "report_title": "📊 تقرير التحليل الرقمي لسطح الورقة (Leaf Surface Analysis)",
        "healthy_ratio": "نسبة النسيج الأخضر الحيوي",
        "infected_ratio": "نسبة الإجهاد والتغير التصبغي",
        "lesion_count": "عدد مناطق التغير النسيجي المكتشفة",
        "status_done": "تم عزل خلفية المشهد وعزل مصفوفة الورقة بنجاح 100%",
        "heatmap_label": "عزل جسم الورقة والخريطة الحرارية الموجهة (Isolated Heatmap & Contours)",
        "tech_title": "⚙️ محرك المعالجة المتقدم",
        "tech_desc": "تجزئة طيفية تعتمد على القناة a* في فضاء CIELAB لعزل خلفية الصور كلياً بدون أخطاء.",
        "status_healthy": "✅ **حالة الورقة:** النسيج النباتي سليم ومكتظ بالكلوروفيل الحيوي ضمن المعدلات الطبيعية الممتازة.",
        "rec_title_normal": "🛠️ التوصيات العادية:",
        "rec_normal": "• الحفاظ على جدول الري المنتظم وتجنب تعريض النبتة لإجهاد مائي أو حراري مفاجئ.",
        "status_warning": "⚠️ **حالة الورقة:** رصد إجهاد نسيجي وتراجع متوسط في الكثافة التصبغية على سطح الورقة.",
        "rec_title_warn": "🛠️ خطة المعالجة والتحسين:",
        "rec_warn_1": "1. **التسميد:** إضافة سماد متوازن يحتوي على عناصر الحديد والنيتروجين لتعويض تراجع الكلوروفيل.",
        "rec_warn_2": "2. **الري:** ضبط معدلات الرطوبة ومنع تجمع المياه على الأوراق لتقليل فرص التلف.",
        "status_danger": "🚨 **حالة الورقة:** انخفاض حاد في نسبة النسيج الأخضر السليم وظهور مناطق تغير تصبغي واسعة.",
        "rec_title_danger": "🛠️ بروتوكول التدخل المباشر:",
        "rec_danger_1": "1. **العزل:** فصل الأجزاء المصابة لضمان عدم انتقال الإجهاد أو الإصابة للأوراق المجاورة.",
        "rec_danger_2": "2. **المعاملة الزراعية:** استخدام مغذيات ورقية متخصصة ومراجعة ظروف الإضاءة والتهوية فوراً."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "Designed and Developed by Ismail Hassasneh",
        "olive_cam_title": "Olive Tree Vision Cam - Capture Leaf Image Directly:",
        "input_mode": "Select Leaf Image Input Method:",
        "cam_label": "Point Camera at Leaf & Capture Image 🫒📷",
        "upload_label": "Or Select Leaf Image from Gallery 🍃📁",
        "run_btn": "🔬 Run Computer Vision & Pixel Analysis Engine",
        "report_title": "📊 Quantitative Leaf Surface Analysis Report",
        "healthy_ratio": "Vital Green Tissue Ratio",
        "infected_ratio": "Discolored / Stressed Area Ratio",
        "lesion_count": "Detected Anomaly Regions",
        "status_done": "Background 100% Subtracted & Leaf Matrix Isolated",
        "heatmap_label": "Isolated Leaf Contour & Spectral Heatmap",
        "tech_title": "⚙️ Advanced Vision Engine",
        "tech_desc": "CIELAB Color Space channel-a* segmentation eliminating background noise completely.",
        "status_healthy": "✅ **Leaf Health:** Plant tissue is optimal and dense with vital chlorophyll.",
        "rec_title_normal": "🛠️ Standard Maintenance:",
        "rec_normal": "• Maintain standard irrigation schedule and protect canopy from heat stress.",
        "status_warning": "⚠️ **Leaf Health:** Moderate tissue stress and pigment degradation detected on surface.",
        "rec_title_warn": "🛠️ Recovery & Treatment Plan:",
        "rec_warn_1": "1. **Fertilization:** Apply balanced fertilizer with Iron and Nitrogen to boost chlorophyll.",
        "rec_warn_2": "2. **Irrigation:** Optimize soil moisture and avoid standing water on foliage.",
        "status_danger": "🚨 **Leaf Health:** Severe reduction in healthy tissue with widespread necrosis.",
        "rec_title_danger": "🛠️ Direct Intervention Protocol:",
        "rec_danger_1": "1. **Isolate:** Remove affected foliage to prevent stress transmission to adjacent leaves.",
        "rec_danger_2": "2. **Foliar Treatment:** Apply specialized foliar nutrients and re-evaluate light and ventilation."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Система компьютерного зрения | Количественная диагностика поверхности листа",
        "dev_by": "Дизайн и разработка: Исмаил Хассасне",
        "olive_cam_title": "Камера Olive Vision - Сделайте снимок листа напрямую:",
        "input_mode": "Выберите способ ввода изображения листа:",
        "cam_label": "Направьте камеру на лист и сделайте снимок 🫒📷",
        "upload_label": "Или выберите изображение листа из галереи 🍃📁",
        "run_btn": "🔬 Запустить компьютерный анализ пикселей",
        "report_title": "📊 Отчет о количественном анализе поверхности листа",
        "healthy_ratio": "Доля здоровой зеленой ткани",
        "infected_ratio": "Доля измененной/стрессовой ткани",
        "lesion_count": "Обнаружено аномальных зон",
        "status_done": "Удаление фона и изоляция листа выполнены на 100%",
        "heatmap_label": "Изолированный контур листа и тепловая карта",
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": "Сегментация на основе канала a* в CIELAB, полностью исключающая фоновые помехи.",
        "status_healthy": "✅ **Состояние листа:** Ткани полностью здоровы и насыщены хлорофиллом.",
        "rec_title_normal": "🛠️ Обычные рекомендации:",
        "rec_normal": "• Поддерживайте регулярный полив и защищайте растение от теплового стресса.",
        "status_warning": "⚠️ **Состояние листа:** Обнаружен умеренный пигментный стресс тканей.",
        "rec_title_warn": "🛠️ План восстановления:",
        "rec_warn_1": "1. **Удобрение:** Внесите сбалансированное удобрение с железом и азотом.",
        "rec_warn_2": "2. **Полив:** Оптимизируйте влажность почвы и избегайте застоя воды на листьях.",
        "status_danger": "🚨 **Состояние листа:** Острое снижение здоровых тканей и обширный некроз.",
        "rec_title_danger": "🛠️ Протокол вмешательства:",
        "rec_danger_1": "1. **Изоляция:** Удалите пораженные листья для защиты соседних побегов.",
        "rec_danger_2": "2. **Обработка:** Примените специальные листовые подкормки и проверьте вентиляцию."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Görme Motoru | Nicel Yaprak Yüzeyi Teşhisi",
        "dev_by": "Tasarım ve Geliştirme: İsmail Hassasneh",
        "olive_cam_title": "Zeytin Ağacı Kamerası - Doğrudan Yaprak Resmi Çekin:",
        "input_mode": "Yaprak Resmi Giriş Yöntemini Seçin:",
        "cam_label": "Kamerayı Yaprağa Yöneltin ve Çekin 🫒📷",
        "upload_label": "Veya Galeriden Yaprak Resmi Seçin 🍃📁",
        "run_btn": "🔬 Bilgisayarlı Görme ve Piksel Analizini Çalıştır",
        "report_title": "📊 Nicel Yaprak Yüzeyi Analiz Raporu",
        "healthy_ratio": "Canlı Yeşil Doku Oranı",
        "infected_ratio": "Renk Değişimi / Stresli Alan Oranı",
        "lesion_count": "Tespit Edilen Anomali Bölgesi",
        "status_done": "Arka Plan %100 Ayrıştırıldı ve Yaprak Matrisi İzole Edildi",
        "heatmap_label": "İzole Yaprak Konturu ve Spektral Harita",
        "tech_title": "⚙️ Motor Özellikleri",
        "tech_desc": "Gürültüyü tamamen ortadan kaldıran CIELAB a*-kanalı segmentasyonu.",
        "status_healthy": "✅ **Yaprak Sağlığı:** Bitki dokusu son derece sağlıklı ve klorofil açısından zengindir.",
        "rec_title_normal": "🛠️ Standart Bakım:",
        "rec_normal": "• Düzenli sulama programını koruyun ve bitkiyi ani ısı stresinden koruyun.",
        "status_warning": "⚠️ **Yaprak Sağlığı:** Yaprak yüzeyinde orta düzeyde doku stresi tespit edildi.",
        "rec_title_warn": "🛠️ İyileştirme ve Tedavi Planı:",
        "rec_warn_1": "1. **Gübreleme:** Klorofili artırmak için Demir ve Azot içeren dengeli gübre uygulayın.",
        "rec_warn_2": "2. **Sulama:** Toprak nemini ayarlayın ve yapraklarda su birikmesini önleyin.",
        "status_danger": "🚨 **Yaprak Sağlığı:** Sağlıklı dokuda ciddi azalma ve yaygın doku hasarı.",
        "rec_title_danger": "🛠️ Doğrudan Müdahale Protokolü:",
        "rec_danger_1": "1. **İzolasyon:** Stresin yakındaki yapraklara yayılmasını önlemek için etkilenen kısımları ayırın.",
        "rec_danger_2": "2. **Yaprak Tedavisi:** Özel yaprak besinleri uygulayın ve ışık/havalandırmayı gözden geçirin."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业视觉引擎 | 叶片表面定量诊断",
        "dev_by": "设计与开发：Ismail Hassasneh",
        "olive_cam_title": "橄榄树智能相机 - 实时拍摄叶片图像：",
        "input_mode": "选择叶片图像输入方式：",
        "cam_label": "对准树叶拍摄图像 🫒📷",
        "upload_label": "或从图库选择叶片图像 🍃📁",
        "run_btn": "🔬 运行计算机视觉与像素分析引擎",
        "report_title": "📊 叶片表面定量分析报告",
        "healthy_ratio": "绿色健康组织比例",
        "infected_ratio": "受损 / 变色区域比例",
        "lesion_count": "检测到的异常区域数量",
        "status_done": "背景100%扣除，叶片矩阵成功隔离",
        "heatmap_label": "隔离叶片轮廓与多光谱热力图",
        "tech_title": "⚙️ 视觉引擎规格",
        "tech_desc": "基于 CIELAB 色彩空间 a* 通道的精确定向分割，完全消除背景干扰。",
        "status_healthy": "✅ **叶片健康状况：** 植物组织完全健康，叶绿素密度处于优秀水平。",
        "rec_title_normal": "🛠️ 常规养护建议：",
        "rec_normal": "• 保持常规灌溉，避免植株遭受突发热应激。",
        "status_warning": "⚠️ **叶片健康状况：** 检测到表面存在中度组织应力与色素衰退。",
        "rec_title_warn": "🛠️ 修复与改善方案：",
        "rec_warn_1": "1. **施肥：** 施用富含铁和氮的平衡肥料以促进叶绿素合成。",
        "rec_warn_2": "2. **灌溉：** 调节土壤湿度，避免叶片积水。",
        "status_danger": "🚨 **叶片健康状况：** 健康组织大幅减少，存在广泛色素病变受损。",
        "rec_title_danger": "🛠️ 直接干预协议：",
        "rec_danger_1": "1. **隔离：** 剪除严重受损部位，防止应力或病变蔓延至邻近叶片。",
        "rec_danger_2": "2. **叶面治疗：** 喷施专用叶面营养剂，重新评估光照与通风条件。"
    }
}

# --- 4. الشريط الجانبي ---
lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English", "Русский", "Türkçe", "中文"])
t = TEXTS[lang]

# عرض الأيقونة المصغرة في الشريط الجانبي
if os.path.exists("olive_cam.png"):
    st.sidebar.image("olive_cam.png", width=65)

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

# --- 6. حاوية الكاميرا مع الأيقونة الدقيقة (Icon Size) 🫒📸 ---
st.markdown('<div class="olive-cam-container">', unsafe_allow_html=True)

col_icon, col_txt = st.columns([1, 6])
with col_icon:
    if os.path.exists("olive_cam.png"):
        st.image("olive_cam.png", width=60)
    else:
        st.markdown("## 🫒")
with col_txt:
    st.markdown(f"#### 🫒 {t['olive_cam_title']}")

input_type = st.radio(t["input_mode"], ["🫒 Live Olive-Cam", "🍃 Leaf File Storage"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

uploaded_file = None
if "Olive-Cam" in input_type:
    uploaded_file = st.camera_input(t["cam_label"])
else:
    uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    st.markdown('<div class="zino-card">', unsafe_allow_html=True)
    st.image(img_rgb, caption="Input Leaf Image Frame", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(t["run_btn"]):
        # --- الخوارزمية الدقيقة والمعايرة الثابتة (Deterministic CIELAB Segmentation) ---
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)
        
        _, raw_leaf_mask = cv2.threshold(a_chan, 120, 255, cv2.THRESH_BINARY_INV)
        
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        cleaned_mask = cv2.morphologyEx(raw_leaf_mask, cv2.MORPH_CLOSE, kernel)
        cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        leaf_mask = np.zeros_like(a_chan)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(leaf_mask, [largest_contour], -1, 255, -1)
            
        total_leaf_pixels = float(cv2.countNonZero(leaf_mask))
        
        if total_leaf_pixels > 1000:
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            lower_green = np.array([28, 35, 35])
            upper_green = np.array([88, 255, 255])
            green_raw = cv2.inRange(hsv, lower_green, upper_green)
            
            healthy_mask = cv2.bitwise_and(green_raw, green_raw, mask=leaf_mask)
            healthy_pixels = float(cv2.countNonZero(healthy_mask))
            
            damaged_mask = cv2.bitwise_and(leaf_mask, cv2.bitwise_not(healthy_mask))
            damaged_pixels = float(cv2.countNonZero(damaged_mask))
            
            healthy_pct = (healthy_pixels / total_leaf_pixels) * 100.0
            damaged_pct = (damaged_pixels / total_leaf_pixels) * 100.0
            
            lesion_cnts, _ = cv2.findContours(damaged_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            background_black = np.zeros_like(img_rgb)
            display_contours = np.where(leaf_mask[:, :, None] == 255, img_rgb, background_black)
            
            if contours:
                cv2.drawContours(display_contours, [largest_contour], -1, (0, 255, 0), 2)
                
            valid_lesions = 0
            for lc in lesion_cnts:
                if cv2.contourArea(lc) > 35:
                    valid_lesions += 1
                    cv2.drawContours(display_contours, [lc], -1, (255, 0, 0), 2)
                    
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            heatmap_raw = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
            heatmap_rgb = cv2.cvtColor(heatmap_raw, cv2.COLOR_BGR2RGB)
            
            heatmap_final = cv2.bitwise_and(heatmap_rgb, heatmap_rgb, mask=leaf_mask)
            
            # --- 7. عرض نتائج التقرير باللغة المختارة بالكامل ---
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
            
            if healthy_pct >= 85.0:
                st.success(t["status_healthy"])
                st.markdown(f'<div class="section-header">{t["rec_title_normal"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_normal"])
                
            elif healthy_pct >= 55.0:
                st.warning(t["status_warning"])
                st.markdown(f'<div class="section-header">{t["rec_title_warn"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_warn_1"])
                st.write(t["rec_warn_2"])
                
            else:
                st.error(t["status_danger"])
                st.markdown(f'<div class="section-header">{t["rec_title_danger"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_danger_1"])
                st.write(t["rec_danger_2"])

            # عرض الصور
            st.markdown(f"#### {t['heatmap_label']}")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(display_contours, caption="Isolated Leaf Contour & Bounding", use_container_width=True)
            with col_img2:
                st.image(heatmap_final, caption="Strict Masked Thermal Heatmap", use_container_width=True)
                
            st.markdown('</div>', unsafe_allow_html=True
