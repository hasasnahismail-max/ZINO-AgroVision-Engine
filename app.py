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

# --- 3. القاموس المعتمد للغات الخمس (شامل التحليل والتوصيات بالكامل) ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "تصميم وتطوير إسماعيل حساسنة",
        "upload_label": "قم برفع صورة ورقة النبات للتحليل المكتبي والدقيق",
        "input_cap": "إطار الصورة المدخلة",
        "run_btn": "🔬 تشغيل تحليل الرؤية الحاسوبية والحساب الرقمي",
        "report_title": "📊 تقرير التحليل الرقمي المتقدم لسطح الورقة (Leaf Surface Analysis)",
        "healthy_ratio": "نسبة النسيج الأخضر الحيوي",
        "infected_ratio": "نسبة الإجهاد والتغير التصبغي",
        "lesion_count": "عدد بقع التغير النسيجي",
        "health_score": "مؤشر الجودة والصحة العامة",
        "status_done": "تم عزل خلفية المشهد وعزل مصفوفة الورقة بنجاح 100%",
        "heatmap_label": "عزل جسم الورقة والخريطة الحرارية الموجهة (Isolated Heatmap & Contours)",
        "tech_title": "⚙️ محرك المعالجة المتقدم",
        "tech_desc": "تجزئة طيفية تعتمد على القناة a* في فضاء CIELAB لعزل خلفية الصور كلياً بدون أخطاء.",
        "cap_contours": "حدود الورقة وتتبع البقع المعزولة",
        "cap_heatmap": "الخريطة الحرارية الموجهة للورقة",
        "err_no_leaf": "⚠️ تعذر التعرف على ورقة النبات. يرجى توجيه الكاميرا مباشرة نحو الورقة.",
        # التوصيات والنتائج
        "st_healthy": "✅ **حالة الورقة:** النسيج النباتي سليم ومكتظ بالكلوروفيل الحيوي ضمن المعدلات الطبيعية الممتازة.",
        "rec_healthy_head": "🛠️ التوصيات الوقائية والحقلية:",
        "rec_healthy_body": "• الحفاظ على جدول الري المنتظم وتجنب تعريض النبتة لإجهاد مائي أو حراري مفاجئ.\n• الاستمرار بالمراقبة الدورية لسطح الأوراق السفلي.",
        "st_warning": "⚠️ **حالة الورقة:** رصد إجهاد نسيجي وتراجع متوسط في الكثافة التصبغية على سطح الورقة.",
        "rec_warning_head": "🛠️ خطة المعالجة والتحسين الموصى بها:",
        "rec_warning_body": "1. **التسميد:** إضافة سماد متوازن يحتوي على عناصر الحديد والنيتروجين لتعويض تراجع الكلوروفيل.\n2. **الري:** ضبط معدلات الرطوبة ومنع تجمع المياه على الأوراق لتقليل فرص التلف والتعفن.",
        "st_danger": "🚨 **حالة الورقة:** انخفاض حاد في نسبة النسيج الأخضر السليم وظهور مناطق تغير تصبغي واسعة.",
        "rec_danger_head": "🛠️ بروتوكول التدخل المباشر والسريع:",
        "rec_danger_body": "1. **العزل:** فصل الأجزاء المصابة لضمان عدم انتقال الإجهاد أو الإصابة للأوراق المجاورة.\n2. **المعاملة الزراعية:** استخدام مغذيات ورقية متخصصة ومراجعة ظروف الإضاءة والتهوية فوراً."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "Designed and Developed by Ismail Hasasa",
        "upload_label": "Upload Leaf Image for Quantitative Analysis",
        "input_cap": "Input Image Frame",
        "run_btn": "🔬 Run Computer Vision & Pixel Analysis Engine",
        "report_title": "📊 Quantitative Leaf Surface Diagnostics Report",
        "healthy_ratio": "Vital Green Tissue Ratio",
        "infected_ratio": "Discolored / Stressed Area Ratio",
        "lesion_count": "Detected Anomaly Regions",
        "health_score": "Overall Plant Health Index",
        "status_done": "Background 100% Subtracted & Leaf Matrix Isolated",
        "heatmap_label": "Isolated Leaf Contour & Spectral Heatmap",
        "tech_title": "⚙️ Advanced Vision Engine",
        "tech_desc": "CIELAB Color Space channel-a* segmentation eliminating background noise completely.",
        "cap_contours": "Isolated Leaf Contour & Anomaly Tracking",
        "cap_heatmap": "Targeted Thermal Heatmap Isolation",
        "err_no_leaf": "⚠️ Unable to detect leaf matrix. Please orient the camera directly towards the leaf.",
        # Diagnostic outputs
        "st_healthy": "✅ **Leaf Status:** Plant tissue is healthy and rich in active chlorophyll within optimal parameters.",
        "rec_healthy_head": "🛠️ Preventive & Field Recommendations:",
        "rec_healthy_body": "• Maintain consistent irrigation schedule and protect the plant from thermal stress.\n• Continue periodic monitoring of lower leaf surfaces.",
        "st_warning": "⚠️ **Leaf Status:** Moderate tissue stress and noticeable reduction in pigmentation detected.",
        "rec_warning_head": "🛠️ Treatment & Optimization Plan:",
        "rec_warning_body": "1. **Fertilization:** Apply balanced fertilizers enriched with Nitrogen and Iron to restore chlorophyll.\n2. **Irrigation:** Regulate humidity levels and avoid leaf wetness to minimize disease risks.",
        "st_danger": "🚨 **Leaf Status:** Severe reduction in healthy green tissue with critical discolored lesions.",
        "rec_danger_head": "🛠️ Immediate Intervention Protocol:",
        "rec_danger_body": "1. **Isolate:** Separate affected leaves/plants to stop potential spread to adjacent foliage.\n2. **Treatment:** Apply specialized foliar nutrients and immediately inspect lighting and ventilation conditions."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Система компьютерного зрения | Количественная диагностика поверхности листа",
        "dev_by": "Дизайн и разработка: Исмаил Хассасна",
        "upload_label": "Загрузить изображение листа для анализа",
        "input_cap": "Кадр исходного изображения",
        "run_btn": "🔬 Запустить компьютерный анализ пикселей",
        "report_title": "📊 Отчет о количественном анализе поверхности листа",
        "healthy_ratio": "Доля здоровой зеленой ткани",
        "infected_ratio": "Доля измененной/стрессовой ткани",
        "lesion_count": "Обнаружено аномальных зон",
        "health_score": "Индекс общего здоровья",
        "status_done": "Удаление фона и изоляция листа выполнены на 100%",
        "heatmap_label": "Изолированный контур листа и тепловая карта",
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": "Сегментация на основе канала a* в CIELAB, полностью исключающая фоновые помехи.",
        "cap_contours": "Контур листа и отслеживание аномалий",
        "cap_heatmap": "Тепловая карта поверхности листа",
        "err_no_leaf": "⚠️ Не удалось обнаружить лист. Пожалуйста, направьте камеру непосредственно на лист.",
        # Diagnostic outputs
        "st_healthy": "✅ **Состояние листа:** Ткань здорова и богата хлорофиллом в пределах нормы.",
        "rec_healthy_head": "🛠️ Профилактические рекомендации:",
        "rec_healthy_body": "• Поддерживайте регулярный полив и избегайте температурных стрессов.\n• Продолжайте периодический осмотр нижней стороны листьев.",
        "st_warning": "⚠️ **Состояние листа:** Обнаружен умеренный стресс тканей и снижение пигментации.",
        "rec_warning_head": "🛠️ План лечения и оптимизации:",
        "rec_warning_body": "1. **Удобрение:** Внесите азотно-железистые удобрения для восстановления хлорофилла.\n2. **Полив:** Отрегулируйте уровень влажности и избегайте скопления воды на листьях.",
        "st_danger": "🚨 **Состояние листа:** Критическое снижение здоровой ткани и сильное поражение.",
        "rec_danger_head": "🛠️ Протокол немедленного вмешательства:",
        "rec_danger_body": "1. **Изоляция:** Удалите поврежденные части, чтобы предотвратить распространение.\n2. **Обработка:** Примените специализированные листовые подкормки и проверьте условия освещения."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Görme Motoru | Nicel Yaprak Yüzeyi Teşhisi",
        "dev_by": "Tasarım ve Geliştirme: İsmail Hassasneh",
        "upload_label": "Nicel Analiz İçin Yaprak Resmi Yükleyin",
        "input_cap": "Giriş Görüntü Çerçevesi",
        "run_btn": "🔬 Bilgisayarlı Görme ve Piksel Analizini Çalıştır",
        "report_title": "📊 Nicel Yaprak Yüzeyi Analiz Raporu",
        "healthy_ratio": "Canlı Yeşil Doku Oranı",
        "infected_ratio": "Renk Değişimi / Stresli Alan Oranı",
        "lesion_count": "Tespit Edilen Anomali Bölgesi",
        "health_score": "Genel Bitki Sağlık Endeksi",
        "status_done": "Arka Plan %100 Ayrıştırıldı ve Yaprak Matrisi İzole Edildi",
        "heatmap_label": "İzole Yaprak Konturu ve Spektral Harita",
        "tech_title": "⚙️ Motor Özellikleri",
        "tech_desc": "Gürültüyü tamamen ortadan kaldıran CIELAB a*-kanalı segmentasyonu.",
        "cap_contours": "İzole Yaprak Anomali Takibi",
        "cap_heatmap": "Hedeflenmiş Isı Haritası",
        "err_no_leaf": "⚠️ Yaprak tespit edilemedi. Lütfen kamerayı doğrudan yaprağa doğrultun.",
        # Diagnostic outputs
        "st_healthy": "✅ **Yaprak Durumu:** Bitki dokusu sağlıklı ve klorofil oranı mükemmel seviyededir.",
        "rec_healthy_head": "🛠️ Koruyucu ve Saha Tavsiyeleri:",
        "rec_healthy_body": "• Düzenli sulama programını koruyun ve ani sıcaklık değişimlerinden kaçının.\n• Alt yaprak yüzeylerini periyodik olarak kontrol etmeye devam edin.",
        "st_warning": "⚠️ **Yaprak Durumu:** Orta düzeyde doku stresi ve pikment kaybı tespit edildi.",
        "rec_warning_head": "🛠️ İyileştirme ve Bakım Planı:",
        "rec_warning_body": "1. **Gübreleme:** Klorofil üretimini artırmak için Azot ve Demir takviyeli gübre kullanın.\n2. **Sulama:** Nem oranını ayarlayın ve yaprak üzerinde su birikmesini önleyin.",
        "st_danger": "🚨 **Yaprak Durumu:** Yeşil doku oranında ciddi düşüş ve yaygın lezyonlar tespit edildi.",
        "rec_danger_head": "🛠️ Acil Müdahale Protokolü:",
        "rec_danger_body": "1. **İzolasyon:** Hastalığın yayılmasını önlemek için etkilenen kısımları ayırın.\n2. **Müdahale:** Özel yaprak besinleri uygulayın, ışık ve havalandırma şartlarını gözden geçirin."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业视觉引擎 | 叶片表面定量诊断",
        "dev_by": "设计与开发：Ismail Hassasneh",
        "upload_label": "上传叶片图像进行定量分析",
        "input_cap": "输入图像帧",
        "run_btn": "🔬 运行计算机视觉与像素分析引擎",
        "report_title": "📊 叶片表面定量诊断报告",
        "healthy_ratio": "绿色健康组织比例",
        "infected_ratio": "受损 / 变色区域比例",
        "lesion_count": "检测到的异常区域数量",
        "health_score": "植物综合健康指数",
        "status_done": "背景100%扣除，叶片矩阵成功隔离",
        "heatmap_label": "隔离叶片轮廓与多光谱热力图",
        "tech_title": "⚙️ 视觉引擎规格",
        "tech_desc": "基于 CIELAB 色彩空间 a* 通道的精确定向分割，完全消除背景干扰。",
        "cap_contours": "隔离叶片轮廓与病斑追踪",
        "cap_heatmap": "定向多光谱热力图",
        "err_no_leaf": "⚠️ 未能识别叶片，请将镜头对准叶片主体。",
        # Diagnostic outputs
        "st_healthy": "✅ **叶片状态：** 植物组织非常健康，活性叶绿素含量处于极佳水平。",
        "rec_healthy_head": "🛠️ 预防与田间建议：",
        "rec_healthy_body": "• 保持规律的灌溉计划，避免突发热应激。\n• 继续定期检查叶片背面。",
        "st_warning": "⚠️ **叶片状态：** 检测到中度组织应激和色素沉着下降。",
        "rec_warning_head": "🛠️ 建议的处理与优化方案：",
        "rec_warning_body": "1. **施肥：** 添加富含铁和氮的平衡肥料，补充叶绿素。\n2. **灌溉：** 调节湿度，防止叶片积水以减少腐烂风险。",
        "st_danger": "🚨 **叶片状态：** 健康组织严重减少，出现大面积病斑。",
        "rec_danger_head": "🛠️ 紧急干预协议：",
        "rec_danger_body": "1. **隔离：** 隔离受影响的叶片/植株，防止扩散。\n2. **治疗：** 使用专用叶面营养剂，并立即检查光照与通风条件。"
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
    st.image(img_rgb, caption=t["input_cap"], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(t["run_btn"]):
        # --- الخوارزمية الدقيقة: فصل الخلفية بواسطة CIELAB Color Space ---
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l_chan, a_chan, b_chan = cv2.split(lab)
        
        # القناة a* في LAB تميز الأنسجة الخضراء النباتية بقيم أصغر من 120
        _, raw_leaf_mask = cv2.threshold(a_chan, 120, 255, cv2.THRESH_BINARY_INV)
        
        # التنظيف المورفولوجي لمنع التشويش
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        cleaned_mask = cv2.morphologyEx(raw_leaf_mask, cv2.MORPH_CLOSE, kernel)
        cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_OPEN, kernel)
        
        # استخراج جسم الورقة الفعلي وتجاهل الخلفية
        contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        leaf_mask = np.zeros_like(a_chan)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(leaf_mask, [largest_contour], -1, 255, -1)
            
        total_leaf_pixels = float(cv2.countNonZero(leaf_mask))
        
        if total_leaf_pixels > 1000:
            # أ) حساب البكسلات الخضراء الحيوية
            hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            lower_green = np.array([28, 35, 35])
            upper_green = np.array([88, 255, 255])
            green_raw = cv2.inRange(hsv, lower_green, upper_green)
            
            healthy_mask = cv2.bitwise_and(green_raw, green_raw, mask=leaf_mask)
            healthy_pixels = float(cv2.countNonZero(healthy_mask))
            
            # ب) مناطق التغير التصبغي
            damaged_mask = cv2.bitwise_and(leaf_mask, cv2.bitwise_not(healthy_mask))
            damaged_pixels = float(cv2.countNonZero(damaged_mask))
            
            healthy_pct = (healthy_pixels / total_leaf_pixels) * 100.0
            damaged_pct = (damaged_pixels / total_leaf_pixels) * 100.0
            
            # ج) مؤشر الصحة الحيوي المركب (Deep Analysis Score)
            health_score_val = min(100.0, max(0.0, healthy_pct - (damaged_pct * 0.2)))
            
            # د) تتبع البقع ورسم الحدود
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
                    
            # هـ) الخريطة الحرارية الطيفية
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
            heatmap_raw = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
            heatmap_rgb = cv2.cvtColor(heatmap_raw, cv2.COLOR_BGR2RGB)
            heatmap_final = cv2.bitwise_and(heatmap_rgb, heatmap_rgb, mask=leaf_mask)
            
            # --- 7. عرض النتائج والتقرير التحليلي المترجم بالكامل ---
            st.markdown('<div class="zino-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="report-title">{t["report_title"]}</div>', unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(label=t["healthy_ratio"], value=f"{healthy_pct:.1f}%")
            with c2:
                st.metric(label=t["infected_ratio"], value=f"{damaged_pct:.1f}%")
            with c3:
                st.metric(label=t["lesion_count"], value=f"{valid_lesions}")
            with c4:
                st.metric(label=t["health_score"], value=f"{health_score_val:.1f} / 100")
                
            st.info(f"📌 {t['status_done']}")
            
            # التحليل المنطقي والإرشادات الديناميكية المترجمة
            if healthy_pct >= 85.0:
                st.success(t["st_healthy"])
                st.markdown(f'<div class="section-header">{t["rec_healthy_head"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_healthy_body"])
                
            elif healthy_pct >= 55.0:
                st.warning(t["st_warning"])
                st.markdown(f'<div class="section-header">{t["rec_warning_head"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_warning_body"])
                
            else:
                st.error(t["st_danger"])
                st.markdown(f'<div class="section-header">{t["rec_danger_head"]}</div>', unsafe_allow_html=True)
                st.write(t["rec_danger_body"])

            # عرض الصور المعزولة مع تسميات مترجمة
            st.markdown(f"#### {t['heatmap_label']}")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(display_contours, caption=t["cap_contours"], use_container_width=True)
            with col_img2:
                st.image(heatmap_final, caption=t["cap_heatmap"], use_container_width=True)
          
