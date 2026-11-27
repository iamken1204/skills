"""Reference build: an operator, a server, three AIO Boxes fanned out, one target machine each.

Shows the left-to-right flow, a dashed neutral zone, a purple chip inside a box,
a horizontal fan-out, and repeated rows on one fixed pitch.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from diagram_kit import Diagram, write_page  # noqa: E402

ROW_PITCH = 136          # every repeated row sits this far below the previous one
FIRST_ROW_CY = 168

d = Diagram(1200, 560, description=(
    "An operator uses the web UI of a Linux server that runs the RPA Orchestrator. The server "
    "dispatches execution to three AIO Boxes on the production lines. Each AIO Box holds the RPA "
    "software and a KVM, and controls one target machine.",
    "操作人員透過 Web UI 使用 Linux 伺服器，伺服器上執行 RPA Orchestrator。伺服器把執行工作派送到產線上的"
    "三台 AIO Box。每台 AIO Box 內有 RPA 軟體和 KVM，各自操控一台目標機台。",
))

d.zone(672, 32, 496, 496, ("Production lines", "產線"))
operator = d.box(32, 248, 136, 64, ("Operator", "操作人員"), rx="pill", align="middle")
server = d.box(296, 216, 256, 128, ("Linux server", "Linux 伺服器"))
d.chip(312, 264, 224, 48, "RPA Orchestrator")
d.wire([(operator.right, operator.cy), (server.left, operator.cy)], label="Web UI")

rows = [FIRST_ROW_CY + index * ROW_PITCH for index in range(3)]
boxes = []
for index, cy in enumerate(rows):
    if index == 0:
        box = d.box(712, cy - 80, 208, 160, "AIO Box")
        d.chip(728, cy - 40, 176, 40, "RPA")
        d.chip(728, cy + 8, 176, 40, "KVM")
    else:
        box = d.box(712, cy - 32, 208, 64, "AIO Box", align="middle")
    target = d.box(1008, box.y, 144, box.h, ("Target machine", "目標機台"), align="middle", title_size=14)
    d.wire([(box.right, cy), (target.left, cy)], label=("Control", "操控") if index == 0 else None)
    boxes.append(box)

d.fanout((server.right, operator.cy), trunk=616, ends=[(b.left, cy) for b, cy in zip(boxes, rows)],
         drops="horizontal", label=("Dispatch\nexecution", "派送\n執行"), label_pos=(604, 112),
         label_anchor="end")

write_page(Path(__file__).with_suffix(".html"), ("RPA Deployment Overview", "RPA 部署架構"), d)
