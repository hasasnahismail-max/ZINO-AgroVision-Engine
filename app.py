import streamlit as st
import cv2
import numpy as np

# --- 1. تهيئة الصفحة العامة ---
st.set_page_config(
    page_title="ZINO AgroVision Engine",
    page_icon="🫒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. رمز أيقونة شجرة الزيتون والكاميرا المدمج برمجياً (SVG) ---
OLIVE_CAM_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="65" height="65" style="border-radius: 50%; border: 2px solid #f1c40f; background: #0d1117; padding: 4px; box-shadow: 0px 4px 10px rgba(0,0,0,0.5);">
  <path d="M 45,90 C 40,70 35,55 42,42 C 48,32 52,32 58,42 C 65,55 60,70 55,90 Z" fill="#795548"/>
  <path d="M 40,85 C 32,88 25,92 20,95 M 60,85 C 68,88 75,92 80,95" stroke="#5d4037" stroke-width="4" stroke-linecap="round"/>
  <circle cx="35" cy="30" r="16" fill="#2e7d32"/>
  <circle cx="65" cy="30" r="16" fill="#2e7d32"/>
  <circle cx="50" cy="20" r="18" fill="#388e3c"/>
  <circle cx="28" cy="40" r="12" fill="#1b5e20"/>
  <circle cx="72" cy="40" r="12" fill="#1b5e20"/>
  <ellipse cx="32" cy="25" rx="3" ry="5" fill="#fbc02d"/>
  <ellipse cx="68" cy="25" rx="3" ry="5" fill="#fbc02d"/>
  <ellipse cx="50" cy="14" rx="3" ry="5" fill="#fbc02d"/>
  <rect x="36" y="48" width="28" height="20" rx="3" fill="#212121" stroke="#f1c40f" stroke-width="1.5"/>
  <circle cx="50" cy="58" r="6" fill="#424242" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="50" cy="58" r="3" fill="#00bcd4"/>
  <rect x="42" y="45" width="8" height="3" fill="#616161"/>
  <circle cx="60" cy="52" r="1.5" fill="#ff5252"/>
</svg>
"""

# --- 3. التصميم البصري الكامل (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f1c40f !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
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
        padding: 16px;
        margin-bottom: 20px;
        color: #f0f6fc;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. القاموس الخماسي الموحد للغات الخمس (I18N) ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "تصميم وتطوير إسماعيل حساسنة",
        "olive_cam_title": "كاميرا شجرة الزيتون الذكية - طرق الإدخال المخصصة للأوراق والشجر:",
        "input_mode": "اختر طريقة الإدخال المناسبة لعدم كشف ألبوم الصور الشخصية:",
        "sample_select": "🍃 اختر عينة ورقة شجر جاهزة للتجربة وتسجيل الشاشة:",
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
        "tech_desc": "تجزئة طيفية تعتمد على القناة a* في فضاء CIELAB لعزل خلفية الصور كلياً وتصفية الأجسام الغريبة.",
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
        "rec_danger_2": "2. **المعاملة الزراعية:** استخدام مغذيات ورقية متخصصة ومراجعة ظروف الإضاءة والتهوية فوراً.",
        "invalid_leaf_err": "🚨 **الصورة غير مطابقة!** لم يتم التعرف على ورقة شجر أو نسيج نباتي واضح (المحرك يمنع تحليل الأجسام الغريبة مثل الأشخاص أو السيارات)."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Vision Engine | Quantitative Leaf Surface Diagnostics",
        "dev_by": "Designed and Developed by Ismail Hassasneh",
        "olive_cam_title": "Olive Tree Vision Cam - Leaf & Tree Specialized Input Methods:",
        "input_mode": "Select Input Mode (Prevents exposing personal gallery):",
        "sample_select": "🍃 Select Built-in Leaf Sample for Screen Recording & Demo:",
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
        "tech_desc": "CIELAB Color Space channel-a* segmentation eliminating background noise completely and filtering non-plant objects.",
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
        "rec_danger_2": "2. **Foliar Treatment:** Apply specialized foliar nutrients and re-evaluate light and ventilation.",
        "invalid_leaf_err": "🚨 **Invalid Image!** No valid leaf detected (Engine excludes non-plant objects)."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Система компьютерного зрения | Количественная диагностика поверхности листа",
        "dev_by": "Дизайн и разработка: Исмаил Хассасне",
        "olive_cam_title": "Камера Olive Vision - Специализированный ввод для листьев:",
        "input_mode": "Выберите режим ввода (защита личной галереи):",
        "sample_select": "🍃 Выберите образец листа для записи экрана:",
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
        "rec_danger_2": "2. **Обработка:** Примените специальные листовые подкормки и проверьте вентиляцию.",
        "invalid_leaf_err": "🚨 **Недействительное изображение!** Пожалуйста, используйте только снимки листьев."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Görme Motoru | Nicel Yaprak Yüzeyi Teşhisi",
        "dev_by": "Tasarım ve Geliştirme: İsmail Hassasneh",
        "olive_cam_title": "Zeytin Ağacı Kamerası - Özel Yaprak Giriş Yöntemleri:",
        "input_mode": "Giriş Yöntemini Seçin (Kişisel galeriyi korur):",
        "sample_select": "🍃 Ekran Kaydı İçin Dahili Yaprak Örneği Seçin:",
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
        "rec_danger_2": "2. **Yaprak Tedavisi:** Özel yaprak besinleri uygulayın ve ışık/havalandırmayı gözden geçirin.",
        "invalid_leaf_err": "🚨 **Geçersiz Görsel!** Lütfen sadece bitki yaprakları görseli kullanın."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业视觉引擎 | 叶片表面定量诊断",
        "dev_by": "设计与开发：Ismail Hassasneh",
        "olive_cam_title": "橄榄树智能相机 - 树叶专用输入模式：",
        "input_mode": "选择输入模式（防止暴露个人相册）：",
        "sample_select": "🍃 选择内置树叶样本（适合录屏与演示）：",
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
        "tech_desc": "基于 CIELAB 色彩空间 a* 通道的精确定向分割，完全消除背景干扰与非植物杂质。",
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
        "rec_danger_2": "2. **叶面治疗：** 喷施专用叶面营养剂，重新评估光照与通风条件。",
        "invalid_leaf_err": "🚨 **无效图像！** 请仅使用植物叶片图像。"
    }
}

# --- 5. الشريط الجانبي (Sidebar) ---
lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", ["العربية", "English", "Русский", "Türkçe", "中文"])
t = TEXTS[lang]

st.sidebar.markdown(f'<div style="text-align: center; margin-bottom: 10px;">{OLIVE_CAM_SVG}</div>', unsafe_allow_html=True)
st.sidebar.markdown(f"### 👨‍💻 {t['dev_by']}")
st.sidebar.markdown("---")
st.sidebar.subheader(t["tech_title"])
st.sidebar.info(t["tech_desc"])

# --- 6. الهيدر الرئيسي ---
st.markdown(f"""
    <div class="zino-header">
        <div class="zino-title-pill">🌱 {t['title']}</div>
        <p class="zino-subtitle">{t['subtitle']}</p>
        <div class="zino-dev-badge">{t['dev_by']}</div>
    </div>
""", unsafe_allow_html=True)

# --- 7. منشئ عينات الأوراق لتسهيل العرض وتسجيل الشاشة ---
def generate_sample_leaf(sample_type):
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    img[:] = (200, 180, 160)
    if sample_type == "healthy_olive":
        cv2.ellipse(img, (200, 200), (60, 160), 15, 0, 360, (30, 140, 40), -1)
        cv2.line(img, (200, 40), (200, 360), (20, 100, 30), 3)
    elif sample_type == "spot_leaf":
        cv2.ellipse(img, (200, 200), (120, 140), 0, 0, 360, (35, 130, 45), -1)
        cv2.circle(img, (160, 160), 22, (20, 40, 180), -1)
        cv2.circle(img, (240, 220), 18, (20, 40, 180), -1)
        cv2.circle(img, (190, 260), 25, (20, 40, 180), -1)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# --- 8. حاوية الكاميرا وطرق الإدخال المخصصة 🫒📸 ---
st.markdown('<div class="olive-cam-container">', unsafe_allow_html=True)

col_icon, col_txt = st.columns([1, 6])
with col_icon:
    st.markdown(f'<div style="text-align: center;">{OLIVE_CAM_SVG}</div>', unsafe_allow_html=True)
with col_txt:
    st.markdown(f"<h4 style='margin-top: 10px;'>{t['olive_cam_title']}</h4>", unsafe_allow_html=True)

input_type = st.radio(t["input_mode"], [
    "🍃 Demo Leaf Gallery (لتسجيل الشاشة بدون فتح المعرض الشخصي)",
    "🫒 Live Olive-Cam (الكاميرا المباشرة)",
    "📁 File Storage (رفع ملف من الجهاز)"
], horizontal=False)

uploaded_file = None
selected_sample_img = None

if "Demo Leaf Gallery" in input_type:
    sample_choice = st.selectbox(t["sample_select"], [
        "ورقة زيتون سليمة (Healthy Olive Leaf)",
        "ورقة بها بقع وتجهد نسيجي (Leaf with Lesions)"
    ])
    if "Healthy" in sample_choice or "سليمة" in sample_choice:
        selected_sample_img = generate_sample_leaf("healthy_olive")
    else:
        selected_sample_img = generate_sample_leaf("spot_leaf")
elif "Olive-Cam" in input_type:
    uploaded_file = st.camera_input(t["cam_label"])
else:
    uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

st.markdown('</div>', unsafe_allow_html=True)

# تجهيز صورة الفحص
img_rgb = None
if selected_sample_img is not None:
    img_rgb = selected_sample_img
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
elif uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if img_bgr is not None:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

if img_rgb is not None:
    st.markdown('<div class="zino-card">', unsafe_allow_html=True)
    st.image(img_rgb, caption="Input Image Frame", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button(t["run_btn"]):
        # --- الفحص الصارم للنسيج النباتي وعزل الأجسام الغريبة ---
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
        total_img_pixels = float(img_bgr.shape[0] * img_bgr.shape[1])
        leaf_coverage_ratio = (total_leaf_pixels / total_img_pixels) * 100.0

    if total_leaf_pixels > 1000 and leaf_coverage_ratio > 1.5:
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower_green = np.array([28, 35, 35])
        upper_green = np.array([88, 255, 255])
        green_raw = cv2.inRange(hsv, lower_green, upper_green)
