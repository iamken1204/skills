"""Reference build: what the vendor provides (purple) versus what the customer prepares (green).

Shows ownership zones, count badges, numbered install steps on wires, a vertical
fan-out, three repeated worker units on one pitch, a legend, and item and step cards.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from diagram_kit import Diagram, items_card, steps_card, write_page  # noqa: E402

UNIT_PITCH = 372         # horizontal distance between the three worker units
UNIT_X = 424
UNIT_Y = 314
TARGET_Y = 500

d = Diagram(1560, 656, description=(
    "The vendor provides and installs two installers on the customer's internal network. The "
    "Orchestrator is installed on one Linux server; the Worker on three Windows PCs. Each PC drives a "
    "remote KVM that is cabled to a target device. Operators use the Orchestrator web page from their "
    "own PC.",
    "廠商提供兩個安裝檔，並在客戶內網安裝。Orchestrator 裝在一台 Linux 伺服器，Worker 裝在三台 "
    "Windows PC。每台 PC 操作一台遠端 KVM，KVM 用線接到目標裝置。操作人員從自己的電腦開 Orchestrator 網頁。",
))

d.zone(24, 64, 296, 568, ("Vendor provides", "廠商提供"), tone="vendor")
d.zone(400, 64, 1136, 568, ("Customer prepares", "客戶準備"), tone="customer",
       note=("all on one internal network, each device able to reach the others",
             "全部在同一個內網，裝置之間互相連得到"))

server_installer = d.box(40, 128, 264, 80, ("Orchestrator installer", "Orchestrator 安裝包"),
                         subtitle=("the vendor installs it on the server", "由廠商安裝到伺服器"),
                         tone="vendor")
worker_installer = d.box(40, 352, 264, 80, ("Worker installer", "Worker 安裝檔"),
                         subtitle=("the vendor installs it on the 3 PCs", "由廠商安裝到 3 台 PC"),
                         tone="vendor")

operator = d.box(424, 128, 208, 64, ("Operator PC", "操作人員電腦"), subtitle=("Chrome or Edge", "Chrome 或 Edge"),
                 tone="customer", icon="person", title_size=14, qty="×1")
server = d.box(760, 104, 752, 120, ("Linux server", "Linux 伺服器"), tone="customer")
d.text(1448, 131, ("x86-64 · 2 CPU · 16 GB RAM · 60 GB disk", "x86-64 · 2 CPU · 16 GB RAM · 60 GB 硬碟"),
       "s", anchor="end")
d.qty(1460, 112, "×1")
d.chip(776, 146, 720, 62, "Orchestrator", subtitle=("installed by the vendor", "由廠商安裝"))
d.wire([(operator.right, 160), (server.left, 160)], label=("web page", "網頁"), muted_label=True)

d.wire([(server_installer.right, 168), (380, 168), (380, 256), (800, 256), (800, server.bottom)],
       origin_dot=True)
d.step(452, 256, 1, label=("install the Orchestrator", "安裝 Orchestrator"))

units = []
for index in range(3):
    x = UNIT_X + index * UNIT_PITCH
    first = index == 0
    unit = d.box(x, UNIT_Y, 344, 128,
                 ("All-in-one box", "一體機") if first else ("Existing PC + KVM", "現有的 PC + KVM"),
                 tone="customer", title_size=14, filled=first, dashed=not first, thick=first,
                 qty="×1" if first else None)
    pc = d.box(x + 16, UNIT_Y + 40, 168, 72, "Windows PC", tone="neutral" if first else "customer",
               title_size=14)
    d.chip(pc.x + 12, pc.y + 34, 144, 28, "Worker", solid=True, size=13)
    kvm = d.box(x + 228, UNIT_Y + 40, 100, 72, "KVM", tone="neutral" if first else "customer",
                title_size=14)
    if not first:
        d.qty(pc.right - 44, pc.y + 6, "×1")
        d.qty(kvm.x + 12, kvm.y + 36, "×1")
    d.wire([(pc.right, kvm.y + 52), (kvm.left, kvm.y + 52)])
    target = d.box(x + 120, TARGET_Y, 208, 64, ("Target device", "目標裝置"),
                   subtitle=("the robot operates it", "機器人操作的機器"), tone="customer", title_size=14,
                   qty="×1")
    d.wire([(x + 278, unit.bottom), (x + 278, target.top)],
           label=("HDMI + USB cables", "HDMI + USB 線"), muted_label=True)
    units.append(unit)

d.wire([(worker_installer.right, 392), (UNIT_X, 392)], origin_dot=True)
d.step(360, 392, 2)
d.fanout((1136, server.bottom), trunk=280, ends=[(u.x + 100, u.top) for u in units])
d.step(1000, 280, 3)
d.text(1152, 266, ("connect the workers to the Orchestrator", "把 worker 連上 Orchestrator"), "s")

d.legend(424, 592, [
    ("vendor", ("Vendor provides and installs", "廠商提供並安裝")),
    ("customer", ("Customer prepares", "客戶準備")),
    ("step", ("install order", "安裝順序")),
])

vendor_card = items_card(("Vendor provides", "廠商提供"), [
    ("×1", ("Orchestrator installer", "Orchestrator 安裝包"),
     ("Goes on the Linux server.", "裝在 Linux 伺服器上。")),
    ("×1", ("Worker installer", "Worker 安裝檔"),
     ("Goes on the 3 Windows PCs.", "裝在 3 台 Windows PC 上。")),
    ("✓", ("Installation of both", "兩者的安裝"), ("Done on site by the vendor.", "由廠商到場操作。")),
], tone="vendor")
customer_card = items_card(("Customer prepares", "客戶準備"), [
    ("×1", ("Linux server", "Linux 伺服器"),
     ("x86-64, 2 CPU, 16 GB RAM, 60 GB disk. An account with sudo for the install. Without `podman-docker`.",
      "x86-64、2 CPU、16 GB RAM、60 GB 硬碟。安裝時需要有 sudo 權限的帳號。不要安裝 `podman-docker`。")),
    ("×2", "Windows PC", ("Administrator account, automatic logon, no screen lock or sleep.",
                          "要有管理員帳號、設定自動登入、不鎖定螢幕也不睡眠。")),
    ("×3", ("Target device", "目標裝置"), ("With its HDMI and USB cables.", "連同 HDMI 和 USB 線。")),
], tone="customer")
order_card = steps_card(("Install order", "安裝順序"), [
    (("Server.", "伺服器。"), ("The vendor installs the Orchestrator on the Linux server.",
                            "廠商在 Linux 伺服器安裝 Orchestrator。")),
    (("Workers.", "Worker。"), ("The vendor installs the Worker on the 3 Windows PCs.",
                              "廠商在 3 台 Windows PC 安裝 Worker。")),
    (("Connect.", "連線。"), ("The vendor adds the 3 workers and their KVMs in the Orchestrator.",
                           "廠商在 Orchestrator 加入 3 台 worker 和它們的 KVM。")),
])

write_page(
    Path(__file__).with_suffix(".html"),
    ("Trial Deployment", "試用部署"),
    d,
    lead=("One server and three workers. Green is what the customer prepares; purple is what the vendor "
          "provides and installs.",
          "一台伺服器、三台 worker。綠色是客戶要準備的，紫色是廠商提供並安裝的。"),
    caption=("For the trial only one all-in-one box exists, so two workers run on PCs and KVMs the "
             "customer already has.",
             "試用期間只有一台一體機，另外兩台 worker 用客戶現有的 PC 和 KVM。"),
    card_rows=[[vendor_card, customer_card], [order_card]],
)
