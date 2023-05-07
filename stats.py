import matplotlib.pyplot as plt

# Ad-hoc plotter for different stats that go into documentation.

colors = ["red", "blue", "green", "orange", "purple", "cyan"]
labels = ["0.1%", "0.2%", "1%", "2%", "10%", "20%"]

fig, ax = plt.subplots(figsize=(10, 6))
s01 = [93.8, 94.4, 95.9, 95.0, 94.7]
s02 = [92.5, 94.4, 93.4, 90.9, 92.8]
s1 = [87.2, 85.6, 83.4, 88.1, 85.6]
s2 = [79.1, 82.2, 78.4, 75.0, 69.7]
s10 = [55.0, 42.2, 50.6, 45.3, 32.8]
s20 = [36.88, 53.1, 40.3, 37.2, 31.6]
sizes = [s01, s02, s1, s2, s10, s20]

ax.set_ylabel("% of original circuit")
ax.set_xlabel("Mean error allowed")

boxprops = dict(linewidth=2, color='black')
bp = ax.boxplot(sizes, labels=labels, boxprops=boxprops, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax.legend()
plt.show()

fig, ax = plt.subplots(figsize=(10, 6))
g01 = [10, 7, 6, 8, 9]
g02 = [12, 7, 8, 10, 12]
g1 = [12, 12, 16, 10, 15]
g2 = [19, 13, 19, 22, 25]
g10 = [31, 39, 33, 39, 56]
g20 = [47, 31, 42, 42, 54]
generations = [g01, g02, g1, g2, g10, g20]
ax.set_ylabel("Generations until convergence")
ax.set_xlabel("Mean error allowed")

boxprops = dict(linewidth=2, color='black')
bp = ax.boxplot(generations, labels=labels, boxprops=boxprops, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax.legend()
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_ylabel("% of original size")
ax.set_xlabel("Generations until convergence")
for i in range(len(labels)):
    ax.scatter(generations[i], sizes[i], marker="o", color=colors[i], label=labels[i])
ax.legend()
plt.show()