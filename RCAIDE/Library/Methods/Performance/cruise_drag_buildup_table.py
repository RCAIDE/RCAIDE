# RCAIDE/Library/Methods/Performance/cruise_drag_buildup_table.py
# 
# 
# Created:  Feb 2026, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Library.Plots.Common import set_axes, plot_style    
from RCAIDE.Library.Plots import *
 
# Pacakge imports 
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
import os,sys
import pandas as pd
 
# ----------------------------------------------------------------------
#  Calculate vehicle Payload Range Diagram
# ----------------------------------------------------------------------  
def cruise_drag_buildup_table(mission = None, cruise_segment_tag = "cruise", save_filepath = None):

    if mission == None:
        raise AssertionError('Mission not specifed!')
    mission.tag = "cruise_drag_buildup"
    
    results = mission.evaluate()
    drag = results.segments[cruise_segment_tag].conditions.aerodynamics.coefficients.drag
    eps = 1e-12

    def _mean_cd(x):
        arr = x.total if hasattr(x, "total") else x
        arr = np.asarray(arr)
        if arr.ndim == 2:
            arr = arr[:, 0]
        return float(np.mean(arr))

    def _pretty_name(name):
        name_map = {
            "main_wing": "Main Wing",
            "vertical_stabilizer": "Vertical Stabilizer",
            "nacelle_1": "Nacelle 1",
            "propulsor_2_nacelle": "Nacelle 2",
            "nacelle_1_pylon": "Pylon 1",
            "propulsor_2_nacelle_pylon": "Pylon 2",
            "viscous": "Viscous",
            "inviscid": "Inviscid",
        }
        if name in name_map:
            return name_map[name]
        return name.replace("_", " ").title()

    # --- totals (mean over cruise nodes)
    cd_total          = float(np.mean(drag.total[:, 0]))
    cd_parasite_total = float(np.mean(drag.parasite.total[:, 0]))
    cd_induced_total  = float(np.mean(drag.induced.total[:, 0]))
    cd_comp_total     = float(np.mean(drag.compressible.total[:, 0]))
    cd_misc_total     = float(np.mean(drag.miscellaneous.total[:, 0]))
    cd_wave_total     = float(np.mean(drag.wave.total[:, 0]))
    cd_form_total     = float(np.mean(drag.form.total[:, 0]))
    cd_cool_total     = float(np.mean(drag.cooling.total[:, 0]))

    # --- parasite subcomponents from available keys (excluding "total")
    parasite_sub = []
    for key in drag.parasite.keys():
        if key == "total":
            continue
        val = _mean_cd(drag.parasite[key])
        if abs(val) > eps:
            parasite_sub.append((key, val))

    induced_sub = [
        ("viscous",  _mean_cd(drag.induced["viscous"])),
        ("inviscid", _mean_cd(drag.induced["inviscid"])),
    ]
    induced_sub = [(name, val) for name, val in induced_sub if abs(val) > eps]

    categories_raw = [
        ("parasite",      parasite_sub,      cd_parasite_total),
        ("induced",       induced_sub,       cd_induced_total),
        ("compressible",  [("total", cd_comp_total)],  cd_comp_total),
        ("miscellaneous", [("total", cd_misc_total)],  cd_misc_total),
        ("wave",          [("total", cd_wave_total)],  cd_wave_total),
        ("form",          [("total", cd_form_total)],  cd_form_total),
        ("cooling",       [("total", cd_cool_total)],  cd_cool_total),
        ("TOTAL",         [("total", cd_total)],       cd_total),
    ]
    categories = []
    for cat, subs, tot in categories_raw:
        filtered_subs = [(name, val) for name, val in subs if abs(val) > eps]
        if abs(tot) > eps or cat == "TOTAL":
            categories.append((cat, filtered_subs, tot))

    # -------------------------
    # Terminal print
    # -------------------------
    print("\nCruise Drag Buildup (mean over segment)")
    print("-" * 72)
    for cat, subs, tot in categories:
        print(f"{cat:14s}  total = {tot: .6e}")
        for (name, val) in subs:
            if name != "total":
                print(f"  - {name:28s} {val: .6e}")
    print("-" * 72)

    # -------------------------
    # DataFrame for Excel
    # -------------------------
    rows = []
    for cat, subs, tot in categories:
        for (name, val) in subs:
            rows.append({"category": cat, "component": name, "CD": val})
        rows.append({"category": cat, "component": "total", "CD": tot})
    df = pd.DataFrame(rows)

    # -------------------------
    # Plot (stacked bars, hatched subcomponents)
    # -------------------------
    plot_style()
    fig, ax = plt.subplots(figsize=(12, 5))

    hatch_list = ["///", "\\\\\\", "xx", "..", "++", "--", "oo", "**", "||", "//"]
    cat_colors = plt.cm.tab10(np.linspace(0, 1, max(len(categories), 1)))
    cat_to_idx = {cat: i for i, (cat, _, _) in enumerate(categories)}

    for i, (cat, subs, tot) in enumerate(categories):
        bottom = 0.0
        base_color = cat_colors[i]

        # stack subcomponents (if any), each with a different hatch
        if len(subs) > 1 or (len(subs) == 1 and subs[0][0] != "total"):
            for j, (name, val) in enumerate(subs):
                ax.bar(i, val, width=0.7, bottom=bottom,
                       color=base_color, alpha=0.65,
                       hatch=hatch_list[j % len(hatch_list)], edgecolor="k")
                bottom += val
        else:
            bar_val = subs[0][1] if len(subs) > 0 else tot
            ax.bar(i, bar_val, width=0.7, color=base_color, alpha=0.65,
                   hatch=hatch_list[0], edgecolor="k")

        # outline to the category total
        ax.bar(i, tot, width=0.7, fill=False, edgecolor=base_color, linewidth=2.0)

    ax.set_xticks(np.arange(len(categories)))
    ax.set_xticklabels([c[0].capitalize() for c in categories], rotation=25, ha="right")
    ax.set_ylabel(r"c$_D$")
    ax.set_title("Cruise Drag Buildup")
    parasite_color = cat_colors[cat_to_idx["parasite"]] if "parasite" in cat_to_idx else "0.85"
    induced_color = cat_colors[cat_to_idx["induced"]] if "induced" in cat_to_idx else "0.85"
    parasite_handles = [
        Patch(
            facecolor=parasite_color,
            edgecolor="k",
            alpha=0.65,
            hatch=hatch_list[i % len(hatch_list)],
            label=_pretty_name(name),
        )
        for i, (name, val) in enumerate(parasite_sub) if abs(val) > eps
    ]
    induced_handles = [
        Patch(
            facecolor=induced_color,
            edgecolor="k",
            alpha=0.65,
            hatch=hatch_list[i % len(hatch_list)],
            label=_pretty_name(name),
        )
        for i, (name, val) in enumerate(induced_sub) if abs(val) > eps
    ]
    if parasite_handles:
        leg1 = ax.legend(
            handles=parasite_handles,
            title="Parasite subcomponents",
            loc="upper left",
            bbox_to_anchor=(0.01, 0.99),
            fontsize=8,
        )
        ax.add_artist(leg1)
    if induced_handles:
        ax.legend(
            handles=induced_handles,
            title="Induced subcomponents",
            loc="upper left",
            bbox_to_anchor=(0.2, 0.99),
            fontsize=8,
        )
    set_axes(ax)
    plt.tight_layout()

    # -------------------------
    # Pie chart (major component contribution to total drag)
    # -------------------------
    pie_entries = [
        ("Parasite", cd_parasite_total),
        ("Induced", cd_induced_total),
        ("Compressible", cd_comp_total),
        ("Miscellaneous", cd_misc_total),
        ("Wave", cd_wave_total),
        ("Form", cd_form_total),
        ("Cooling", cd_cool_total),
    ]
    pie_entries = [(label, val) for (label, val) in pie_entries if abs(val) > eps]
    pie_labels = [x[0] for x in pie_entries]
    pie_values = [x[1] for x in pie_entries]
    pie_colors = [cat_colors[cat_to_idx[label.lower()]] for label in pie_labels if label.lower() in cat_to_idx]
    if len(pie_colors) != len(pie_labels):
        pie_colors = plt.cm.tab10(np.linspace(0, 1, len(pie_labels)))
    fig_pie, ax_pie = plt.subplots(figsize=(7, 6))
    ax_pie.pie(
        pie_values,
        labels=pie_labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=pie_colors,
        pctdistance=0.78,
        labeldistance=1.06,
        wedgeprops={"edgecolor": "white", "linewidth": 1.0},
        textprops={"fontsize": 10},
    )
    # ax_pie.set_title("Main Drag Component Contribution (%)")
    ax_pie.axis("equal")
    fig_pie.tight_layout()

    # -------------------------
    # Separate parasite zoom figure
    # -------------------------
    fig_parasite_zoom = None
    if len(parasite_sub) > 0:
        fig_parasite_zoom, ax_pz = plt.subplots(figsize=(9, 4.8))
        parasite_zoom_data = [(n, v) for (n, v) in parasite_sub if n != "main_wing" and abs(v) > eps]
        if len(parasite_zoom_data) == 0:
            parasite_zoom_data = parasite_sub

        x_pz = np.arange(len(parasite_zoom_data))
        for i, (name, val) in enumerate(parasite_zoom_data):
            ax_pz.bar(
                i, val,
                color=parasite_color,
                alpha=0.75,
                edgecolor="k",
                hatch=hatch_list[i % len(hatch_list)],
            )
        ax_pz.set_xticks(x_pz)
        nice_labels = [_pretty_name(n) for n, _ in parasite_zoom_data]
        ax_pz.set_xticklabels(nice_labels, fontsize=9, rotation=20, ha="right")
        ax_pz.set_ylabel(r"c$_D$")
        ax_pz.set_title("Parasite Drag Subcomponents")
        ax_pz.grid(True, axis="y", linestyle="--", alpha=0.4)
        zoom_handles = [
            Patch(
                facecolor=parasite_color,
                edgecolor="k",
                alpha=0.75,
                hatch=hatch_list[i % len(hatch_list)],
                label=nice_labels[i],
            )
            for i in range(len(parasite_zoom_data))
        ]
        ax_pz.legend(handles=zoom_handles, title="Parasite subcomponents", loc="upper right", fontsize=8)
        set_axes(ax_pz)
        fig_parasite_zoom.tight_layout()

    # -------------------------
    # Save Excel + image (if save_filepath provided)
    # -------------------------
    if save_filepath is not None:
        if os.path.isdir(save_filepath):
            excel_path = os.path.join(save_filepath, "cruise_drag_buildup.xlsx")
            img_path = os.path.join(save_filepath, "cruise_drag_buildup.png")
            pie_img_path = os.path.join(save_filepath, "cruise_drag_buildup_pie.png")
            parasite_zoom_img_path = os.path.join(save_filepath, "cruise_drag_buildup_parasite_zoom.png")
        elif save_filepath.lower().endswith(".png"):
            img_path = save_filepath
            excel_path = os.path.splitext(save_filepath)[0] + ".xlsx"
            pie_img_path = os.path.splitext(save_filepath)[0] + "_pie.png"
            parasite_zoom_img_path = os.path.splitext(save_filepath)[0] + "_parasite_zoom.png"
        elif save_filepath.lower().endswith(".xlsx"):
            excel_path = save_filepath
            img_path = os.path.splitext(save_filepath)[0] + ".png"
            pie_img_path = os.path.splitext(save_filepath)[0] + "_pie.png"
            parasite_zoom_img_path = os.path.splitext(save_filepath)[0] + "_parasite_zoom.png"
        else:
            excel_path = save_filepath + ".xlsx"
            img_path = save_filepath + ".png"
            pie_img_path = save_filepath + "_pie.png"
            parasite_zoom_img_path = save_filepath + "_parasite_zoom.png"

        out_dir = os.path.dirname(excel_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        df.to_excel(excel_path, index=False)
        fig.savefig(img_path, dpi=200)
        fig_pie.savefig(pie_img_path, dpi=200)
        if fig_parasite_zoom is not None:
            fig_parasite_zoom.savefig(parasite_zoom_img_path, dpi=200)

    return df
