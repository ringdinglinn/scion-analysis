import matplotlib as mpl

def apply_styling():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial"],
        "mathtext.fontset": "cm",
        "mathtext.rm": "sans",
        "mathtext.default": "regular",
        "font.size": 14,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })