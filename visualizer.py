import argparse
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import re


parser = argparse.ArgumentParser(description="Visualize a run of CGP based on its output.")
parser.add_argument("output", type=str,
                    help="Output file from a previous run of CGP")

args = parser.parse_args()

with open(args.output, "r") as f:
    lines = f.readlines()

generations = []
gate_counts = []
mean_errors = []
max_errors = []
rel_mean_errors = []
for i in range(0, len(lines), 3):
    # extract generation number and gate count
    gen_num = re.search(r"Starting generation (\d+)", lines[i])
    if not gen_num:
        break
    gen_num = int(gen_num.group(1))
    gate_count = int(re.search(r"Current gate count is (\d+)", lines[i+1]).group(1))
    
    # extract error values
    errors = lines[i+2].strip()
    errors = re.search(r"\[mean\] (\d+\.\d+), \[max\] (\d+), \[rel mean\] (\d+\.\d+)", errors)
    mean_error = float(errors.group(1))
    max_error = int(errors.group(2))
    rel_mean_error = float(errors.group(3))
    
    generations.append(gen_num)
    gate_counts.append(gate_count)
    mean_errors.append(mean_error)
    max_errors.append(max_error)
    rel_mean_errors.append(rel_mean_error)


fig, axs = plt.subplots(1, 4, figsize=(20, 4))

for ax in axs:
    ax.set_xlabel("Generation")
    ax.set_xticks(generations)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=15, integer=True))

axs[0].plot(generations, gate_counts, color="blue")
axs[0].set_ylabel("Gate count")

axs[1].plot(generations, max_errors, color="orange")
axs[1].set_ylabel("Max error")

axs[2].plot(generations, mean_errors, color="green")
axs[2].set_ylabel("Mean error")

axs[3].plot(generations, rel_mean_errors, color="red")
axs[3].set_ylabel("Relative mean error")

fig.tight_layout()
plt.show()

# fig, ax = plt.subplots(figsize=(10, 4))
# size = [93.8, 92.5, 87.2, 79.1, 55.0, 36.88]
# generations = [10, 12, 12, 19, 31, 47]
# colors = ["red", "blue", "green", "orange", "purple", "cyan"]
# labels = ["0.1%", "0.2%", "1%", "2%", "10%", "20%"]
# ax.set_ylabel("% of original size")
# ax.set_xlabel("Generations until convergence")
# for i in range(len(labels)):
#     ax.plot(generations[i], size[i], marker="o", color=colors[i], label=labels[i])
# ax.legend()
# plt.show()

# fig, ax = plt.subplots(figsize=(10, 6))
# s01 = [93.8, 94.4, 95.9, 95.0, 94.7]
# s02 = [92.5, 94.4, 93.4, 90.9, 92.8]
# s1 = [87.2, 85.6, 83.4, 88.1, 85.6]
# s2 = [79.1, 82.2, 78.4, 75.0, 69.7]
# s10 = [55.0, 42.2, 50.6, 45.3, 32.8]
# s20 = [36.88, 53.1, 40.3, 37.2, 31.6]
# sizes = [s01, s02, s1, s2, s10, s20]

# labels = ["0.1%", "0.2%", "1%", "2%", "10%", "20%"]
# colors = ["red", "blue", "green", "orange", "purple", "cyan"]
# ax.set_ylabel("% of original circuit")
# ax.set_xlabel("Mean error allowed")

# boxprops = dict(linewidth=2, color='black')
# bp = ax.boxplot(sizes, labels=labels, boxprops=boxprops, patch_artist=True)
# for patch, color in zip(bp['boxes'], colors):
#     patch.set_facecolor(color)
# ax.legend()
# plt.show()
