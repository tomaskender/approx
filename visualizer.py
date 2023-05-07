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