from typing import Dict, List, Optional
import math
import textwrap


import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

class RouteVisualizer:
    """Generate visual route diagrams as PNG images."""

    def __init__(self, graph: Dict[str, Dict[str, float]]):
        self.graph = graph

    def _edge_weight(self, start: str, end: str) -> Optional[float]:
        if start not in self.graph:
            return None
        return self.graph[start].get(end)

    @staticmethod
    def _format_station_label(station: str) -> tuple[str, int]:
        clean_name = " ".join(station.split())
        wrapped_lines = textwrap.wrap(clean_name, width=11, break_long_words=True)

        if len(wrapped_lines) > 3:
            wrapped_lines = wrapped_lines[:3]
            last_line = wrapped_lines[-1]
            wrapped_lines[-1] = (last_line[:8] + "...") if len(last_line) > 8 else (last_line + "...")

        longest_line = max((len(line) for line in wrapped_lines), default=0)
        if len(wrapped_lines) >= 3 or longest_line > 10:
            font_size = 7
        elif len(wrapped_lines) == 2:
            font_size = 8
        else:
            font_size = 10

        return "\n".join(wrapped_lines), font_size

    def save_route_png(
        self,
        route: List[str],
        total_cost: float,
        filename: str,
        start_station: Optional[str] = None,
        end_station: Optional[str] = None,
        intermediate_stations: Optional[List[str]] = None,
    ) -> str:
        if not route:
            raise ValueError("Route is empty. Cannot generate a diagram.")

        if not filename.lower().endswith(".png"):
            filename += ".png"

        cols = max(3, min(6, int(math.sqrt(len(route))) + 1))
        rows = math.ceil(len(route) / cols)
        x_gap = 3.8
        y_gap = 3.4

        fig_width = max(12, cols * 3.6)
        fig_height = max(6.5, rows * 2.8)
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))

        positions = []
        for i in range(len(route)):
            row = i // cols
            col = i % cols
            # Serpentine row direction gives a compact zig-zag path.
            plot_col = col if row % 2 == 0 else (cols - 1 - col)
            x = plot_col * x_gap
            y = -row * y_gap
            positions.append((x, y))

        requested_intermediates = set(intermediate_stations or [])

        for i, station in enumerate(route):
            is_start = station == start_station if start_station is not None else i == 0
            is_end = station == end_station if end_station is not None else i == len(route) - 1
            is_intermediate = station in requested_intermediates and not is_start and not is_end

            if is_start:
                node_color = "#9be7ff"
                edge_color = "#0277bd"
            elif is_end:
                node_color = "#b9f6ca"
                edge_color = "#2e7d32"
            elif is_intermediate:
                node_color = "#ffe082"
                edge_color = "#ff6f00"
            else:
                node_color = "#eceff1"
                edge_color = "#546e7a"

            x, y = positions[i]

            if is_intermediate:
                # Strong highlight ring for intermediate stations.
                ax.scatter(
                    x,
                    y,
                    s=7600,
                    facecolors="none",
                    edgecolors="#6a1b9a",
                    linewidth=3.2,
                    zorder=2,
                )

            ax.scatter(
                x,
                y,
                s=5200,
                color=node_color,
                edgecolor=edge_color,
                linewidth=2.6,
                zorder=3,
            )
            label_text, label_size = self._format_station_label(station)
            ax.text(
                x,
                y,
                label_text,
                ha="center",
                va="center",
                fontsize=label_size,
                wrap=True,
                zorder=4,
            )

        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            weight = self._edge_weight(start, end)
            label = "unknown" if weight is None else f"{weight:.2f}"

            start_x, start_y = positions[i]
            end_x, end_y = positions[i + 1]

            dx = end_x - start_x
            dy = end_y - start_y
            dist = math.hypot(dx, dy) or 1.0
            ux = dx / dist
            uy = dy / dist

            # Keep arrows outside the large circles.
            radius_offset = 0.72
            p1 = (start_x + ux * radius_offset, start_y + uy * radius_offset)
            p2 = (end_x - ux * radius_offset, end_y - uy * radius_offset)
            arrow = FancyArrowPatch(
                p1,
                p2,
                arrowstyle="-|>",
                mutation_scale=18,
                linewidth=2.1,
                color="#37474f",
                zorder=2,
            )
            ax.add_patch(arrow)

            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            normal_x = -uy
            normal_y = ux
            ax.text(
                mid_x + normal_x * 0.32,
                mid_y + normal_y * 0.32,
                label,
                ha="center",
                va="center",
                fontsize=8,
                color="#111",
                bbox={"boxstyle": "round,pad=0.2", "fc": "#ffffff", "ec": "#b0bec5", "lw": 0.8},
            )

        xs = [x for x, _ in positions]
        ys = [y for _, y in positions]
        ax.set_title(f"Route Diagram (Total Cost: {total_cost:.2f})", fontsize=13, pad=16)
        ax.set_xlim(min(xs) - 2.2, max(xs) + 2.2)
        ax.set_ylim(min(ys) - 2.0, max(ys) + 2.0)
        ax.text(
            min(xs) - 1.9,
            max(ys) + 1.2,
            "Legend: Start (Blue) | Intermediate Stops (Amber + Purple Ring) | End (Green) | Transit (Gray)",
            fontsize=8,
            color="#263238",
            ha="left",
            va="center",
        )
        ax.axis("off")

        fig.tight_layout()
        fig.savefig(filename, dpi=220, bbox_inches="tight")
        plt.close(fig)
        return filename

