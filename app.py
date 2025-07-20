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

# === Penjelasan IPA & Parameter ===
with st.expander("📘 Penjelasan Lengkap Tentang Indeks Pencemaran Air dan Parameternya"):
    st.markdown("""
    <div style='color:white'>
    <b>Indeks Pencemaran Air (IPA)</b> adalah suatu metode kuantitatif untuk menilai tingkat pencemaran suatu badan air berdasarkan parameter kualitas air yang diukur dan dibandingkan dengan baku mutu tertentu.
    
    Berikut penjelasan singkat tiap parameter:
    - <b>pH</b>: Rentang ideal 6–9. Di luar ini berbahaya bagi makhluk hidup dan mempercepat korosi.
    - <b>Suhu</b>: Kenaikan maksimal ±3°C dari suhu alami.
    - <b>DO</b> (Oksigen Terlarut): Ideal ≥ 4 mg/L. Kurang dari itu mengindikasikan pencemaran organik.
    - <b>BOD</b>: Ideal ≤ 3 mg/L. Mewakili jumlah oksigen yang dibutuhkan mikroba untuk menguraikan bahan organik.
    - <b>COD</b>: Ideal ≤ 25 mg/L. Mewakili pencemar organik dan anorganik.
    - <b>TDS</b>: Ideal ≤ 1000 mg/L. Terlalu tinggi bisa membahayakan organisme air.
    - <b>TSS</b>: Ideal ≤ 50 mg/L. Menunjukkan kekeruhan air.
    - <b>E-Coli</b>: Ideal ≤ 1000 MPN/100mL. Tanda pencemaran feses manusia/hewan.
    - <b>Logam Berat</b>: Harus di bawah ambang batas tertentu (lihat input logam berat).
    </div>
    """, unsafe_allow_html=True)

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
    # Cek apakah semua nilai default (tidak diisi)
    input_dasar = [ph, suhu, do, bod, cod, tss, tds, ecoli]
    if all(v == 0 for v in input_dasar) and not kadar_logam_input:
        st.warning("⚠ Silakan isi parameter kualitas air terlebih dahulu untuk melihat hasil analisis.")
    else:
        pelanggaran = 0
        catatan = []

        if ph < 6.5 or ph > 8.5:
            pelanggaran += 1
            catatan.append("pH di luar rentang aman (6.5 - 8.5)")
        if suhu > 30:
            pelanggaran += 1
            catatan.append("Suhu naik > 3°C dari alami")
        if do < 4:
            pelanggaran += 1
            catatan.append("DO < 4 mg/L")
        if bod > 3:
            pelanggaran += 1
            catatan.append("BOD > 3 mg/L")
        if cod > 25:
            pelanggaran += 1
            catatan.append("COD > 25 mg/L")
        if tss > 50:
            pelanggaran += 1
            catatan.append("TSS > 50 mg/L")
        if tds > 1000:
            pelanggaran += 1
            catatan.append("TDS > 1000 mg/L")
        if ecoli > 1000:
            pelanggaran += 1
            catatan.append("E-Coli melebihi batas aman (>1000 MPN/100mL)")

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
