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

# --- 2. التصميم البصري الكامل (CSS) ---
# خلفية صفراء خارجية حقيقية + بطاقات داكنة بإطار أصفر ذهبي مع زر أزرق برّاق
st.markdown("""
    <style>
    /* خلفية المنصة الصفراء الكلاسيكية */
    .stApp {
        background-color: #f1c40f !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
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
        font-size: 2.1rem;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .zino-subtitle {
        color: #c9d1d9;
        font-size: 0.95rem;
        margin: 0;
        font-weight: 500;
    }
    
    /* الحاويات الداكنة للصور والتقارير */
    .zino-card {
        background-color: #0d1117;
        border: 2px solid #161b22;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        color: #f0f6fc;
        box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.35);
    }
    
    /* زر الفحص الأزرق */
    div.stButton > button {
        background: linear-gradient(90deg, #0052d4, #4364f7, #6fb1fc) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        padding: 16px 24px !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 15px rgba(0, 82, 212, 0.5) !important;
        cursor: pointer !important;
        transition: all 0.3s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(0, 82, 212, 0.7) !important;
    }
    
    /* عناوين التقارير الفرعية */
    .report-title {
        color: #f1c40f;
        font-size: 1.35rem;
        font-weight: bold;
        margin-bottom: 14px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. قاموس اللغات الخمس الشامل (I18N) ---
TEXTS = {
    "العربية": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Diagnostic System | Software Engineering & Computer Vision Hardware",
        "select_lang": "🌐 اختر اللغة / Select Language",
        "upload_label": "قم برفع صورة ورقة النبات للتحليل",
        "run_btn": "🔬 فحص وتشخيص الورقة الآن",
        "report_title": "📊 تقرير التشخيص الزراعي (Agriculture Diagnosis Report)",
        "healthy_ratio": "النسيج السليم (Healthy Tissue)",
        "infected_ratio": "النسيج المصاب / المتضرر (Infected / Damaged Area)",
        "status_done": "اكتمل التحليل - Analysis Complete",
        "heatmap_label": "خريطة المعالجة الشريحية والحرارية (HSV Segmentation & Thermal Map Analysis)",
        "healthy_msg": "الورقة بحالة جيدة جداً، النسيج النباتي الأخضر سليماً ضمن المعدل الطبيعي.",
        "warning_msg": "تم اكتشاف بقع بكتيرية أو إجهاد حراري/اصفرار على نسيج الورقة.",
        "tech_title": "⚙️ مواصفات المحرك (Core Highlights)",
        "tech_desc": "محرك معالجة صور مدمج مبني بلغة C++17 و OpenCV 4.x مخصص للأجهزة الطرفية (Edge SBCs) لتحليل الصُور فائق السرعة."
    },
    "English": {
        "title": "ZINO AgroVision",
        "subtitle": "Advanced Agricultural Diagnostic System | Software Engineering & Computer Vision Hardware",
        "select_lang": "🌐 Select Language",
        "upload_label": "Upload Leaf Image for Diagnostic",
        "run_btn": "🔬 Run Diagnostic & Visual Analysis Now",
        "report_title": "📊 Agricultural Diagnosis Report",
        "healthy_ratio": "Healthy Tissue",
        "infected_ratio": "Infected / Damaged Area",
        "status_done": "Analysis Complete",
        "heatmap_label": "HSV Segmentation & Thermal Map Analysis",
        "healthy_msg": "Leaf is in optimal health. Green tissue covers expected percentage.",
        "warning_msg": "Detected chlorotic lesions or tissue stress on leaf surface.",
        "tech_title": "⚙️ Core Engine Highlights",
        "tech_desc": "High-performance spatial filtering & frame processing built with pure C++17 and OpenCV 4.x for edge compute units."
    },
    "Русский": {
        "title": "ZINO AgroVision",
        "subtitle": "Усовершенствованная система сельхоздиагностики | Компьютерное зрение",
        "select_lang": "🌐 Выберите язык",
        "upload_label": "Загрузить изображение листа",
        "run_btn": "🔬 Начать диагностику и визуальный анализ",
        "report_title": "📊 Отчет о сельскохозяйственной диагностике",
        "healthy_ratio": "Здоровая ткань",
        "infected_ratio": "Пораженная область",
        "status_done": "Анализ завершен",
        "heatmap_label": "Тепловая карта и сегментация HSV",
        "healthy_msg": "Лист в хорошем состоянии. Зеленые ткани в норме.",
        "warning_msg": "Обнаружены признаки поражения или хлороза на листе.",
        "tech_title": "⚙️ Технические характеристики",
        "tech_desc": "Высокопроизводительный движок обработки изображений на C++17 и OpenCV 4.x для устройств Edge."
    },
    "Türkçe": {
        "title": "ZINO AgroVision",
        "subtitle": "Gelişmiş Tarımsal Teşhis Sistemi | Bilgisayarlı Görmü Donanımı",
        "select_lang": "🌐 Dil Seçin",
        "upload_label": "Teşhis İçin Yaprak Resmi Yükleyin",
        "run_btn": "🔬 Teşhisi ve Görsel Analizi Başlat",
        "report_title": "📊 Tarımsal Teşhis Raporu",
        "healthy_ratio": "Sağlıklı Doku",
        "infected_ratio": "Hasarlı / Enfekte Alan",
        "status_done": "Analiz Tamamlandı",
        "heatmap_label": "HSV Segmentasyon ve Termal Harita",
        "healthy_msg": "Yaprak oldukça sağlıklı. Yeşil doku normal seviyede.",
        "warning_msg": "Yaprak yüzeyinde lekelenme veya doku hasarı tespit edildi.",
        "tech_title": "⚙️ Çekirdek Sistem Özellikleri",
        "tech_desc": "C++17 ve OpenCV 4.x ile geliştirilmiş yüksek performanslı görüntü işleme motoru."
    },
    "中文": {
        "title": "ZINO AgroVision",
        "subtitle": "高级农业叶片诊断系统 | 计算机视觉与软件工程",
        "select_lang": "🌐 选择语言",
        "upload_label": "上传叶片图像进行诊断",
        "run_btn": "🔬 立即运行诊断与视觉分析",
        "report_title": "📊 农业诊断报告",
        "healthy_ratio": "健康组织",
        "infected_ratio": "受损 / 病变区域",
        "status_done": "分析完成",
        "heatmap_label": "HSV 分割与热力图",
        "healthy_msg": "叶片健康状况良好，绿色组织比例正常。",
        "warning_msg": "检测到叶片表面存在病斑或组织受损。",
        "tech_title": "⚙️ 核心引擎 Highlight",
        "tech_desc": "基于 C++17 与 OpenCV 4.x 构建的高性能嵌入式图像处理引擎，为边缘设备优化。"
    }
}

# --- 4. الشريط الجانبي (Sidebar) ---
lang = st.sidebar.selectbox("🌐 Language / اللغة", ["العربية", "English", "Русский", "Türkçe", "中文"])
t = TEXTS[lang]

# معلومات التقنيات من مستودع README
st.sidebar.markdown("---")
st.sidebar.subheader(t["tech_title"])
st.sidebar.info(t["tech_desc"])
st.sidebar.markdown("""
- **Core Languages:** C++17 / C++20 / Python
- **Vision Library:** OpenCV 4.x
- **Build System:** CMake
- **Target Hardware:** Embedded Linux / Edge SBCs
""")

# --- 5. الهيدر الذهبي الرئيسي ---
st.markdown(f"""
    <div class="zino-header">
        <div class="zino-title-pill">🌱 {t['title']}</div>
        <p class="zino-subtitle">{t['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. رفع الصورة ---
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # قراءة الصورة عبر OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # عرض الصورة الأصلية في بطاقة داكنة
    st.markdown('<div class="zino-card">', unsafe_allow_html=True)
    st.image(img_rgb, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- 7. زر الفحص التشخيصي ---
    if st.button(t["run_btn"]):
        # أ) الخطوة الأولى: Isolation (عزل اللون الأخضر بالـ HSV)
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # ب) الخطوة الثانية: Pixel Math (حساب البكسلات والنسب)
        total_pixels = float(img_bgr.shape[0] * img_bgr.shape[1])
        healthy_pixels = float(cv2.countNonZero(green_mask))
        healthy_pct = (healthy_pixels / total_pixels) * 100.0
        infected_pct = max(0.0, 100.0 - healthy_pct)
        
        # ج) الخطوة الثالثة: Thermal Heatmap Generation (الخريطة الحرارية)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        heatmap_rgb = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # --- 8. بطاقة تقرير التشخيص النهائي ---
        st.markdown('<div class="zino-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="report-title">{t["report_title"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=t["healthy_ratio"], value=f"{healthy_pct:.2f}%")
        with col2:
            st.metric(label=t["infected_ratio"], value=f"{infected_pct:.2f}%")
            
        st.info(f"📌 STATUS: **{t['status_done']}**")
        
        if healthy_pct > 20.0:
            st.success(t["healthy_msg"])
        else:
            st.warning(t["warning_msg"])
            
        st.markdown(f"#### {t['heatmap_label']}")
        st.image(heatmap_rgb, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
