import os
import matplotlib.pyplot as plt
import matplotlib as mpl

def configure_plot_style():
    mpl.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['DejaVu Serif'],
        'font.size': 18,
        'axes.titlesize': 22,
        'axes.labelsize': 18,
        'xtick.labelsize': 16,
        'ytick.labelsize': 16,
        'lines.linewidth': 2,
        'lines.markersize': 8,
        'axes.linewidth': 1.2,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.linestyle': '--',
        'grid.linewidth': 0.6,
        'grid.alpha': 0.6,
        'legend.frameon': True,
        'legend.fontsize': 16,
        'legend.title_fontsize': 16,
    })

def plot_cka_single_line(cka_results, layers, output_path, label="Unlearned", color="#1b9e77", linestyle="--"):
    """
    Plot CKA similarity between original and updated model across layers.
    
    Args:
        cka_results: dict of {layer_index: cka_value}
        layers: list of int, which layers to plot
        output_path: path to save PDF (e.g., "output/cka_plot.pdf")
        label: label for the updated model
        color: line color
        linestyle: line style
    """
    configure_plot_style()
    
    y_vals = [cka_results[L] for L in layers]
    marker_freq = 5
    marker_indices = [i for i in range(len(layers)) if i % marker_freq == 0]

    fig, ax = plt.subplots(figsize=(5, 3))

    ax.plot(layers, y_vals, linestyle=linestyle, linewidth=2,
            color=color, label=label)
    
    ax.plot([layers[i] for i in marker_indices],
            [y_vals[i] for i in marker_indices],
            'o', color=color, markersize=6)

    ax.set_xticks([L for i, L in enumerate(layers) if i % 5 == 0])
    ax.set_xticklabels([str(L) for i, L in enumerate(layers) if i % 5 == 0])
    ax.set_xlabel("Layer index")
    ax.set_ylabel("Linear CKA")
    ax.set_title("CKA", pad=12)
    ax.set_ylim(-1, 3)

    ax.legend(loc="best", frameon=False, fancybox=True)

    fig.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.show()
