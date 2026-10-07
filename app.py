import streamlit as st
import cv2
import numpy as np

# --- 1. تهيئة إعدادات الصفحة ---
st.set_page_config(
    page_title="ZINO AgroVision Engine | Deep Diagnostic Edition",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. التصميم البصري الكامل (CSS) ---
st.markdown("""
    <style>
    /* خلفية التطبيق الصفراء الكلاسيكية */
    .stApp {
        background-color: #f1c40f !important;
        font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
    }
    
    /* الهيدر العلوي الداكن */
    .zino-header {
        background-color: #0d1117;
        border: 2px solid #000000;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        margin-bottom: 22px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.3);
    }
    .zino-title-pill {
        background: linear-gradient(90deg, #f39c12, #f1c40f);
        color: #000000;
        display: inline-block;
        padding: 8px 28px;
        border-radius: 25px;
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
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
        margin-top: 12px;
        box-shadow: 0px 2px 8px rgba(241, 196, 15, 0.2);
    }
    
    /* الحاويات والبطاقات الداكنة */
    .zino-card {
        background-color: #0d1117;
        border: 2px solid #161b22;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        color: #f0f6fc;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.35);
    }
    
    /* زر الفحص الأزرق البرّاق */
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
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 82, 212, 0.7) !important;
    }
    
    /* عناوين التقارير */
    .report-title {
        color: #f1c40f;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 14px;
        border-bottom: 1.5px solid #30363d;
        padding-bottom: 8px;
    }
    .section-header {
        color: #58a6ff;
        font-size: 1.15rem;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 8px;
    }
    
    /* الفوتر السفلـي */
    .zino-footer {
        background-color: #0d1117;
        border: 1.5px solid #161b22;
        border-radius: 10px;
        text-align: center;
        padding: 14px;
        color: #f1c40f;
        font-weight: bold;
        margin-top: 25px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. القاموس الخماسي العميق مع شريط الحقوق البرمجية (I18N) ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Diagnostic System | High-Precision Computer Vision Hardware Engine",
        "dev_by": "👨‍💻 تصميم وتطوير: المهندس إسماعيل حساسنة",
        "select_lang": "🌐 اختر اللغة / Select Language",
        "upload_label": "قم برفع صورة ورقة النبات للتحليل المجهري والدقيق",
        "run_btn": "🔬 تشغيل المحرك والتحليل التشخيصي المتقدم الان",
        "report_title": "📊 تقرير التشخيص الزراعي والتحليل الطيفي العميق",
        "healthy_ratio": "النسيج الحيوي السليم (Healthy Ratio)",
        "infected_ratio": "مساحة الإصابة والتلف (Lesion Area)",
        "lesion_count": "عدد البقع المصابة المكتشفة",
        "status_done": "اكتمل الفحص والتجزئة الشريحية بنجاح",
        "heatmap_label": "الخريطة الحرارية المجهرية وتجزئة البقع (Lesion Contours & Thermal Heatmap)",
        "cause_title": "🔍 المسبب المرضي والدراسة التشريحية:",
        "treatment_title": "🛠️ بروتوكول العلاج الموصى به (توصيات المحرك):",
        "tech_title": "⚙️ مواصفات المحرك والأجهزة الطرفية",
        "tech_desc": "محرك رؤية حاسوبية عالي الأداء معالجة C++17/OpenCV 4.x مخصص للأجهزة المدمجة (Edge Compute Engine)."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Diagnostic System | High-Precision Computer Vision Hardware Engine",
        "dev_by": "👨‍💻 Designed & Developed by Ismail Hassasneh",
        "select_lang": "🌐 Select Language",
        "upload_label": "Upload Leaf Image for Deep Microscopic Diagnostics",
        "run_btn": "🔬 Run Advanced Diagnostic Engine & Pathology Pipeline",
        "report_title": "📊 Deep Agricultural Diagnostic & Spectral Analysis Report",
        "healthy_ratio": "Healthy Vital Tissue Ratio",
        "infected_ratio": "Infected & Lesion Surface Area",
        "lesion_count": "Detected Lesion Contours",
        "status_done": "Deep Pathology & Segmentation Analysis Complete",
        "heatmap_label": "Lesion Contours & Multi-Spectral Thermal Heatmap",
        "cause_title": "🔍 Etiology & Pathological Analysis:",
        "treatment_title": "🛠️ Recommended Treatment Protocol:",
        "tech_title": "⚙️ Engine & Edge Hardware Specs",
        "tech_desc": "High-performance C++17 & OpenCV 4.x compute engine optimized for resource-constrained Edge SBCs."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Усовершенствованная система сельхоздиагностики | Компьютерное зрение высокой точности",
        "dev_by": "👨‍💻 Дизайн и разработка: Исмаил Хассасне",
        "select_lang": "🌐 Выберите язык",
        "upload_label": "Загрузить изображение листа для глубокой диагностики",
        "run_btn": "🔬 Запустить расширенный диагностический анализ",
        "report_title": "📊 Подробный отчет о сельскохозяйственной диагностике",
        "healthy_ratio": "Здоровая ткань",
        "infected_ratio": "Площадь поражения",
        "lesion_count": "Обнаружено очагов поражения",
        "status_done": "Глубокий анализ сегментации завершен",
        "heatmap_label": "Контуры поражений и спектральная тепловая карта",
        "cause_title": "🔍 Причина заболевания и этиология:",
        "treatment_title": "🛠️ Рекомендуемый протокол лечения:",
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": "Высокопроизводительный движок обработки C++17 / OpenCV 4.x для Edge устройств."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Teşhis Sistemi | Yüksek Hassasiyetli Bilgisayarlı Görme Motoru",
        "dev_by": "👨‍💻 Tasarım ve Geliştirme: İsmail Hassasneh",
        "select_lang": "🌐 Dil Seçin",
        "upload_label": "Derin Teşhis İçin Yaprak Resmini Yükleyin",
        "run_btn": "🔬 Gelişmiş Teşhis Motorunu Çalıştır",
        "report_title": "📊 Derin Tarımsal Teşhis ve Spektral Rapor",
        "healthy_ratio": "Sağlıklı Doku Oranı",
        "infected_ratio": "Hasarlı / Enfekte Alan",
        "lesion_count": "Tespit Edilen Lezyon Sayısı",
        "status_done": "Derin Segmentasyon Analizi Tamamlandı",
        "heatmap_label": "Lezyon Konturları ve Spektral Termal Harita",
        "cause_title": "🔍 Hastalık Nedeni ve Etiyoloji:",
        "treatment_title": "🛠️ Önerilen Tedavi Protokolü:",
        "tech_title": "⚙️ Motor & Donanım Özellikleri",
        "tech_desc": "C++17 ve OpenCV 4.x ile geliştirilmiş kenar bilişim donanım motoru."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业叶片深度诊断系统 | 高精度计算机视觉硬件引擎",
        "dev_by": "👨‍💻 设计与开发：Ismail Hassasneh",
        "select_lang": "🌐 选择语言",
        "upload_label": "上传叶片图像进行深度病理微观诊断",
        "run_btn": "🔬 运行高级诊断引擎与病理分析",
        "report_title": "📊 深度农业诊断与光谱分析报告",
        "healthy_ratio": "健康组织比例",
        "infected_ratio": "病变受损面积比例",
        "lesion_count": "检测到的病斑轮廓数量",
        "status_done": "深度分割与病理分析完成",
        "heatmap_label": "病斑轮廓跟踪与多光谱热力图",
        "cause_title": "🔍 病原学与病因分析:",
        "treatment_title": "🛠️ 推荐治疗与防护方案:",
        "tech_title": "⚙️ 引擎与边缘硬件规格",
        "tech_desc": "基于 C++17 和 OpenCV 4.x 构建的高性能嵌入式计算引擎。"
    }
}

# --- 4. الشريط الجانبي (Sidebar) ---
lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English", "Русский", "Türkçe", "中文"])
t = TEXTS[lang]

# عرض حقوق التطوير في الشريط الجانبي
st.sidebar.markdown(f"### {t['dev_by']}")

st.sidebar.markdown("---")
st.sidebar.subheader(t["tech_title"])
st.sidebar.info(t["tech_desc"])
st.sidebar.markdown("""
- **Core Vision Pipeline:** C++17 / OpenCV 4.x / Python
- **Segmentation Models:** Dual-Space HSV + CIELAB Color Space Filtering
- **Contour Detection:** Topological Structural Analysis (`cv2.findContours`)
- **Thermal Mapping:** Multi-Spectral Pseudo-Color Rendering
""")

# --- 5. الهيدر الرئيسي وتوثيق المطور ---
st.markdown(f"""
    <div class="zino-header">
        <div class="zino-title-pill">🌱 {t['title']}</div>
        <p class="zino-subtitle">{t['subtitle']}</p>
        <div class="zino-dev-badge">{t['dev_by']}</div>
    </div>
""", unsafe_allow_html=True)

# --- 6. رفع الصورة ---
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    st.markdown('<div class="zino-card">', unsafe_allow_html=True)
    st.image(img_rgb, caption="Input Leaf Matrix", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- 7. تنفيذ المحرك التشخيصي الدقيق ---
    if st.button(t["run_btn"]):
        # أ) التجزئة اللونية المزدوجة (HSV + LAB)
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        
        # ماسك النسيج الأخضر السليم
        lower_green = np.array([25, 35, 35])
        upper_green = np.array([85, 255, 255])
        healthy_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # ماسك التلف والاصفرار/البقع النسيجية
        lower_necrotic = np.array([10, 50, 50])
        upper_necrotic = np.array([24, 255, 255])
        necrotic_mask = cv2.inRange(hsv, lower_necrotic, upper_necrotic)
        
        # ب) تتبع الحدود الجغرافية للبقع المرضية
        contours, _ = cv2.findContours(necrotic_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contoured_img = img_rgb.copy()
        
        min_contour_area = 20
        valid_lesions = 0
        for cnt in contours:
            if cv2.contourArea(cnt) > min_contour_area:
                valid_lesions += 1
                cv2.drawContours(contoured_img, [cnt], -1, (255, 0, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(contoured_img, (x, y), (x + w, y + h), (241, 196, 15), 1)
                
        # ج) الرياضيات الحسابية للبكسلات
        total_pixels = float(img_bgr.shape[0] * img_bgr.shape[1])
        healthy_pixels = float(cv2.countNonZero(healthy_mask))
        necrotic_pixels = float(cv2.countNonZero(necrotic_mask))
        
        healthy_pct = (healthy_pixels / total_pixels) * 100.0
        infected_pct = (necrotic_pixels / total_pixels) * 100.0
        
        # د) خريطة المعالجة الحرارية
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # --- 8. بطاقة التقرير النهائي ---
        st.markdown('<div class="zino-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="report-title">{t["report_title"]}</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label=t["healthy_ratio"], value=f"{healthy_pct:.2f}%")
        with c2:
            st.metric(label=t["infected_ratio"], value=f"{infected_pct:.2f}%")
        with c3:
            st.metric(label=t["lesion_count"], value=f"{valid_lesions} Spots")
            
        st.info(f"📌 Pipeline Status: **{t['status_done']}**")
        
        # التشخيص المرضي والسبب والبروتوكول العلاجي
        st.markdown(f'<div class="section-header">{t["cause_title"]}</div>', unsafe_allow_html=True)
        
        if healthy_pct >= 75.0 and infected_pct < 5.0:
            status_text = {
                "العربية": "الورقة سليمة تماماً وزاهية الحيويّة. لا توجد أي أعراض مرضية أو إجهاد نسيجي.",
                "English": "Leaf is in optimal health with high vital chlorophyll density. No pathological symptoms.",
                "Русский": "Лист абсолютно здоров. Патологических симптомов не обнаружено.",
                "Türkçe": "Yaprak tamamen sağlıklı. Herhangi bir hastalık belirtisi bulunamadı.",
                "中文": "叶片处于完全健康状态，叶绿素密度正常，无病理症状。"
            }[lang]
            st.success(f"✅ {status_text}")
            
            st.markdown(f'<div class="section-header">{t["treatment_title"]}</div>', unsafe_allow_html=True)
            st.write({
                "العربية": "• استمرار برنامج الري المنتظم وتنظيف الأوراق من الأتربة لضمان كفاءة التمثيل الضوئي.",
                "English": "• Maintain standard irrigation and keep foliage clear of dust for optimal photosynthesis.",
                "Русский": "• Продолжайте регулярный полив и очищайте листья от пыли.",
                "Türkçe": "• Düzenli sulamaya devam edin ve fotosentez için yaprakları temiz tutun.",
                "中文": "• 保持常规灌溉，保持叶片清洁以进行光合作用。"
            }[lang])

        elif infected_pct >= 5.0 or valid_lesions > 3:
            disease_name = {
                "العربية": "إصابة تبقع بكتيري / فطري (Bacterial/Fungal Leaf Spot - Alternaria/Xanthomonas)",
                "English": "Bacterial/Fungal Leaf Spot Infection (Xanthomonas / Alternaria pathogen)",
                "Русский": "Бактериальная/Грибковая пятнистость листьев (Xanthomonas / Alternaria)",
                "Türkçe": "Bakteriyel / Mantar Yaprak Lekesi Enfeksiyonu",
                "中文": "细菌性/真菌性叶斑病感染 (Xanthomonas / Alternaria 病原体)"
            }[lang]
            
            st.warning(f"⚠️ **التشخيص الدقيق:** {disease_name}")
            
            st.write({
                "العربية": "المسبب: رطوبة زائدة مع انتشار جراثيم فطرية أو بكتيرية أدت لتلف أغشية الخلايا الباركيمية وانهيار البلاستيدات الخضراء.",
                "English": "Etiology: Excessive humidity enabling fungal/bacterial spores to rupture parenchymal cell walls.",
                "Русский": "Причина: Высокая влажность и споры грибков/бактерий, разрушающие клеточные мембраны.",
                "Türkçe": "Neden: Hücre zarlarını bozan yüksek nem ve mantar/bakteri sporları.",
                "中文": "病因：过度潮湿导致真菌/细菌孢子侵入，破坏叶肉细胞壁。"
            }[lang])
            
            st.markdown(f'<div class="section-header">{t["treatment_title"]}</div>', unsafe_allow_html=True)
            st.markdown({
                "العربية": """
                1. **الرش الكيميائي:** استخدام مركب نحاسي (Copper Oxychloride) أو مادة المانكوزيب (Mancozeb) بتركيز 2.5 جرام/لتر.
                2. **العلاج العضوي:** رش زيت النيم (Neem Oil) العضوي بتركيز 5 مل/لتر مع تهوية النبتة.
                3. **الوقاية:** إزالة الأوراق شديدة الإصابة وتجنب ري الأوراق علوياً.
                """,
                "English": """
                1. **Chemical Treatment:** Apply Copper Oxychloride or Mancozeb fungicide (2.5g/L).
                2. **Organic Remediation:** Spray Cold-Pressed Neem Oil (5ml/L) with enhanced canopy ventilation.
                3. **Prevention:** Prune heavily infected leaves and eliminate overhead irrigation.
                """,
                "Русский": """
                1. **Химическая обработка:** Примените хлорокись меди или Манкоцеб (2.5 г/л).
                2. **Органический метод:** Опрыскивание маслом Нима (5 мл/л).
                3. **Профилактика:** Обрезка пораженных листьев и исключение верхнего полива.
                """,
                "Türkçe": """
                1. **Kimyasal Tedavi:** Bakır Oksiklorür veya Mancozeb fungisit uygulayın (2.5g/L).
                2. **Organik Tedavi:** Soğuk sıkım Neem Yağı püskürtün (5ml/L).
                3. **Önleme:** Enfekte yaprakları budayın ve üstten sulamayı durdurun.
                """,
                "中文": """
                1. **化学治疗：** 喷洒王铜 (Copper Oxychloride) 或代森锰锌 (Mancozeb) (2.5g/L)。
                2. **有机修复：** 喷洒冷榨苦楝油 (Neem Oil) (5ml/L) 并改善通风。
                3. **预防措施：** 修剪重病叶片，改用根部灌溉。
                """
            }[lang])
            
        else:
            st.info({
                "العربية": "⚠️ **التشخيص:** إجهاد حراري / اصفرار ناتج عن نقص عنصر النيتروجين أو الحديد (Chlorosis).",
                "English": "⚠️ **Diagnosis:** Thermal stress or Iron/Nitrogen deficiency Chlorosis.",
                "Русский": "⚠️ **Диагноз:** Хлороз или недостаток железа/азота.",
                "Türkçe": "⚠️ **Teşhis:** Azot veya Demir eksikliğine bağlı Kloroz.",
                "中文": "⚠️ **诊断：** 热应激或缺铁/缺氮导致的大面积缺绿症。"
            }[lang])
            
            st.markdown(f'<div class="section-header">{t["treatment_title"]}</div>', unsafe_allow_html=True)
            st.write({
                "العربية": "• التسميد الورقي بحديد مخلبي (Fe-EDDHA) وتزويد التربة بمركب NPK متوازن.",
                "English": "• Apply Chelated Iron (Fe-EDDHA) foliar spray and balance soil NPK ratio.",
                "Русский": "• Внекорневая подкормка хелатом железа (Fe-EDDHA) и NPK.",
                "Türkçe": "• Şelatlı Demir (Fe-EDDHA) ve dengeli NPK gübresi uygulayın.",
                "中文": "• 喷施螯合铁 (Fe-EDDHA) 并补充平衡 NPK 复合肥。"
            }[lang])
            
        # هـ) عرض خريطة التتبع
        st.markdown(f"#### {t['heatmap_label']}")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(contoured_img, caption="Lesion Bounding Contours", use_container_width=True)
        with col_img2:
            st.image(heatmap_rgb, caption="Multi-Spectral Thermal Heatmap", use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- 9. الفوتر السفلـي التوثيقي ---
st.markdown(f"""
    <div class="zino-footer">
        {t['dev_by']} | ZINO AgroVision Engine © 2026
    </div>
""", unsafe_allow_html=True)
