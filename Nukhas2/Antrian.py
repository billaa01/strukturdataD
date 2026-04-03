import streamlit as st

# Inisialisasi state untuk menyimpan queue jika belum ada
if 'queue' not in st.session_state:
    st.session_state.size = 8
    st.session_state.queue = [None] * st.session_state.size
    st.session_state.head = -1
    st.session_state.tail = -1

def enqueue(data):
    size = st.session_state.size
    # Cek apakah queue penuh
    if ((st.session_state.tail + 1) % size == st.session_state.head):
        st.error("Queue Penuh!")
    else:
        if (st.session_state.head == -1):
            st.session_state.head = 0
        
        st.session_state.tail = (st.session_state.tail + 1) % size
        st.session_state.queue[st.session_state.tail] = data
        st.success(f"Berhasil menambahkan: {data}")

def dequeue():
    size = st.session_state.size
    # Cek apakah queue kosong
    if (st.session_state.head == -1):
        st.error("Queue Kosong!")
    else:
        removed_data = st.session_state.queue[st.session_state.head]
        st.session_state.queue[st.session_state.head] = None
        
        if (st.session_state.head == st.session_state.tail):
            st.session_state.head = -1
            st.session_state.tail = -1
        else:
            st.session_state.head = (st.session_state.head + 1) % size
        st.warning(f"Berhasil menghapus: {removed_data}")

# --- UI Streamlit ---
st.title("🎡 Visualisasi Circular Queue")
st.write("Implementasi konsep *wrap-around* secara interaktif.")

# Sidebar untuk Kontrol
with st.sidebar:
    st.header("Kontrol Antrian")
    new_item = st.text_input("Input Data")
    if st.button("Enqueue (Tambah)"):
        if new_item:
            enqueue(new_item)
    
    if st.button("Dequeue (Hapus)"):
        dequeue()
    
    if st.button("Reset Queue"):
        st.session_state.queue = [None] * st.session_state.size
        st.session_state.head = -1
        st.session_state.tail = -1
        st.rerun()

# Visualisasi Utama
cols = st.columns(st.session_state.size)

for i in range(st.session_state.size):
    with cols[i]:
        label = ""
        if i == st.session_state.head: label += "🏁 Head"
        if i == st.session_state.tail: label += "\n 🔚 Tail"
        
        # Beri warna beda kalau ada isinya
        box_color = "primary" if st.session_state.queue[i] is not None else "secondary"
        
        st.metric(label=f"Index {i}", value=st.session_state.queue[i] if st.session_state.queue[i] else "-")
        st.caption(label)

# Info Status
st.divider()
st.write(f"**Head Index:** {st.session_state.head} | **Tail Index:** {st.session_state.tail}")