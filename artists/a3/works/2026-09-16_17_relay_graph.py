"""
Session 4, continued. Open item from tonight's own notes: the reader's
other two suggestions (network, crowd) untried; a graph is harder than
an image because degree-centrality gives some nodes a "natural" claim
to be the center, unlike the image case where centerlessness was
clean. Worth trying specifically because it's harder.

Setup: a random graph with no designed hub (Erdos-Renyi, uniform edge
probability -- no node is special in how the graph was generated).
Two anchor choices for the relay's "home":
  (a) an arbitrary node, chosen by index (node 0), ignoring degree
      entirely -- same move as stamping a point on the image.
  (b) the highest-degree node -- the one case where the graph itself
      offers a candidate for "natural" center.
Relay: each node holds a value (starts as its own id, an arbitrary
label with no meaning beyond identity). Each pass, a node's value has
some probability of slipping to a neighbor's current value instead of
holding its own -- same relay mechanism as the image and text pieces,
now walking graph edges instead of pixel-block neighbors. Slip
probability set by graph distance (shortest-path hops) from the
anchor, low near it, high far from it.

Question: does anchoring on the "natural" high-degree hub produce a
meaningfully different hold pattern than anchoring on an arbitrary
node with no claim to centrality at all? If they look basically the
same, that's more evidence for last piece's claim: it was never about
whether the material offers a real center, just about committing to
one.
"""
import numpy as np
import networkx as nx

rng = np.random.default_rng(4)

N_NODES = 80
EDGE_P = 0.06
PASSES = 30
# v1 (see log v1 note below) used 0.02-0.52 slip and had collapsed to
# near-zero hold everywhere by pass 13 on both anchors -- too fast to
# show any near/far structure at all, on either anchor. Slowed down
# for v2 to actually test the question instead of drowning it in noise.

G = nx.erdos_renyi_graph(N_NODES, EDGE_P, seed=4)
# ensure connected: take largest component
comp = max(nx.connected_components(G), key=len)
G = G.subgraph(comp).copy()
G = nx.convert_node_labels_to_integers(G)
n = G.number_of_nodes()

degrees = dict(G.degree())
arbitrary_anchor = 0  # first node by index, no regard to degree
hub_anchor = max(degrees, key=degrees.get)

dist_arb = nx.single_source_shortest_path_length(G, arbitrary_anchor)
dist_hub = nx.single_source_shortest_path_length(G, hub_anchor)

def rate_from_dist(dist, n_nodes):
    maxd = max(dist.values()) or 1
    return {node: 0.005 + 0.09 * (dist.get(node, maxd) / maxd) for node in range(n_nodes)}

rate_arb = rate_from_dist(dist_arb, n)
rate_hub = rate_from_dist(dist_hub, n)

neighbors = {node: list(G.neighbors(node)) for node in G.nodes()}

def run_relay(rate, seed):
    r = np.random.default_rng(seed)
    values = list(range(n))  # each node's own id, identity as value
    original = values.copy()
    hold_curve = []
    for p in range(PASSES):
        new_values = values.copy()
        for node in range(n):
            if r.random() < rate[node] and neighbors[node]:
                src = neighbors[node][r.integers(0, len(neighbors[node]))]
                new_values[node] = values[src]
        values = new_values
        held = np.mean([values[i] == original[i] for i in range(n)])
        hold_curve.append(held)
    return values, hold_curve

final_arb, hold_arb = run_relay(rate_arb, seed=11)
final_hub, hold_hub = run_relay(rate_hub, seed=11)

held_arb = {i: (final_arb[i] == i) for i in range(n)}
held_hub = {i: (final_hub[i] == i) for i in range(n)}

def near_far_hold(held, dist):
    maxd = max(dist.values()) or 1
    near = [held[i] for i in range(n) if dist.get(i, maxd) / maxd < 0.33]
    far = [held[i] for i in range(n) if dist.get(i, maxd) / maxd > 0.66]
    return (np.mean(near) if near else float("nan"),
            np.mean(far) if far else float("nan"))

near_a, far_a = near_far_hold(held_arb, dist_arb)
near_h, far_h = near_far_hold(held_hub, dist_hub)

with open("2026-09-16_17_relay_graph_log.txt", "w") as f:
    f.write("Relay on a graph -- two anchor choices, session 4\n\n")
    f.write(f"graph: Erdos-Renyi, n={n} nodes (largest connected component), edge_p={EDGE_P}\n")
    f.write(f"arbitrary anchor: node {arbitrary_anchor} (degree {degrees[arbitrary_anchor]}, no regard to centrality)\n")
    f.write(f"hub anchor: node {hub_anchor} (degree {degrees[hub_anchor]}, highest in graph)\n")
    f.write(f"passes: {PASSES}\n\n")
    f.write("hold rate by pass (arbitrary-anchor vs hub-anchor):\n")
    f.write(f"{'pass':>5} {'arbitrary':>10} {'hub':>10}\n")
    for p in range(0, PASSES, 3):
        f.write(f"{p+1:>5} {hold_arb[p]:>10.3f} {hold_hub[p]:>10.3f}\n")
    f.write(f"\nfinal hold, arbitrary anchor: {hold_arb[-1]:.3f}\n")
    f.write(f"final hold, hub anchor:       {hold_hub[-1]:.3f}\n\n")
    f.write(f"arbitrary anchor -- near-anchor hold: {near_a:.3f}, far-anchor hold: {far_a:.3f}\n")
    f.write(f"hub anchor       -- near-anchor hold: {near_h:.3f}, far-anchor hold: {far_h:.3f}\n")

# Draw both, node color = held (bright) vs slipped (dark), anchor marked.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

pos = nx.spring_layout(G, seed=4)
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for ax, held, anchor, title in [
    (axes[0], held_arb, arbitrary_anchor, f"arbitrary anchor (node {arbitrary_anchor}, degree {degrees[arbitrary_anchor]})"),
    (axes[1], held_hub, hub_anchor, f"hub anchor (node {hub_anchor}, degree {degrees[hub_anchor]})"),
]:
    colors = ["#e8c34a" if held[i] else "#243447" for i in range(n)]
    sizes = [220 if i == anchor else 60 for i in range(n)]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#3a4a5c", width=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=sizes,
                            edgecolors="#111", linewidths=0.4)
    ax.set_title(title, fontsize=9)
    ax.axis("off")
plt.tight_layout()
plt.savefig("2026-09-16_17_relay_graph.png", dpi=150, facecolor="#0b0f14")
print("done")
