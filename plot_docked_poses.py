"""Draw two coordinate projections of the top five Vina poses as an SVG."""

from html import escape
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
COLORS = {
    "12313376": ("Nimbolide", "#a62646"),
    "10906239": ("Azadirone", "#135eaa"),
    "10219": ("Emetine", "#365a39"),
    "68911": ("Artemether", "#7f4ca5"),
    "936": ("Nicotinamide", "#b35c00"),
}


def atom_records(path, first_model=False):
    for line in path.read_text(encoding="ascii").splitlines():
        if first_model and line == "ENDMDL":
            return
        if line.startswith(("ATOM  ", "HETATM")):
            point = tuple(float(line[index:index + 8]) for index in (30, 38, 46))
            yield line, point


def text(x, y, label, size=14, fill="#263853"):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">'
        f'{escape(label)}</text>'
    )


def circle(x, y, radius, color, opacity=1):
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" '
        f'opacity="{opacity}" />'
    )


def panel(left, horizontal, label, receptor, pocket, ligands):
    top = 112
    panel_size = 330
    extent = 66
    scale = panel_size / extent
    mid = (4, 3, 23)

    def project(point):
        x = left + panel_size / 2 + (point[horizontal] - mid[horizontal]) * scale
        y = top + panel_size / 2 - (point[2] - mid[2]) * scale
        return x, y

    items = [
        f'<rect x="{left}" y="{top}" width="{panel_size}" height="{panel_size}" '
        'rx="8" fill="#f5f8fc" stroke="#c9d5e3" />',
        text(left, top - 14, label, 16),
        text(left + 125, top + panel_size + 22, label[0] + " coordinate (Å)"),
        text(left + 10, top + 19, "Z ↑", 12),
        f'<clipPath id="panel{horizontal}"><rect x="{left}" y="{top}" '
        f'width="{panel_size}" height="{panel_size}"/></clipPath>',
        f'<g clip-path="url(#panel{horizontal})">',
    ]
    last = None
    for resi, point in receptor:
        x, y = project(point)
        if last is not None and resi == last[0] + 1:
            px, py = project(last[1])
            items.append(
                f'<path d="M{px:.2f},{py:.2f} L{x:.2f},{y:.2f}" '
                'stroke="#a2b0c2" stroke-width="1.6" fill="none"/>'
            )
        last = resi, point
    for resi, point in receptor:
        if resi in pocket:
            items.append(circle(*project(point), 2.5, "#126d78"))
    for cid, points in ligands.items():
        for point in points:
            items.append(circle(*project(point), 3, COLORS[cid][1], 0.73))
    items.append("</g>")
    return items


def main():
    receptor = [
        (int(line[22:26]), point)
        for line, point in atom_records(ROOT / "structures/8TO4_prepared.pdb")
        if line[12:16].strip() == "CA" and line[21] == "D"
    ]
    pocket = {
        int(line[22:26])
        for line, _ in atom_records(ROOT / "data/pocket_p0_records.pdb")
    }
    ligands = {}
    for path in sorted((ROOT / "docking/poses").glob("*.pdbqt")):
        cid = path.name.split("_", 1)[0]
        ligands[cid] = [
            point
            for line, point in atom_records(path, first_model=True)
            if line[77:].strip() not in {"H", "HD", "HS"}
        ]
    if set(ligands) != set(COLORS):
        raise ValueError("Expected one pose file for each of the five compounds.")

    layers = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="840" height="550" '
        'viewBox="0 0 840 550" role="img" aria-labelledby="title description">',
        '<title id="title">Top-ranked docked poses in 8TO4 chain D</title>',
        '<desc id="description">Two projections show heavy atoms from five '
        'rank-one poses against the EGFR chain D backbone and predicted pocket.</desc>',
        '<rect width="840" height="550" fill="white"/>',
        '<g font-family="Arial, sans-serif">',
        text(58, 40, "Top-ranked docked poses in 8TO4 chain D", 26),
        text(58, 65, "Rank-one Vina pose heavy atoms projected in the receptor coordinate frame", 15),
        *panel(58, 0, "X–Z projection", receptor, pocket, ligands),
        *panel(452, 1, "Y–Z projection", receptor, pocket, ligands),
    ]
    for i, (name, color) in enumerate(COLORS.values()):
        x = 64 + 145 * i
        layers.extend([circle(x, 493, 4, color), text(x + 10, 498, name)])
    layers.extend([
        '<path d="M60,521 L78,521" stroke="#a2b0c2" stroke-width="2"/>',
        text(87, 526, "Chain D Cα trace"),
        circle(245, 521, 3, "#126d78"),
        text(256, 526, "DoGSiteScorer P_0 residue Cα"),
        "</g></svg>",
    ])
    svg = "\n".join(layers) + "\n"
    ElementTree.fromstring(svg)
    (ROOT / "figures/docked_pose_projections.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
