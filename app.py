import streamlit as st
import base64

# === Background Gambar ===
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Pasang background
set_background("turtle.jpg")

# === Judul Aplikasi ===
st.markdown("<h1 style='text-align:center; color:white;'>💧 Indeks Pencemaran Air</h1>", unsafe_allow_html=True)

# === Penjelasan Umum IPA ===
with st.expander("📘 Apa itu Indeks Pencemaran Air (IPA)?"):
    st.markdown("""
    <div style='color:white'>
    Indeks Pencemaran Air (IPA) adalah suatu metode kuantitatif untuk menilai tingkat pencemaran suatu badan air
    berdasarkan parameter kualitas air yang diukur dan dibandingkan dengan baku mutu yang ditetapkan
    untuk peruntukan tertentu.
    </div>
    """, unsafe_allow_html=True)

# === Penjelasan Parameter ===
params_info = {
    "pH": "Menunjukkan tingkat keasaman atau kebasaan air. Rentang ideal: 6–9. Di luar rentang ini bisa mengganggu kehidupan akuatik dan mempercepat korosi atau reaksi kimia tertentu.",
    "Suhu": "Mempengaruhi kelarutan oksigen dan aktivitas biologis. Suhu tinggi menurunkan kadar oksigen terlarut dan mempercepat reaksi kimia. Deviasi ±3°C dari suhu alami dianggap aman.",
    "DO (Oksigen Terlarut)": "Kandungan oksigen yang tersedia dalam air untuk makhluk hidup. Nilai ideal: ≥4 mg/L. DO rendah menandakan pencemaran organik tinggi dan bisa menyebabkan kematian biota.",
    "BOD": "Jumlah oksigen yang dibutuhkan mikroorganisme untuk mengurai bahan organik. Semakin tinggi BOD, semakin tercemar airnya. Baku mutu: ≤3 mg/L untuk kelas II.",
    "COD": "Jumlah oksigen yang dibutuhkan untuk mengoksidasi semua bahan organik. COD tinggi menunjukkan pencemaran berat. Baku mutu: ≤25 mg/L untuk kelas II.",
    "TDS": "Menunjukkan jumlah zat terlarut (garam, mineral, logam). Nilai tinggi bisa mengganggu osmoregulasi organisme air. Baku mutu: ≤1000 mg/L.",
    "TSS": "Padatan tersuspensi seperti lumpur, tanah liat, ganggang. TSS tinggi menyebabkan kekeruhan dan menghambat fotosintesis. Baku mutu: ≤50 mg/L.",
    "Logam Berat": "Logam berat adalah unsur logam dengan massa jenis tinggi (>5 g/cm³) yang bersifat toksik bagi organisme hidup jika melebihi ambang batas.",
    "E-Coli": "Indikator pencemaran biologis dari limbah manusia/hewan. Baku mutu: ≤1000 MPN/100 mL untuk kelas II. Nilai tinggi menunjukkan risiko penyakit seperti diare dan disentri."
}

for param, desc in params_info.items():
    with st.expander(f"🔎 Penjelasan Parameter: {param}"):
        st.markdown(f"<div style='color:white'>{desc}</div>", unsafe_allow_html=True)

# === Ambang batas logam berat ===
ambang_logam = {
    "Arsen (As)": 0.01, "Kadmium (Cd)": 0.003, "Kromium (Cr)": 0.05, "Raksa (Hg)": 0.001,
    "Timbal (Pb)": 0.01, "Selenium (Se)": 0.02, "Antimon (Sb)": 0.02, "Barium (Ba)": 0.7,
    "Boron (B)": 0.5, "Besi (Fe)": 0.3, "Mangan (Mn)": 0.1, "Nikel (Ni)": 0.07,
    "Tembaga (Cu)": 2.0, "Seng (Zn)": 3.0, "Aluminium (Al)": 0.2
}

# === Input Form ===
with st.form("form_input"):
    st.markdown("### 🔍 Masukkan Parameter Kualitas Air")
    col1, col2 = st.columns(2)
    with col1:
        ph = st.number_input("pH", 0.0, 14.0, step=0.1, format="%.1f")
        suhu = st.number_input("Suhu (°C)", step=0.1, format="%.1f")
        do = st.number_input("Oksigen Terlarut / DO (mg/L)", step=0.1, format="%.1f")
        bod = st.number_input("BOD (mg/L)", step=0.1, format="%.1f")
        tds = st.number_input("TDS (mg/L)", step=1.0, format="%.1f")
    with col2:
        cod = st.number_input("COD (mg/L)", step=0.1, format="%.1f")
        tss = st.number_input("TSS (mg/L)", step=0.1, format="%.1f")
        ecoli = st.number_input("E-Coli (Jumlah/100mL)", step=1.0, format="%.1f")

    # Logam berat (opsional)
    selected_logam = st.multiselect("Pilih Jenis Logam Berat yang Terdeteksi (Opsional)", list(ambang_logam.keys()))
    kadar_logam_input = {}
    if selected_logam:
        st.markdown("### 💡 Nilai Kadar Logam Berat:")
        for logam in selected_logam:
            kadar = st.number_input(f"Kadar {logam} (mg/L)", step=0.001, format="%.3f", key=logam)
            kadar_logam_input[logam] = (kadar, ambang_logam[logam])

    submit = st.form_submit_button("🔬 Lanjutkan Analisis Kualitas Air")

# === Analisis ===
if submit:
    pelanggaran = 0
    catatan = []

    if ph < 6.5 or ph > 8.5:
        pelanggaran += 1
        catatan.append("pH di luar rentang aman (6.5 - 8.5)")
    if suhu > 30:
        pelanggaran += 1
        catatan.append("Suhu naik > 3°C dari alami")
    if do < 5:
        pelanggaran += 1
        catatan.append("DO < 5 mg/L")
    if bod > 3:
        pelanggaran += 1
        catatan.append("BOD > 3 mg/L")
    if cod > 10:
        pelanggaran += 1
        catatan.append("COD > 10 mg/L")
    if tss > 50:
        pelanggaran += 1
        catatan.append("TSS > 50 mg/L")
    if tds > 500:
        pelanggaran += 1
        catatan.append("TDS > 500 mg/L")
    if ecoli > 0:
        pelanggaran += 1
        catatan.append("E-Coli terdeteksi")

    for logam, (nilai, ambang) in kadar_logam_input.items():
        if nilai > ambang:
            pelanggaran += 1
            catatan.append(f"{logam} melebihi ambang batas ({nilai} > {ambang})")

    if pelanggaran == 0:
        status, color = "💚 Baik", "rgba(46, 204, 113, 0.75)"
    elif pelanggaran <= 2:
        status, color = "🟡 Sedang", "rgba(244, 208, 63, 0.75)"
    elif pelanggaran <= 4:
        status, color = "🟠 Tercemar", "rgba(230, 126, 34, 0.75)"
    else:
        status, color = "🔴 Sangat Tercemar", "rgba(231, 76, 60, 0.75)"

    st.markdown(f"""
    <div style="padding:20px; background-color:{color}; border-radius:12px;">
        <h3 style="color:white;">Status Kualitas Air: {status}</h3>
        <ul style="color:white;">
            {''.join(f"<li>{c}</li>" for c in catatan)}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# === Footer ===
st.markdown("""
<hr style="border:0.5px solid white">
<p style="text-align:center; color:lightgrey;">
    Disusun oleh Kelompok 11 Logika dan Pemrograman Komputer
</p>
""", unsafe_allow_html=True)
