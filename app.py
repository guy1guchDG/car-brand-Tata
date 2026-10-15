import joblib
import streamlit as st
import pandas as pd

# โหลดโมเดลและตั้งค่าหน้าเว็บ
pipeline = joblib.load("./pipeline_car_rf.joblib")
st.set_page_config(page_title="TATA MOTORS - Smart Value Estimator", layout="wide")

# ฟังก์ชันทำนายราคา (คง Logic การเช็ค Error และ Warning เดิมไว้ทั้งหมด)
def predict_resale_price(model_name, variant, body_type, car_age, ex_showroom_price_lakh,
                         engine_cc, power_bhp, mileage_kmpl, fuel_type, transmission,
                         kilometers_driven, owner_count, accident_history):
    
    valid_fuels = ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
    if fuel_type not in valid_fuels:
        return f"❌ Error: ไม่รู้จักเชื้อเพลิง '{fuel_type}' (กรุณาระบุตัวสะกดให้ตรงเช่น Petrol, Diesel)"
        
    valid_transmissions = ["Manual", "Automatic"]
    if transmission not in valid_transmissions:
        return f"❌ Error: ไม่รู้จักเกียร์ '{transmission}' (กรุณาระบุ Manual หรือ Automatic)"

    features = {
        'engine_cc': engine_cc,
        'power_bhp': power_bhp,
        'mileage_kmpl': mileage_kmpl,
        'ex_showroom_price_lakh': ex_showroom_price_lakh,
        'car_age': car_age,
        'kilometers_driven': kilometers_driven,
        'owner_count': owner_count,
        'accident_history': accident_history,
        'model': model_name,
        'variant': variant,
        'fuel_type': fuel_type,
        'transmission': transmission,
        'body_type': body_type
    }
    input_df = pd.DataFrame([features])
    
    prediction = pipeline.predict(input_df)[0]
    
    warning = ""
    if car_age >= 20 or kilometers_driven >= 500000:
        warning = " | ⚠️ คำเตือน: สภาพรถอยู่นอกเหนือช่วงข้อมูลปกติ โมเดลอาจประเมินราคาสูงกว่าความเป็นจริง"
        
    return f"₹ {prediction:,.2f} Lakh{warning}"

# กำหนดค่าเริ่มต้นใน Session State (เพื่อให้ปุ่ม Examples กดแล้วเปลี่ยนค่าในช่อง Input ได้ทันที)
default_values = {
    "in_model": "Nexon",
    "in_variant": "XZA Plus",
    "in_body": "SUV",
    "in_age": 3,
    "in_ex_price": 8.5,
    "in_engine": 1199,
    "in_power": 118,
    "in_mileage": 17.5,
    "in_fuel": "Petrol",
    "in_trans": "Automatic",
    "in_km": 35000,
    "in_owner": 1,
    "in_accident": 0
}

for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

def set_example(model_name, variant, body_type, age, ex_price, engine, power, mileage, fuel, trans, km, owner, accident):
    st.session_state.in_model = model_name
    st.session_state.in_variant = variant
    st.session_state.in_body = body_type
    st.session_state.in_age = age
    st.session_state.in_ex_price = float(ex_price)
    st.session_state.in_engine = engine
    st.session_state.in_power = power
    st.session_state.in_mileage = float(mileage)
    st.session_state.in_fuel = fuel
    st.session_state.in_trans = trans
    st.session_state.in_km = km
    st.session_state.in_owner = owner
    st.session_state.in_accident = accident

# ส่วนหัว (Header Banner)
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #0b1c3c 0%, #1a365d 100%); border-radius: 12px; margin-bottom: 25px; box-shadow: 0 8px 16px rgba(0,0,0,0.15); color: white;'>
    <h1 style='font-size: 3em; margin-bottom: 0px; color: #ffffff; font-weight: 800; letter-spacing: 2px;'>TATA MOTORS</h1>
    <h2 style='font-size: 1.5em; margin-bottom: 10px; color: #60a5fa; font-weight: 500;'>Smart Value Estimator</h2>
    <p style='font-size: 1.1em; color: #cbd5e1; font-weight: 300;'>ระบบประเมินราคารถยนต์อัจฉริยะ</p>
</div>
""", unsafe_allow_html=True)

# แบ่งหน้าจอเป็น 3 คอลัมน์
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚙 ข้อมูลรถยนต์พื้นฐาน")
    in_model = st.text_input("รุ่นรถ (Model)", key="in_model", placeholder="เช่น Nexon, Safari, Tiago")
    in_variant = st.text_input("รุ่นย่อย (Variant)", key="in_variant", placeholder="เช่น XZA Plus, XT")
    in_body = st.text_input("ประเภทตัวถัง (Body Type)", key="in_body", placeholder="เช่น SUV, Hatchback")
    in_age = st.number_input("อายุการใช้งาน (ปี)", min_value=0, max_value=100, step=1, key="in_age")
    in_ex_price = st.number_input("ราคามือหนึ่ง (Lakh)", min_value=0.0, max_value=100.0, step=0.5, key="in_ex_price")

with col2:
    st.markdown("### ⚙️ สเปกและเครื่องยนต์")
    in_fuel = st.text_input("เชื้อเพลิง (Fuel Type)", key="in_fuel", placeholder="Petrol / Diesel / CNG")
    in_trans = st.text_input("เกียร์ (Transmission)", key="in_trans", placeholder="Manual / Automatic")
    in_engine = st.number_input("ขนาดเครื่องยนต์ (CC)", min_value=0, max_value=10000, step=50, key="in_engine")
    in_power = st.number_input("แรงม้า (BHP)", min_value=0, max_value=1000, step=5, key="in_power")
    in_mileage = st.number_input("อัตราสิ้นเปลือง (km/l)", min_value=0.0, max_value=100.0, step=0.5, key="in_mileage")

with col3:
    st.markdown("### 🛣️ ประวัติการใช้งาน")
    in_km = st.number_input("เลขไมล์ (km)", min_value=0, max_value=5000000, step=1000, key="in_km")
    in_owner = st.number_input("จำนวนเจ้าของก่อนหน้า", min_value=0, max_value=20, step=1, key="in_owner")
    in_accident = st.number_input("ประวัติชน (0 = ไม่มี, 1 = มี)", min_value=0, max_value=1, step=1, key="in_accident")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏁 คำนวณราคาประเมิน", type="primary", use_container_width=True):
        price = predict_resale_price(
            in_model, in_variant, in_body, in_age, in_ex_price,
            in_engine, in_power, in_mileage, in_fuel, in_trans,
            in_km, in_owner, in_accident
        )
        st.session_state.predicted_price = price

    # แสดงผลลัพธ์ตามรูปแบบไฟล์ตัวอย่าง
    if "predicted_price" in st.session_state:
        st.text_input("💰 ราคาขายต่อที่คาดการณ์", value=st.session_state.predicted_price, disabled=True)

st.markdown("---")

# ส่วนของปุ่มกดโหลดเคสตัวอย่าง (แทนที่ gr.Examples)
st.markdown("### ✅ กรณีปกติ (Normal Cases): ทำนายแม่นยำ สมเหตุสมผล")
st.caption("คลิกปุ่มด้านล่างเพื่อโหลดข้อมูลตัวอย่างลงในช่องกรอกอัตโนมัติ แล้วกดคำนวณราคาประเมิน")
ex_col1, ex_col2, ex_col3 = st.columns(3)
with ex_col1:
    st.button("🚗 Case 1: Tiago XZ (5 ปี, Petrol)", use_container_width=True,
              on_click=set_example, args=("Tiago", "XZ", "Hatchback", 5, 6.0, 1199, 84, 20.0, "Petrol", "Manual", 60000, 2, 0))
with ex_col2:
    st.button("🚙 Case 2: Nexon XZA Plus (3 ปี, Petrol)", use_container_width=True,
              on_click=set_example, args=("Nexon", "XZA Plus", "SUV", 3, 11.5, 1199, 118, 17.5, "Petrol", "Automatic", 35000, 1, 0))
with ex_col3:
    st.button("🚘 Case 3: Safari XZA Plus (2 ปี, Diesel)", use_container_width=True,
              on_click=set_example, args=("Safari", "XZA Plus", "SUV", 2, 23.0, 1956, 168, 14.0, "Diesel", "Automatic", 20000, 1, 0))

st.markdown("### ⚠️ กรณีข้อจำกัดของระบบ (Edge/Error Cases): ทำนายคลาดเคลื่อน")
err_col1, err_col2 = st.columns(2)
with err_col1:
    st.button("❌ Error Case: พิมพ์ชื่อเชื้อเพลิงผิด ('Patrol')", use_container_width=True,
              on_click=set_example, args=("Nexon", "XZA Plus", "SUV", 3, 11.5, 1199, 118, 17.5, "Patrol", "Automatic", 35000, 1, 0))
with err_col2:
    st.button("⚠️ Edge Case: รถเก่า 50 ปี / ไมล์ 2 ล้านกม. (Altroz)", use_container_width=True,
              on_click=set_example, args=("Altroz", "XE", "Hatchback", 50, 7.0, 1199, 85, 19.0, "Petrol", "Manual", 2000000, 5, 1))
