import streamlit as st
import time

# ─────────────────────────────────────────
#  CIRCULAR LINKED LIST
# ─────────────────────────────────────────

class Node:
    """Satu simpul dalam circular linked list."""
    def __init__(self, warna: str, durasi: int, hex_color: str):
        self.warna = warna        # nama lampu
        self.durasi = durasi      # durasi (detik)
        self.hex_color = hex_color
        self.next: "Node | None" = None


class CircularLinkedList:
    """Circular linked list untuk siklus lampu lalu lintas."""

    def __init__(self):
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def append(self, warna: str, durasi: int, hex_color: str) -> None:
        node = Node(warna, durasi, hex_color)
        if self.head is None:
            self.head = node
            self.tail = node
            node.next = node          # tunjuk ke diri sendiri
        else:
            self.tail.next = node
            self.tail = node
            self.tail.next = self.head  # tutup lingkaran

        self.size += 1

    def traverse(self):
        """Generator: iterasi node tanpa henti (circular)."""
        current = self.head
        while True:
            yield current
            current = current.next


# ─────────────────────────────────────────
#  BANGUN LINKED LIST
# ─────────────────────────────────────────

def build_traffic_list() -> CircularLinkedList:
    cll = CircularLinkedList()
    cll.append("Merah",  40, "#FF3B3B")
    cll.append("Hijau",  20, "#2ECC71")
    cll.append("Kuning",  5, "#F1C40F")
    return cll


# ─────────────────────────────────────────
#  STREAMLIT UI
# ─────────────────────────────────────────

st.set_page_config(page_title="Traffic Light — Circular Linked List", page_icon="🚦")

st.title("🚦 Visualisasi Lampu Merah")
st.caption("Implementasi **Circular Linked List** · Struktur Data")

# Sidebar: info struktur
with st.sidebar:
    st.header("📋 Circular Linked List")
    cll_info = build_traffic_list()
    st.markdown("Urutan node (melingkar):")
    current = cll_info.head
    for _ in range(cll_info.size):
        st.markdown(
            f"🔵 **{current.warna}** → {current.durasi} detik  \n"
            f"`next →` {current.next.warna}"
        )
        current = current.next
    st.markdown("---")
    st.info("Setelah **Kuning**, `next` kembali ke **Merah** ♻️")

# Kolom utama
col_lampu, col_info = st.columns([1, 1])

with col_lampu:
    st.subheader("Lampu Aktif")
    lampu_placeholder = st.empty()

with col_info:
    st.subheader("Status")
    status_placeholder = st.empty()
    progress_placeholder = st.empty()
    countdown_placeholder = st.empty()

# ─────────────────────────────────────────
#  STATE & KONTROL
# ─────────────────────────────────────────

if "running" not in st.session_state:
    st.session_state.running = False
if "node_index" not in st.session_state:
    st.session_state.node_index = 0          # indeks node aktif
if "sisa_detik" not in st.session_state:
    st.session_state.sisa_detik = None
if "siklus" not in st.session_state:
    st.session_state.siklus = 0

col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    if st.button("▶️ Mulai", use_container_width=True):
        st.session_state.running = True
with col_btn2:
    if st.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False
with col_btn3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.running = False
        st.session_state.node_index = 0
        st.session_state.sisa_detik = None
        st.session_state.siklus = 0
        st.rerun()

st.markdown("---")
st.caption(f"🔁 Siklus selesai: **{st.session_state.siklus}**")

# ─────────────────────────────────────────
#  HELPER: tampilkan satu frame
# ─────────────────────────────────────────

def render_frame(node: Node, sisa: int):
    r, g, y = (
        node.hex_color if node.warna == "Merah"  else "#333",
        node.hex_color if node.warna == "Hijau"  else "#333",
        node.hex_color if node.warna == "Kuning" else "#333",
    )
    lampu_placeholder.markdown(
        f"""
        <div style="
            display:flex; flex-direction:column; align-items:center;
            background:#1a1a1a; border-radius:20px; padding:20px; width:120px; margin:auto;
        ">
            <div style="width:80px;height:80px;border-radius:50%;background:{r};
                        box-shadow:{'0 0 30px ' + r if node.warna=='Merah' else 'none'};
                        margin-bottom:10px;"></div>
            <div style="width:80px;height:80px;border-radius:50%;background:{g};
                        box-shadow:{'0 0 30px ' + g if node.warna=='Hijau' else 'none'};
                        margin-bottom:10px;"></div>
            <div style="width:80px;height:80px;border-radius:50%;background:{y};
                        box-shadow:{'0 0 30px ' + y if node.warna=='Kuning' else 'none'};
                        "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    status_placeholder.markdown(
        f"### {node.warna.upper()}\n"
        f"Durasi total: **{node.durasi} detik**"
    )

    persen = int(((node.durasi - sisa) / node.durasi) * 100)
    progress_placeholder.progress(persen, text=f"Progress: {persen}%")
    countdown_placeholder.metric("⏱️ Sisa Waktu", f"{sisa} detik")


# ─────────────────────────────────────────
#  LOOP UTAMA
# ─────────────────────────────────────────

# Bangun list & ambil node sesuai indeks
cll = build_traffic_list()
nodes = []
cur = cll.head
for _ in range(cll.size):
    nodes.append(cur)
    cur = cur.next

node_aktif: Node = nodes[st.session_state.node_index % cll.size]

# Inisialisasi sisa detik pertama kali
if st.session_state.sisa_detik is None:
    st.session_state.sisa_detik = node_aktif.durasi

render_frame(node_aktif, st.session_state.sisa_detik)

if st.session_state.running:
    time.sleep(1)
    st.session_state.sisa_detik -= 1

    if st.session_state.sisa_detik <= 0:
        # Pindah ke node berikutnya (circular)
        st.session_state.node_index = (st.session_state.node_index + 1) % cll.size
        if st.session_state.node_index == 0:
            st.session_state.siklus += 1
        next_node = nodes[st.session_state.node_index]
        st.session_state.sisa_detik = next_node.durasi

    st.rerun()