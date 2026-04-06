import streamlit as st

# Inisialisasi State untuk Circular Queue
if 'size' not in st.session_state:
    st.session_state.size = 5
    st.session_state.queue = [None] * st.session_state.size
    st.session_state.front = -1
    st.session_state.rear = -1

def enqueue(data):
    size = st.session_state.size
    # Cek apakah penuh
    if ((st.session_state.rear + 1) % size == st.session_state.front):
        st.error("Antrian Penuh (Queue Full)!")
    else:
        if st.session_state.front == -1:
            st.session_state.front = 0
        
        st.session_state.rear = (st.session_state.rear + 1) % size
        st.session_state.queue[st.session_state.rear] = data
        st.success(f"Berhasil menambahkan: {data}")

def dequeue():
    size = st.session_state.size
    # Cek apakah kosong
    if st.session_state.front == -1:
        st.error("Antrian Kosong (Queue Empty)!")
    else:
        removed_data = st.session_state.queue[st.session_state.front]
        st.session_state.queue[st.session_state.front] = None
        
        if st.session_state.front == st.session_state.rear:
            st.session_state.front = -1
            st.session_state.rear = -1
        else:
            st.session_state.front = (st.session_state.front + 1) % size
        st.warning(f"Berhasil menghapus: {removed_data}")

# --- UI Streamlit ---
st.title("🎡 Visualisasi Circular Queue")
st.write("Representasi struktur data antrian melingkar (Circular Buffer).")

# Sidebar Kontrol
with st.sidebar:
    st.header("Kontrol Antrian")
    input_data = st.text_input("Input Data", placeholder="Ketik sesuatu...")
    
    col1, col2 = st.columns(2)
    if col1.button("Enqueue", use_container_width=True):
        if input_data:
            enqueue(input_data)
        else:
            st.info("Masukkan data terlebih dahulu.")
            
    if col2.button("Dequeue", use_container_width=True):
        dequeue()

    if st.button("Reset Queue"):
        st.session_state.queue = [None] * st.session_state.size
        st.session_state.front = -1
        st.session_state.rear = -1
        st.rerun()

# --- Visualisasi ---
st.write("### Status Array Saat Ini")
cols = st.columns(st.session_state.size)

for i in range(st.session_state.size):
    with cols[i]:
        val = st.session_state.queue[i]
        color = "lightgray"
        label = ""
        
        # Logika penentuan label Front/Rear
        labels = []
        if i == st.session_state.front:
            labels.append("FRONT")
            color = "#ff4b4b" # Merah
        if i == st.session_state.rear:
            labels.append("REAR")
            color = "#1f77b4" # Biru
            
        if i == st.session_state.front and i == st.session_state.rear and st.session_state.front != -1:
            color = "#9b59b6" # Ungu jika keduanya di satu tempat

        # Box Visual
        st.markdown(
            f"""
            <div style="
                border: 2px solid {color};
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                background-color: {color if val else 'transparent'};
                color: {'white' if val else 'gray'};
                min-height: 80px;
            ">
                <small>Index {i}</small><br>
                <strong>{val if val else '-'}</strong>
            </div>
            <div style="text-align: center; font-size: 10px; font-weight: bold; margin-top: 5px;">
                {' & '.join(labels)}
            </div>
            """,
            unsafe_allow_html=True
        )

st.divider()

# Info Teknis
st.info(f"""
**Info Pointer:**
- **Front Index:** `{st.session_state.front}`
- **Rear Index:** `{st.session_state.rear}`
- **Formula Next Rear:** `(rear + 1) % {st.session_state.size}`
""")