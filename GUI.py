import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import os
import json

# 设置页面配置
st.set_page_config(
    page_title="医院管理系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 数据文件路径
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PATIENTS_FILE = os.path.join(DATA_DIR, "patients.json")
DOCTORS_FILE = os.path.join(DATA_DIR, "doctors.json")
PRESCRIPTIONS_FILE = os.path.join(DATA_DIR, "prescriptions.json")

# 创建数据文件夹（如果不存在）
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 初始化数据文件
def init_data_files():
    # 患者数据
    if not os.path.exists(PATIENTS_FILE):
        initial_patients = []
        with open(PATIENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_patients, f, ensure_ascii=False, indent=4)
    
    # 医生数据
    if not os.path.exists(DOCTORS_FILE):
        initial_doctors = [
            {"id": 1, "name": "张医生", "department": "内科", "specialty": "心血管疾病"},
            {"id": 2, "name": "李医生", "department": "外科", "specialty": "骨科"},
            {"id": 3, "name": "王医生", "department": "儿科", "specialty": "儿童发育"},
            {"id": 4, "name": "赵医生", "department": "神经科", "specialty": "神经疾病"}
        ]
        with open(DOCTORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_doctors, f, ensure_ascii=False, indent=4)
    
    # 处方数据
    if not os.path.exists(PRESCRIPTIONS_FILE):
        initial_prescriptions = []
        with open(PRESCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_prescriptions, f, ensure_ascii=False, indent=4)

# 初始化数据文件
init_data_files()

# 读取患者数据
def load_patients():
    try:
        with open(PATIENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 保存患者数据
def save_patients(patients):
    with open(PATIENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)

# 读取医生数据
def load_doctors():
    try:
        with open(DOCTORS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 读取处方数据
def load_prescriptions():
    try:
        with open(PRESCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# 保存处方数据
def save_prescriptions(prescriptions):
    with open(PRESCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(prescriptions, f, ensure_ascii=False, indent=4)

# 自定义CSS样式
# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
        .main {
            background-color: #f0f8ff;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        h1, h2, h3 {
            color: #0047AB;
        }
        .stButton>button {
            background-color: #0047AB;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #003380;
        }
        
        /* 卡片基本样式 */
        .card {
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background-color: white;
            margin-bottom: 1rem;
            color: #000000 !important;
        }
        
        /* 通用选择器，强制所有卡片内的元素使用黑色 */
        .card * {
            color: #000000 !important;
        }
        
        /* 具体元素的样式覆盖 */
        .card h3, .card h4, .card p, .card label, .card span,
        .card div, .card input, .card textarea, .card select, 
        .card option, .card button {
            color: #000000 !important;
        }
        
        /* Streamlit组件的文本颜色 */
        .card .stTextInput input, 
        .card .stTextArea textarea,
        .card .stNumberInput input,
        .card .stSelectbox select,
        .card .stSelectbox div,
        .card .stDateInput input {
            color: #000000 !important;
        }
        
        /* Streamlit特殊类 */
        .card .st-eb, .card .st-bq, .card .st-aj, 
        .card .st-ae, .card .st-af, .card .st-ag, .card .st-ah, 
        .card .st-ai, .card .st-cx, .card .st-dc, .card .st-dd, 
        .card .st-de, .card .st-df, .card .st-dg, .card .st-dh,
        .card [data-testid="stText"], .card [data-testid="stMarkdown"] {
            color: #000000 !important;
        }
        
        /* 直接用标签选择器覆盖 */
        .card label, .card p, .card div, .card input, 
        .card textarea, .card select, .card option {
            color: #000000 !important;
        }
        
        /* 子元素选择器，确保嵌套元素也能正确显示颜色 */
        .card > *, .card > * > *, .card > * > * > * {
            color: #000000 !important;
        }
        
        /* 特别针对今日待诊患者和已登记患者挂号部分的样式 */
        [data-testid="stMarkdown"] div[style*="background-color:#f8f9fa"],
        [data-testid="stMarkdown"] div[style*="background-color:#e6f3ff"] {
            color: #000000 !important;
        }
        
        [data-testid="stMarkdown"] div[style*="background-color:#f8f9fa"] p,
        [data-testid="stMarkdown"] div[style*="background-color:#e6f3ff"] p,
        [data-testid="stMarkdown"] div[style*="background-color:#f8f9fa"] span,
        [data-testid="stMarkdown"] div[style*="background-color:#e6f3ff"] span,
        [data-testid="stMarkdown"] div[style*="background-color:#f8f9fa"] h4,
        [data-testid="stMarkdown"] div[style*="background-color:#e6f3ff"] h4 {
            color: #000000 !important;
        }
        
        .success-msg {
            padding: 1rem;
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .error-msg {
            padding: 1rem;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)
        
# 初始化session状态
if 'page' not in st.session_state:
    st.session_state.page = 'registration'
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = None
if 'success_message' not in st.session_state:
    st.session_state.success_message = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# 侧边栏导航
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=100)
    st.title("医院管理系统")
    st.markdown("---")
    
    if st.button("患者登记与挂号", key="nav_registration"):
        st.session_state.page = 'registration'
        st.session_state.success_message = None
        st.session_state.error_message = None
    
    if st.button("医生诊断与处方", key="nav_diagnosis"):
        st.session_state.page = 'diagnosis'
        st.session_state.success_message = None
        st.session_state.error_message = None
    
    if st.button("药房配药与结算", key="nav_pharmacy"):
        st.session_state.page = 'pharmacy'
        st.session_state.success_message = None
        st.session_state.error_message = None
    
    st.markdown("---")
    st.markdown("© 2025 医院管理系统")

# 显示成功消息
def show_success_message():
    if st.session_state.success_message:
        st.markdown(f"""
        <div class="success-msg">
            {st.session_state.success_message}
        </div>
        """, unsafe_allow_html=True)
        # 自动清除消息（5秒后）
        time.sleep(0.1)  # 让消息显示一下
        st.session_state.success_message = None

# 显示错误消息
def show_error_message():
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-msg">
            {st.session_state.error_message}
        </div>
        """, unsafe_allow_html=True)
        # 自动清除消息（5秒后）
        time.sleep(0.1)  # 让消息显示一下
        st.session_state.error_message = None

# 患者登记与挂号页面
def registration_page():
    st.title("患者登记与挂号")
    show_success_message()
    show_error_message()
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>新患者登记</h3>
        """, unsafe_allow_html=True)
        
        name = st.text_input("患者姓名")
        
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            gender = st.selectbox("性别", ["男", "女"])
        with col1_2:
            age = st.number_input("年龄", min_value=0, max_value=120, step=1)
        with col1_3:
            id_number = st.text_input("身份证号")
        
        phone = st.text_input("联系电话")
        address = st.text_input("家庭住址")
        
        col1_4, col1_5 = st.columns(2)
        with col1_4:
            department = st.selectbox("就诊科室", ["内科", "外科", "儿科", "妇科", "神经科", "皮肤科", "眼科", "耳鼻喉科"])
        with col1_5:
            # 根据科室筛选医生
            doctors = load_doctors()
            dept_doctors = [doc for doc in doctors if doc["department"] == department]
            doctor_names = [f"{doc['name']} ({doc['specialty']})" for doc in dept_doctors]
            selected_doctor = st.selectbox("选择医生", doctor_names)
        
        medical_history = st.text_area("病史简介")
        
        appointment_date = st.date_input("预约日期", min_value=datetime.now().date())
        
        col1_6, col1_7 = st.columns(2)
        with col1_6:
            insurance = st.selectbox("医保类型", ["城镇职工医保", "城乡居民医保", "商业保险", "自费"])
        with col1_7:
            priority = st.selectbox("挂号优先级", ["普通", "优先", "急诊"])
        
        if st.button("提交登记"):
            if not name or not id_number or not phone:
                st.session_state.error_message = "请填写必要信息（姓名、身份证号和联系电话）"
            else:
                patients = load_patients()
                # 检查是否已存在相同身份证的患者
                existing_patient = next((p for p in patients if p.get("id_number") == id_number), None)
                
                if existing_patient:
                    patient_id = existing_patient["id"]
                    st.session_state.success_message = f"患者 {name} 已存在，挂号成功！您的患者ID为: {patient_id}"
                else:
                    # 创建新患者
                    patient_id = random.randint(10000, 99999)
                    while any(p.get("id") == patient_id for p in patients):
                        patient_id = random.randint(10000, 99999)
                    
                    selected_doctor_name = selected_doctor.split()[0]
                    doctor_id = next((doc["id"] for doc in doctors if doc["name"] == selected_doctor_name), None)
                    
                    new_patient = {
                        "id": patient_id,
                        "name": name,
                        "gender": gender,
                        "age": age,
                        "id_number": id_number,
                        "phone": phone,
                        "address": address,
                        "department": department,
                        "doctor_id": doctor_id,
                        "medical_history": medical_history,
                        "appointment_date": appointment_date.strftime("%Y-%m-%d"),
                        "insurance": insurance,
                        "priority": priority,
                        "registration_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    patients.append(new_patient)
                    save_patients(patients)
                    
                    st.session_state.success_message = f"患者 {name} 登记成功！您的患者ID为: {patient_id}"
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>已登记患者挂号</h3>
        """, unsafe_allow_html=True)
        
        search_option = st.selectbox("搜索方式", ["患者ID", "身份证号"])
        search_value = st.text_input(f"请输入{search_option}")
        
        if st.button("查找患者"):
            if not search_value:
                st.session_state.error_message = "请输入搜索内容"
            else:
                patients = load_patients()
                found_patient = None
                
                if search_option == "患者ID":
                    try:
                        patient_id = int(search_value)
                        found_patient = next((p for p in patients if p.get("id") == patient_id), None)
                    except ValueError:
                        st.session_state.error_message = "患者ID必须是数字"
                else:  # 身份证号
                    found_patient = next((p for p in patients if p.get("id_number") == search_value), None)
                
                if found_patient:
                    # 显示患者信息
                    st.markdown(f"""
<div style="background-color:#e6f3ff; padding:10px; border-radius:5px; margin-top:10px;">
    <h4 style="color:#000000;">患者信息</h4>
    <p style="color:#000000;">姓名: {found_patient['name']}</p>
    <p style="color:#000000;">ID: {found_patient['id']}</p>
    <p style="color:#000000;">性别: {found_patient['gender']}</p>
    <p style="color:#000000;">年龄: {found_patient['age']}</p>
    <p style="color:#000000;">联系电话: {found_patient['phone']}</p>
</div>
""", unsafe_allow_html=True)
                    
                    # 挂号操作
                    st.subheader("快速挂号")
                    col2_1, col2_2 = st.columns(2)
                    with col2_1:
                        dept = st.selectbox("变更科室", ["内科", "外科", "儿科", "妇科", "神经科", "皮肤科", "眼科", "耳鼻喉科"], 
                                          index=["内科", "外科", "儿科", "妇科", "神经科", "皮肤科", "眼科", "耳鼻喉科"].index(found_patient["department"]))
                    with col2_2:
                        doctors = load_doctors()
                        dept_doctors = [doc for doc in doctors if doc["department"] == dept]
                        doctor_names = [f"{doc['name']} ({doc['specialty']})" for doc in dept_doctors]
                        doc_selection = st.selectbox("变更医生", doctor_names)
                    
                    if st.button("确认挂号"):
                        # 更新患者信息
                        for patient in patients:
                            if patient["id"] == found_patient["id"]:
                                patient["department"] = dept
                                doctor_name = doc_selection.split()[0]
                                doctor_id = next((doc["id"] for doc in doctors if doc["name"] == doctor_name), None)
                                patient["doctor_id"] = doctor_id
                                patient["appointment_date"] = datetime.now().strftime("%Y-%m-%d")
                                patient["registration_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                break
                        
                        save_patients(patients)
                        st.session_state.success_message = f"患者 {found_patient['name']} 挂号成功！"
                else:
                    st.session_state.error_message = "未找到患者，请先进行登记"
        
        st.markdown("""
        <div style="margin-top:20px;">
            <h4>今日挂号情况</h4>
        """, unsafe_allow_html=True)
        
        # 显示今日挂号人数统计
        patients = load_patients()
        today = datetime.now().strftime("%Y-%m-%d")
        today_patients = [p for p in patients if p.get("appointment_date") == today]
        
        departments = ["内科", "外科", "儿科", "妇科", "神经科", "皮肤科", "眼科", "耳鼻喉科"]
        dept_counts = {dept: len([p for p in today_patients if p.get("department") == dept]) for dept in departments}
        
        # 创建数据框并展示
        df = pd.DataFrame({
            "科室": list(dept_counts.keys()),
            "挂号人数": list(dept_counts.values())
        })
        
        st.dataframe(df, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# 医生诊断与处方页面
def diagnosis_page():
    st.title("医生诊断与处方")
    show_success_message()
    show_error_message()
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>患者查询</h3>
        """, unsafe_allow_html=True)
        
        search_option = st.selectbox("搜索方式", ["患者ID", "患者姓名"])
        search_value = st.text_input(f"请输入{search_option}")
        
        if st.button("查找患者"):
            if not search_value:
                st.session_state.error_message = "请输入搜索内容"
            else:
                patients = load_patients()
                found_patients = []
                
                if search_option == "患者ID":
                    try:
                        patient_id = int(search_value)
                        found_patient = next((p for p in patients if p.get("id") == patient_id), None)
                        if found_patient:
                            found_patients = [found_patient]
                    except ValueError:
                        st.session_state.error_message = "患者ID必须是数字"
                else:  # 患者姓名
                    found_patients = [p for p in patients if p.get("name") == search_value]
                
                if found_patients:
                    # 显示患者列表
                    st.session_state.found_patients = found_patients
                    st.markdown("<h4>搜索结果</h4>", unsafe_allow_html=True)
                    
                    for i, patient in enumerate(found_patients):
                        doctors = load_doctors()
                        doctor_name = next((doc["name"] for doc in doctors if doc["id"] == patient.get("doctor_id")), "未分配")
                        
                        st.markdown(f"""
                        <div style="background-color:#e6f3ff; padding:10px; border-radius:5px; margin-bottom:10px;">
                                
                            <p>ID: {patient['id']} | 姓名: {patient['name']} | 性别: {patient['gender']} | 年龄: {patient['age']}</p>
                            <p>科室: {patient['department']} | 医生: {doctor_name}</p>
                            <p>预约日期: {patient['appointment_date']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"选择患者 #{patient['id']}", key=f"select_patient_{i}"):
                            st.session_state.patient_id = patient['id']
                            st.session_state.success_message = f"已选择患者: {patient['name']}"
                            st.rerun()
                else:
                    st.session_state.error_message = "未找到患者"
        
        # 显示排队患者列表
        st.markdown("<h4>今日待诊患者</h4>", unsafe_allow_html=True)
        
        patients = load_patients()
        today = datetime.now().strftime("%Y-%m-%d")
        waiting_patients = [p for p in patients if p.get("appointment_date") == today and not any(pr.get("patient_id") == p["id"] for pr in load_prescriptions())]
        
        # 按优先级排序
        priority_order = {"急诊": 0, "优先": 1, "普通": 2}
        waiting_patients.sort(key=lambda p: priority_order.get(p.get("priority", "普通"), 3))
        
        if waiting_patients:
            for i, patient in enumerate(waiting_patients[:5]):  # 只显示前5个
                doctors = load_doctors()
                doctor_name = next((doc["name"] for doc in doctors if doc["id"] == patient.get("doctor_id")), "未分配")
                priority_color = {"急诊": "#ff6b6b", "优先": "#ffa94d", "普通": "#69db7c"}.get(patient.get("priority", "普通"), "#69db7c")
                
                st.markdown(f"""
            <div style="background-color:#f8f9fa; padding:10px; border-radius:5px; margin-bottom:5px; border-left:5px solid {priority_color}; color:#000000;">
            
                <p style="color:#000000;">ID: {patient['id']} | 姓名: {patient['name']} | 优先级: {patient.get('priority', '普通')}</p>
                <p style="color:#000000;">科室: {patient['department']} | 医生: {doctor_name}</p>
            </div>
            """, unsafe_allow_html=True)
                
                if st.button(f"开始诊断 #{patient['id']}", key=f"start_diagnosis_{i}"):
                    st.session_state.patient_id = patient['id']
                    st.session_state.success_message = f"已选择患者: {patient['name']}"
                    st.rerun()
        else:
            st.info("今日没有待诊患者")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>诊断与处方</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.patient_id:
            patients = load_patients()
            current_patient = next((p for p in patients if p.get("id") == st.session_state.patient_id), None)
            
            if current_patient:
                doctors = load_doctors()
                doctor_name = next((doc["name"] for doc in doctors if doc["id"] == current_patient.get("doctor_id")), "未分配")
                
                # 显示患者基本信息
                st.markdown(f"""
                <div style="background-color:#e6f3ff; padding:15px; border-radius:5px; margin-bottom:15px;">
                    <h4>患者信息</h4>
                    <p><strong>姓名:</strong> {current_patient['name']} &nbsp;&nbsp; <strong>性别:</strong> {current_patient['gender']} &nbsp;&nbsp; <strong>年龄:</strong> {current_patient['age']}</p>
                    <p><strong>科室:</strong> {current_patient['department']} &nbsp;&nbsp; <strong>医生:</strong> {doctor_name}</p>
                    <p><strong>病史:</strong> {current_patient.get('medical_history', '无')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 诊断表单
                st.subheader("诊断信息")
                
                vital_signs = st.text_area("生命体征", placeholder="例如: 体温:36.5℃, 血压:120/80mmHg, 心率:75次/分")
                symptoms = st.text_area("症状描述", placeholder="请描述患者主诉症状...")
                diagnosis = st.text_area("诊断结果", placeholder="医生诊断...")
                treatment_plan = st.text_area("治疗方案", placeholder="建议治疗方案...")
                
                st.subheader("开具处方")
                
                medications = []
                for i in range(3):  # 默认支持3种药品
                    col_m1, col_m2, col_m3 = st.columns([3, 1, 1])
                    with col_m1:
                        med_name = st.text_input(f"药品名称 #{i+1}", key=f"med_name_{i}")
                    with col_m2:
                        med_dosage = st.text_input(f"剂量 #{i+1}", key=f"med_dosage_{i}")
                    with col_m3:
                        med_days = st.number_input(f"天数 #{i+1}", min_value=0, max_value=30, step=1, key=f"med_days_{i}")
                    
                    if med_name:
                        medications.append({
                            "name": med_name,
                            "dosage": med_dosage,
                            "days": med_days,
                            "price": round(random.uniform(10, 200), 2)  # 模拟药品价格
                        })
                
                notes = st.text_area("医嘱", placeholder="用药注意事项...")
                
                next_visit = st.date_input("复诊日期", min_value=datetime.now().date() + timedelta(days=1))
                
                col_b1, col_b2 = st.columns(2)
                
                with col_b1:
                    if st.button("保存诊断记录", use_container_width=True):
                        if not diagnosis:
                            st.session_state.error_message = "请填写诊断结果"
                        else:
                            prescriptions = load_prescriptions()
                            
                            # 生成处方ID
                            prescription_id = random.randint(100000, 999999)
                            while any(pr.get("id") == prescription_id for pr in prescriptions):
                                prescription_id = random.randint(100000, 999999)
                            
                            # 创建新处方
                            new_prescription = {
                                "id": prescription_id,
                                "patient_id": current_patient["id"],
                                "patient_name": current_patient["name"],
                                "doctor_id": current_patient.get("doctor_id"),
                                "doctor_name": doctor_name,
                                "department": current_patient["department"],
                                "vital_signs": vital_signs,
                                "symptoms": symptoms,
                                "diagnosis": diagnosis,
                                "treatment_plan": treatment_plan,
                                "medications": medications,
                                "notes": notes,
                                "next_visit": next_visit.strftime("%Y-%m-%d"),
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "status": "待处理",
                                "payment_status": "未结算"
                            }
                            
                            prescriptions.append(new_prescription)
                            save_prescriptions(prescriptions)
                            
                            st.session_state.success_message = f"处方已保存，处方ID: {prescription_id}"
                            st.session_state.patient_id = None
                            st.rerun()
                
                with col_b2:
                    if st.button("取消", use_container_width=True):
                        st.session_state.patient_id = None
                        st.rerun()
            else:
                st.error("未找到患者信息")
        else:
            st.info("请先从左侧选择一名患者进行诊断")
        
        st.markdown("</div>", unsafe_allow_html=True)

# 药房配药与结算页面
def pharmacy_page():
    st.title("药房配药与结算")
    show_success_message()
    show_error_message()
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>处方查询</h3>
        """, unsafe_allow_html=True)
        
        search_option = st.selectbox("搜索方式", ["处方ID", "患者ID", "患者姓名"])
        search_value = st.text_input(f"请输入{search_option}")
        
        if st.button("查找处方"):
            if not search_value:
                st.session_state.error_message = "请输入搜索内容"
            else:
                prescriptions = load_prescriptions()
                found_prescriptions = []
                
                if search_option == "处方ID":
                    try:
                        prescription_id = int(search_value)
                        found_prescription = next((p for p in prescriptions if p.get("id") == prescription_id), None)
                        if found_prescription:
                            found_prescriptions = [found_prescription]
                    except ValueError:
                        st.session_state.error_message = "处方ID必须是数字"
                elif search_option == "患者ID":
                    try:
                        patient_id = int(search_value)
                        found_prescriptions = [p for p in prescriptions if p.get("patient_id") == patient_id]
                    except ValueError:
                        st.session_state.error_message = "患者ID必须是数字"
                else:  # 患者姓名
                    found_prescriptions = [p for p in prescriptions if p.get("patient_name") == search_value]
                
                if found_prescriptions:
                    # 显示处方列表
                    st.session_state.found_prescriptions = found_prescriptions
                    st.markdown("<h4>搜索结果</h4>", unsafe_allow_html=True)
                    
                    for i, prescription in enumerate(found_prescriptions):
                        status_color = {"待处理": "#ffa94d", "配药中": "#4dabf7", "已完成": "#69db7c", "已取消": "#868e96"}.get(prescription.get("status", "待处理"), "#ffa94d")
                        payment_color = {"未结算": "#ff6b6b", "已结算": "#69db7c"}.get(prescription.get("payment_status", "未结算"), "#ff6b6b")
                        
                        st.markdown(f"""
                        <div style="background-color:#f8f9fa; padding:10px; border-radius:5px; margin-bottom:10px; border-left:5px solid {status_color};">
                            <p>处方ID: {prescription['id']} | 患者: {prescription['patient_name']} (ID: {prescription['patient_id']})</p>
                            <p>开具医生: {prescription.get('doctor_name', '未知')} | 科室: {prescription.get('department', '未知')}</p>
                            <p>状态: <span style="color:{status_color};">{prescription.get('status', '待处理')}</span> | 
                               结算: <span style="color:{payment_color};">{prescription.get('payment_status', '未结算')}</span></p>
                            <p>开具时间: {prescription.get('created_at', '未知')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"处理处方 #{prescription['id']}", key=f"process_prescription_{i}"):
                            st.session_state.prescription_id = prescription['id']
                            st.session_state.success_message = f"已选择处方 #{prescription['id']}"
                            st.rerun()
                else:
                    st.session_state.error_message = "未找到处方"
        
        # 显示待处理处方列表
        st.markdown("<h4>待处理处方</h4>", unsafe_allow_html=True)
        
        prescriptions = load_prescriptions()
        pending_prescriptions = [p for p in prescriptions if p.get("status") == "待处理"]
        
        # 按创建时间排序
        pending_prescriptions.sort(key=lambda p: p.get("created_at", ""), reverse=True)
        
        if pending_prescriptions:
            for i, prescription in enumerate(pending_prescriptions[:5]):  # 只显示前5个
                st.markdown(f"""
                <div style="background-color:#f8f9fa; padding:10px; border-radius:5px; margin-bottom:5px; border-left:5px solid #ffa94d;">
                    <p>处方ID: {prescription['id']} | 患者: {prescription['patient_name']}</p>
                    <p>开具医生: {prescription.get('doctor_name', '未知')} | 科室: {prescription.get('department', '未知')}</p>
                    <p>开具时间: {prescription.get('created_at', '未知')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"处理 #{prescription['id']}", key=f"handle_prescription_{i}"):
                    st.session_state.prescription_id = prescription['id']
                    st.session_state.success_message = f"已选择处方 #{prescription['id']}"
                    st.rerun()
        else:
            st.info("没有待处理的处方")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>配药与结算</h3>
        """, unsafe_allow_html=True)
        
        if hasattr(st.session_state, 'prescription_id') and st.session_state.prescription_id:
            prescriptions = load_prescriptions()
            current_prescription = next((p for p in prescriptions if p.get("id") == st.session_state.prescription_id), None)
            
            if current_prescription:
                # 显示处方基本信息
                status_color = {"待处理": "#ffa94d", "配药中": "#4dabf7", "已完成": "#69db7c", "已取消": "#868e96"}.get(current_prescription.get("status", "待处理"), "#ffa94d")
                
                st.markdown(f"""
                <div style="background-color:#e6f3ff; padding:15px; border-radius:5px; margin-bottom:15px;">
                    <h4>处方信息 <span style="float:right; background-color:{status_color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.8em;">{current_prescription.get('status', '待处理')}</span></h4>
                    <p><strong>处方ID:</strong> {current_prescription['id']} &nbsp;&nbsp; <strong>开具时间:</strong> {current_prescription.get('created_at', '未知')}</p>
                    <p><strong>患者:</strong> {current_prescription['patient_name']} (ID: {current_prescription['patient_id']}) &nbsp;&nbsp; <strong>医生:</strong> {current_prescription.get('doctor_name', '未知')}</p>
                    <p><strong>诊断:</strong> {current_prescription.get('diagnosis', '无')}</p>
                    <p><strong>医嘱:</strong> {current_prescription.get('notes', '无')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 药品列表
                st.subheader("药品清单")
                
                medications = current_prescription.get("medications", [])
                if medications:
                    medication_df = pd.DataFrame(medications)
                    
                    # 为每种药品添加状态
                    if "medication_status" not in current_prescription:
                        current_prescription["medication_status"] = ["待准备"] * len(medications)
                    
                    # 显示药品表格
                    for i, med in enumerate(medications):
                        med_status = current_prescription["medication_status"][i] if i < len(current_prescription["medication_status"]) else "待准备"
                        status_options = ["待准备", "准备中", "已准备"]
                        
                        col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns([3, 1, 1, 1, 2])
                        with col_d1:
                            st.markdown(f"**{med['name']}**")
                        with col_d2:
                            st.markdown(f"{med['dosage']}")
                        with col_d3:
                            st.markdown(f"{med['days']}天")
                        with col_d4:
                            st.markdown(f"¥{med['price']}")
                        with col_d5:
                            new_status = st.selectbox("状态", status_options, status_options.index(med_status), key=f"med_status_{i}")
                            if new_status != med_status:
                                current_prescription["medication_status"][i] = new_status
                                # 更新处方
                                for idx, p in enumerate(prescriptions):
                                    if p.get("id") == current_prescription["id"]:
                                        prescriptions[idx] = current_prescription
                                        save_prescriptions(prescriptions)
                                        break
                    
                    # 计算总价
                    total_price = sum(med["price"] * med["days"] for med in medications)
                    st.markdown(f"<h3>总计: ¥{total_price:.2f}</h3>", unsafe_allow_html=True)
                    
# 主程序入口
def main():
    # 根据页面状态显示相应页面
    if st.session_state.page == 'registration':
        registration_page()
    elif st.session_state.page == 'diagnosis':
        diagnosis_page()
    elif st.session_state.page == 'pharmacy':
        pharmacy_page()

if __name__ == "__main__":
    main()