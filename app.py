import cv2
import numpy as np
import streamlit as st

# --- 1. إعداد الصفحة العامة ---
st.set_page_config(
    page_title="ZINO AgroVision Engine",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. التصميم البصري (CSS) ---
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# --- 3. القاموس الموحد للغات الخمس ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": (
            "Advanced Agricultural Vision Engine | Quantitative Leaf Surface"
            " Diagnostics"
        ),
        "dev_by": "تصميم وتطوير إسماعيل حساسنة",
        "input_mode": "طريقة إدخال الصورة:",
        "cam_option": "📷 التقاط بواسطة الكاميرا",
        "upload_option": "📁 رفع صورة من الملفات",
        "cam_label": "وجه الكاميرا نحو ورقة النبات والتقط الصورة",
        "upload_label": "قم برفع صورة ورقة النبات للتحليل المكتبي والدقيق",
        "run_btn": "🔬 تشغيل تحليل الرؤية الحاسوبية والحساب الرقمي",
        "report_title": (
            "📊 تقرير التحليل الرقمي لسطح الورقة (Leaf Surface Analysis)"
        ),
        "healthy_ratio": "نسبة النسيج الأخضر الحيوي",
        "infected_ratio": "نسبة الإجهاد والتغير التصبغي",
        "lesion_count": "عدد مناطق التغير النسيجي المكتشفة",
        "status_done": (
            "تم عزل خلفية المشهد وعزل مصفوفة الورقة بنجاح 100%"
        ),
        "status_error": (
            "⚠️ تعذر التعرف على ورقة النبات. يرجى توجيه الكاميرا مباشرة نحو"
            " الورقة."
        ),
        "heatmap_label": (
            "عزل جسم الورقة والخريطة الحرارية الموجهة (Isolated Heatmap &"
            " Contours)"
        ),
        "tech_title": "⚙️ محرك المعالجة المتقدم",
        "tech_desc": (
            "تجزئة طيفية تعتمد على القناة a* في فضاء CIELAB لعزل خلفية الصور"
            " كلياً بدون أخطاء."
        ),
        "status_healthy": (
            "✅ **حالة الورقة:** النسيج النباتي سليم ومكتظ بالكلوروفيل الحيوي ضمن"
            " المعدلات الطبيعية الممتازة."
        ),
        "rec_title_normal": "🛠️ التوصيات العادية:",
        "rec_normal": (
            "• الحفاظ على جدول الري المنتظم وتجنب تعريض النبتة لإجهاد مائي أو"
            " حراري مفاجئ."
        ),
        "status_warning": (
            "⚠️ **حالة الورقة:** رصد إجهاد نسيجي وتراجع متوسط في الكثافة التصبغية"
            " على سطح الورقة."
        ),
        "rec_title_warn": "🛠️ خطة المعالجة والتحسين:",
        "rec_warn_1": (
            "1. **التسميد:** إضافة سماد متوازن يحتوي على عناصر الحديد والنيتروجين"
            " لتعويض تراجع الكلوروفيل."
        ),
        "rec_warn_2": (
            "2. **الري:** ضبط معدلات الرطوبة ومنع تجمع المياه على الأوراق لتقليل"
            " فرص التلف."
        ),
        "status_danger": (
            "🚨 **حالة الورقة:** انخفاض حاد في نسبة النسيج الأخضر السليم وظهور"
            " مناطق تغير تصبغي واسعة."
        ),
        "rec_title_danger": "🛠️ بروتوكول التدخل المباشر:",
        "rec_danger_1": (
            "1. **العزل:** فصل الأجزاء المصابة لضمان عدم انتقال الإجهاد أو الإصابة"
            " للأوراق المجاورة."
        ),
        "rec_danger_2": (
            "2. **المعاملة الزراعية:** استخدام مغذيات ورقية متخصصة ومراجعة"
            " ظروف الإضاءة والتهوية فوراً."
        ),
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": (
            "Advanced Agricultural Vision Engine | Quantitative Leaf Surface"
            " Diagnostics"
        ),
        "dev_by": "Designed and Developed by Ismail Hassasneh",
        "input_mode": "Image Input Method:",
        "cam_option": "📷 Capture via Camera",
        "upload_option": "📁 Upload File",
        "cam_label": "Point camera at the plant leaf and capture",
        "upload_label": "Upload leaf image for quantitative analysis",
        "run_btn": "🔬 Run Computer Vision & Pixel Analysis Engine",
        "report_title": "📊 Quantitative Leaf Surface Analysis Report",
        "healthy_ratio": "Vital Green Tissue Ratio",
        "infected_ratio": "Discolored / Stressed Area Ratio",
        "lesion_count": "Detected Anomaly Regions",
        "status_done": (
            "Background 100% Subtracted & Leaf Matrix Isolated"
        ),
        "status_error": (
            "⚠️ Could not identify leaf tissue. Please point camera or upload a"
            " clear image."
        ),
        "heatmap_label": "Isolated Leaf Contour & Spectral Heatmap",
        "tech_title": "⚙️ Advanced Vision Engine",
        "tech_desc": (
            "CIELAB Color Space channel-a* segmentation eliminating background"
            " noise completely."
        ),
        "status_healthy": (
            "✅ **Leaf Condition:** Plant tissue is healthy and rich in vital"
            " chlorophyll within optimal ranges."
        ),
        "rec_title_normal": "🛠️ Standard Recommendations:",
        "rec_normal": (
            "• Maintain regular irrigation schedules and protect the plant from"
            " sudden heat or water stress."
        ),
        "status_warning": (
            "⚠️ **Leaf Condition:** Tissue stress and moderate pigment loss"
            " detected on the leaf surface."
        ),
        "rec_title_warn": "🛠️ Treatment & Recovery Plan:",
        "rec_warn_1": (
            "1. **Fertilization:** Apply balanced fertilizer containing Iron"
            " and Nitrogen to restore chlorophyll."
        ),
        "rec_warn_2": (
            "2. **Irrigation:** Regulate soil moisture and avoid water"
            " accumulation on foliage to reduce decay risk."
        ),
        "status_danger": (
            "🚨 **Leaf Condition:** Severe reduction in healthy green tissue"
            " with widespread pigment damage."
        ),
        "rec_title_danger": "🛠️ Direct Intervention Protocol:",
        "rec_danger_1": (
            "1. **Isolation:** Separate affected leaves/parts to prevent"
            " stress or infection spreading to adjacent foliage."
        ),
        "rec_danger_2": (
            "2. **Agricultural Treatment:** Apply specialized foliar nutrients"
            " and inspect lighting/ventilation immediately."
        ),
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": (
            "Система компьютерного зрения | Количественная диагностика"
            " поверхности листа"
        ),
        "dev_by": "Дизайн и разработка: Исмаил Хассасне",
        "input_mode": "Способ ввода изображения:",
        "cam_option": "📷 Сделать снимок камерой",
        "upload_option": "📁 Загрузить файл",
        "cam_label": "Направьте камеру на лист и сделайте снимок",
        "upload_label": "Загрузить изображение листа для анализа",
        "run_btn": "🔬 Запустить компьютерный анализ пикселей",
        "report_title": "📊 Отчет о количественном анализе поверхности листа",
        "healthy_ratio": "Доля здоровой зеленой ткани",
        "infected_ratio": "Доля измененной/стрессовой ткани",
        "lesion_count": "Обнаружено аномальных зон",
        "status_done": (
            "Удаление фона и изоляция листа выполнены на 100%"
        ),
        "status_error": (
            "⚠️ Не удалось распознать лист. Направьте камеру или загрузите"
            " четкое изображение."
        ),
        "heatmap_label": (
            "Изолированный контур листа и тепловая карта"
        ),
        "tech_title": "⚙️ Характеристики движка",
        "tech_desc": (
            "Сегментация на основе канала a* в CIELAB, полностью исключающая"
            " фоновые помехи."
        ),
        "status_healthy": (
            "✅ **Состояние листа:** Ткани листа полностью здоровы и насыщены"
            " хлорофиллом в пределах нормы."
        ),
        "rec_title_normal": "🛠️ Стандартные рекомендации:",
        "rec_normal": (
            "• Поддерживайте регулярный полив и защищайте растение от"
            " перепадов температуры."
        ),
        "status_warning": (
            "⚠️ **Состояние листа:** Обнаружен стресс тканей и умеренное"
            " снижение пигментации."
        ),
        "rec_title_warn": "🛠️ План восстановления и лечения:",
        "rec_warn_1": (
            "1. **Удобрение:** Внесите сбалансированное удобрение с железом и"
            " азотом для восстановления хлорофилла."
        ),
        "rec_warn_2": (
            "2. **Полив:** Отрегулируйте уровень влажности и избегайте"
            " скопления воды на листьях."
        ),
        "status_danger": (
            "🚨 **Состояние листа:** Острое снижение здоровой зеленой ткани и"
            " обширные зоны повреждений."
        ),
        "rec_title_danger": "🛠️ Протокол прямого вмешательства:",
        "rec_danger_1": (
            "1. **Изоляция:** Удалите пораженные участки для предотвращения"
            " распространения инфекции."
        ),
        "rec_danger_2": (
            "2. **Обработка:** Примените специализированные листовые"
            " подкормки и проверьте освещение."
        ),
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": (
            "Gelişmiş Tarımsal Görme Motoru | Nicel Yaprak Yüzeyi Teşhisi"
        ),
        "dev_by": "Tasarım ve Geliştirme: İsmail Hassasneh",
        "input_mode": "Görüntü Giriş Yöntemi:",
        "cam_option": "📷 Kamera ile Çek",
        "upload_option": "📁 Dosya Yükle",
        "cam_label": "Kamerayı yaprağa doğrultun ve çekim yapın",
        "upload_label": "Nicel analiz için yaprak resmi yükleyin",
        "run_btn": "🔬 Bilgisayarlı Görme ve Piksel Analizini Çalıştır",
        "report_title": "📊 Nicel Yaprak Yüzeyi Analiz Raporu",
        "healthy_ratio": "Canlı Yeşil Doku Oranı",
        "infected_ratio": "Renk Değişimi / Stresli Alan Oranı",
        "lesion_count": "Tespit Edilen Anomali Bölgesi",
        "status_done": (
            "Arka Plan %100 Ayrıştırıldı ve Yaprak Matrisi İzole Edildi"
        ),
        "status_error": (
            "⚠️ Yaprak tespit edilemedi. Lütfen kamerayı doğrultun veya net bir"
            " resim yükleyin."
        ),
        "heatmap_label": "İzole Yaprak Konturu ve Spektral Harita",
        "tech_title": "⚙️ Motor Özellikleri",
        "tech_desc": (
            "Gürültüyü tamamen ortadan kaldıran CIELAB a*-kanalı segmentasyonu."
        ),
        "status_healthy": (
            "✅ **Yaprak Durumu:** Bitki dokusu son derece sağlıklı ve klorofil"
            " açısından optimum düzeydedir."
        ),
        "rec_title_normal": "🛠️ Standart Öneriler:",
        "rec_normal": (
            "• Düzenli sulama takvimini koruyun ve bitkiyi ani sıcaklık veya su"
            " stresinden koruyun."
        ),
        "status_warning": (
            "⚠️ **Yaprak Durumu:** Yaprak yüzeyinde doku stresi ve orta"
            " düzeyde pigment kaybı tespit edildi."
        ),
        "rec_title_warn": "🛠️ İyileştirme ve Tedavi Planı:",
        "rec_warn_1": (
            "1. **Gübreleme:** Klorofil seviyesini artırmak için Demir ve Azot"
            " içeren gübre uygulayın."
        ),
        "rec_warn_2": (
            "2. **Sulama:** Toprak nemini düzenleyin ve yapraklarda su"
            " birikmesini önleyin."
        ),
        "status_danger": (
            "🚨 **Yaprak Durumu:** Sağlıklı yeşil dokuda ciddi azalma ve yaygın"
            " renk değişimi/hasar saptandı."
        ),
        "rec_title_danger": "🛠️ Doğrudan Müdahale Protokolü:",
        "rec_danger_1": (
            "1. **İzolasyon:** Stres veya hastalığın komşu yapraklara"
            " yayılmasını önlemek için etkilenen kısımları ayırın."
        ),
        "rec_danger_2": (
            "2. **Tarım Uygulaması:** Özel yaprak gübreleri uygulayın, ışık ve"
            " havalandırmayı gözden geçirin."
        ),
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业视觉引擎 | 叶片表面定量诊断",
        "dev_by": "设计与开发：Ismail Hassasneh",
        "input_mode": "图像输入方式：",
        "cam_option": "📷 拍照",
        "upload_option": "📁 上传文件",
        "cam_label": "将摄像头对准树叶进行拍摄",
        "upload_label": "上传叶片图像进行定量分析",
        "run_btn": "🔬 运行计算机视觉与像素分析引擎",
        "report_title": "📊 叶片表面定量分析报告",
        "healthy_ratio": "绿色健康组织比例",
        "infected_ratio": "受损 / 变色区域比例",
        "lesion_count": "检测到的异常区域数量",
        "status_done": "背景100%扣除，叶片矩阵成功隔离",
        "status_error": "⚠️ 无法识别叶片。请对准树叶或上传清晰的叶片图像。",
        "heatmap_label": "隔离叶片轮廓与多光谱热力图",
        "tech_title": "⚙️ 视觉引擎规格",
        "tech_desc": (
            "基于 CIELAB 色彩空间 a* 通道的精确定向分割，完全消除背景干扰。"
        ),
        "status_healthy": (
            "✅ **叶片状态：** 植物组织非常健康，叶绿素含量处于极佳的标准范围内。"
        ),
        "rec_title_normal": "🛠️ 常规养护建议：",
        "rec_normal": "• 保持定期灌溉计划，避免植物遭受突发的干旱或高温应激。",
        "status_warning": (
            "⚠️ **叶片状态：** 检测到叶片表面存在组织应力及中等程度的色素衰退。"
        ),
        "rec_title_warn": "🛠️ 修复与治疗方案：",
        "rec_warn_1": (
            "1. **施肥：** 施用富含铁和氮的平衡肥料，补充叶绿素合成。"
        ),
        "rec_warn_2": "2. **灌溉：** 调节土壤湿度，避免叶片表面积水。",
        "status_danger": (
            "🚨 **叶片状态：**"
            " 健康绿色组织大幅减少，并出现广泛的色素病变与受损区域。"
        ),
        "rec_title_danger": "🛠️ 直接干预协议：",
        "rec_danger_1": (
            "1. **隔离：** 剪除或隔离受损部位，防止病变蔓延至邻近叶片。"
        ),
        "rec_danger_2": (
            "2. **叶面治疗：**"
            " 喷施专用叶面营养剂，并立即检查光照与通风条件。"
        ),
    },
}

# --- 4. الشريط الجانبي ---
lang = st.sidebar.selectbox(
    "🌐 Choose Language / اختر اللغة",
    ["العربية", "English", "Русский", "Türkçe", "中文"],
)
t = TEXTS[lang]

st.sidebar.markdown(f"### 👨‍💻 {t['dev_by']}")
st.sidebar.markdown("---")
st.sidebar.subheader(t["tech_title"])
st.sidebar.info(t["tech_desc"])

# --- 5. الهيدر الرئيسي ---
st.markdown(
    f"""
    <div class="zino-header">
        <div class="zino-title-pill">🌱 {t['title']}</div>
        <p class="zino-subtitle">{t['subtitle']}</p>
        <div class="zino-dev-badge">{t['dev_by']}</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- 6. اختيار طريقة الإدخال ورفع الصورة ---
input_choice = st.radio(
    t["input_mode"],
    [t["cam_option"], t["upload_option"]],
    horizontal=True,
)

uploaded_file = None
if input_choice == t["cam_option"]:
  uploaded_file = st.camera_input(t["cam_label"])
else:
  uploaded_file = st.file_uploader(
      t["upload_label"], type=["jpg", "jpeg", "png"]
  )

if uploaded_file is not None:
  file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
  img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
  img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

  st.markdown('<div class="zino-card">', unsafe_allow_html=True)
  st.image(img_rgb, caption="Input Leaf Frame", use_container_width=True)
  st.markdown("</div>", unsafe_allow_html=True)

  if st.button(t["run_btn"]):
    # --- الخوارزمية الحتمية والدقيقة لضمان ثبات النتائج ---
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    a_chan = lab[:, :, 1]

    # عزل الأنسجة النباتية بالاعتماد على القناة a* في CIELAB
    _, raw_leaf_mask = cv2.threshold(a_chan, 120, 255, cv2.THRESH_BINARY_INV)

    # تنظيف المورفولوجيا لضمان استقرار القناع
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    cleaned_mask = cv2.morphologyEx(raw_leaf_mask, cv2.MORPH_CLOSE, kernel)
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_OPEN, kernel)

    # استخراج مجسم الورقة الرئيسي وتجاهل الضوضاء الخارجية
    contours, _ = cv2.findContours(
        cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    leaf_mask = np.zeros_like(a_chan)
    if contours:
      largest_contour = max(contours, key=cv2.contourArea)
      cv2.drawContours(leaf_mask, [largest_contour], -1, 255, -1)

    total_leaf_pixels = float(cv2.countNonZero(leaf_mask))

    if total_leaf_pixels > 1000:
      # حساب النسيج الأخضر الحيوي في HSV
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

      # تتبع البقع بعتبة نسبية دقيقة وثابتة
      lesion_cnts, _ = cv2.findContours(
          damaged_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
      )

      background_black = np.zeros_like(img_rgb)
      display_contours = np.where(
          leaf_mask[:, :, None] == 255, img_rgb, background_black
      )

      if contours:
        cv2.drawContours(
            display_contours, [largest_contour], -1, (0, 255, 0), 2
        )

      min_lesion_area = max(30, int(total_leaf_pixels * 0.0004))
      valid_lesions = 0
      for lc in lesion_cnts:
        if cv2.contourArea(lc) > min_lesion_area:
          valid_lesions += 1
          cv2.drawContours(display_contours, [lc], -1, (255, 0, 0), 2)

      # توليد الخريطة الحرارية الموجهة للورقة فقط
      gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
      heatmap_raw = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
      heatmap_rgb = cv2.cvtColor(heatmap_raw, cv2.COLOR_BGR2RGB)
      heatmap_final = cv2.bitwise_and(heatmap_rgb, heatmap_rgb, mask=leaf_mask)

      # --- 7. عرض النتائج والتوصيات باللغة الحالية بالكامل ---
      st.markdown('<div class="zino-card">', unsafe_allow_html=True)
      st.markdown(
          f'<div class="report-title">{t["report_title"]}</div>',
          unsafe_all
