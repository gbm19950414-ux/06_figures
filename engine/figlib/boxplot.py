# boxplot plotting placeholder
# engine/figlib/boxplot.py
import os
import seaborn as sns
from statannotations.Annotator import Annotator
import pandas as pd
from ..registry import register
from ..io import load_table

@register("box")
def plot_box(ax, panel, style=None):
    df = load_table(panel["data"])
    # 如果 panel 中指定了 order，则强制 df 的 x 列按照 order 排序
    if panel.get("order"):
        x_key = panel["mapping"]["x"]
        df[x_key] = pd.Categorical(
            df[x_key],
            categories=panel["order"],
            ordered=True
        )
    # 优先使用面板级调色板，其次是全局样式中的 palette
    palette = panel.get("palette")
    if palette is None and style:
        palette = style.get("color", {}).get("palette")
    sns.boxplot(
        data=df,
        x=panel["mapping"]["x"],
        y=panel["mapping"]["y"],
        hue=panel["mapping"].get("hue"),           # ✅ 添加 hue
        order=panel.get("order"),
        hue_order=panel.get("hue_order"),          # ✅ 添加 hue_order
        palette=palette,                # ✅ 使用 palette
        ax=ax,
        linewidth=0.5,
        width=0.6,   # ✅ 允许 YAML 中设置 box_width
        fliersize=0,
        dodge=True                                 # ✅ 确保分组并排
    )
    sns.stripplot(
        data=df,
        x=panel["mapping"]["x"],
        y=panel["mapping"]["y"],
        hue=panel["mapping"].get("hue"),           # ✅ 添加 hue
        order=panel.get("order"),
        hue_order=panel.get("hue_order"),          # ✅ 添加 hue_order
        palette=palette,                # ✅ 使用 palette
        ax=ax,
        dodge=True,
        color=None,
        size=2
    )
        # === 显著性标注 ===
    stats_cfg = panel.get("stats", {})
    if stats_cfg.get("enabled", False):
        sheet_name = stats_cfg.get("sheet", 0)  # 如果没有 sheet，默认第一个工作表
        pvals_df = pd.read_excel(stats_cfg["source"], sheet_name=sheet_name)
        pairs = []
        pvals = []
        # 按照 YAML 中的 order 字段重新排序
        display_order = panel.get("order", [])
        if display_order:
            pvals_df[x_key] = pd.Categorical(
                pvals_df[x_key], categories=display_order, ordered=True
            )
            pvals_df = pvals_df.sort_values(x_key)
        # 生成 pairs 和 pvals，保证顺序与绘图一致
        for _, row in pvals_df.iterrows():
            drug = row[x_key]
            if pd.isna(drug):   # ✅ 跳过 drug 为空的比较
                continue
            pairs.append(((drug, "WT"), (drug, "HO")))
            pvals.append(row[stats_cfg.get("column", "p_value")])
        if pairs:
            annot = Annotator(
                ax, pairs, data=df,
                x=panel["mapping"]["x"],
                y=panel["mapping"]["y"],
                hue=panel["mapping"].get("hue")
            )
            # 读取 style/stat.yaml 中的显著性样式配置
            stat_style = {}
            if style:
                # 直接获取 style 目录下的 stat.yaml 配置
                stat_style = style.get("stat", {})
            annot.configure(
                test=None,
                text_format="star",
                loc="inside",
                fontsize=stat_style.get("star_fontsize", 6),     # 全局控制星号字体大小
                line_width=stat_style.get("line_width", 0.5),    # 全局控制显著性线段线宽
                line_height=stat_style.get("line_height", 0.03)  # 全局控制显著性线段高度
            )
            annot.set_pvalues(pvals)
            annot.annotate()
    # 设置坐标轴范围
    if "ylim" in panel:
        ax.set_ylim(panel["ylim"])
    # 设置坐标轴标题，并确保留有足够的内边距
    ax.set_xlabel(panel.get("x_label", ""), labelpad=panel.get("x_labelpad", 4))
    ax.set_ylabel(panel.get("y_label", ""), labelpad=panel.get("y_labelpad", 10))
    
    # 如果在 panel 中指定了 x_tick_rotation，则旋转 x 轴刻度标签
    if "x_tick_rotation" in panel:
        for tick in ax.get_xticklabels():
            tick.set_rotation(panel["x_tick_rotation"])
            tick.set_ha("right")
    # 去重图例
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[0:len(set(labels))], list(set(labels)))