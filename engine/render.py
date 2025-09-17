# render module placeholder
# engine/render.py
from .figlib import boxplot
import yaml
import matplotlib.pyplot as plt
from pathlib import Path
from .registry import PLOTTERS

def render_one(fig_yaml, style_dir, out_dir):
    with open(fig_yaml, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    panel = spec["panels"][0]
    typ = panel["type"]
    plotter = PLOTTERS[typ]

    fig, ax = plt.subplots()
    plotter(ax, panel)

    out_path = Path(out_dir) / f"{spec.get('out', 'figure')}.pdf"
    fig.savefig(out_path)
    plt.close(fig)
    print(f"✅ 已生成: {out_path}")