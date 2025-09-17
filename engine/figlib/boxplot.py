# boxplot plotting placeholder
# engine/figlib/boxplot.py
import seaborn as sns
from ..registry import register
from ..io import load_table

@register("box")
def plot_box(ax, panel):
    df = load_table(panel["data"])
    sns.boxplot(
        data=df,
        x=panel["mapping"]["x"],
        y=panel["mapping"]["y"],
        order=panel.get("order"),
        ax=ax,
        linewidth=0.5,
        width=0.6,
        fliersize=0
    )
    sns.stripplot(
        data=df,
        x=panel["mapping"]["x"],
        y=panel["mapping"]["y"],
        order=panel.get("order"),
        ax=ax,
        color="black",
        size=2
    )
    ax.set_xlabel(panel["x_label"])
    ax.set_ylabel(panel["y_label"])