# Import pandas, matplotlib, and numpy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


# Read the csv file into a dataframe
df = pd.read_csv("data/MetisAAVE.csv")

# Convert the time column to datetime format
df["time"] = pd.to_datetime(df["time"], format="%d/%m/%Y %H:%M:%S")

# Group the data by date and calculate the mean values

dfmin = df.groupby(df["time"].dt.date).min()
dfavg = df.groupby(df["time"].dt.date).apply(lambda x: x.mean(numeric_only=True))
df = df.groupby(df["time"].dt.date).max()

# Create a range of values for the x-axis
x = np.arange(len(df))

# Create a figure and an axes object
fig, ax = plt.subplots(figsize=(16, 8))

# Create a secondary axis for the subplot
axb = ax.twinx()

# Create a third axis for apyborrow and apysupply
axc = ax.twinx()

# Plot the totalsupply, supplied, borrowcap, and borrowed on the primary axis as bars with 20% transparency
b1 = ax.bar(x - 0.15, df["totalsupply"], width=0.3, color="white", edgecolor="green", linewidth=2, label="totalsupply", alpha=0.8)
b2 = ax.bar(x - 0.15, df["supplied"], width=0.3, color="limegreen", label="supplied", alpha=0.8)
b3 = ax.bar(x + 0.15, df["borrowcap"], width=0.3, color="white", edgecolor="red", linewidth=2, label="borrowcap", alpha=0.8)
b4 = ax.bar(x + 0.15, df["borrowed"], width=0.3, color="red", label="borrowed", alpha=0.8)

# Plot the price on the secondary axis as a line
# l1 = axb.plot(x, df["price"], color="black", linewidth=3, marker="o", label="price")
axb.fill_between(x, dfmin["price"], df["price"], color="gray", alpha=.5, linewidth=0)
l1 = axb.plot(x, dfavg["price"], color="black", linewidth=3, marker="o", label="price")


# Plot the apyborrow and apysupply on the third axis as lines
l2 = axc.plot(x, df["apysupply"], color="lightgreen", linewidth=2, marker="o", label="supply apy")
l3 = axc.plot(x, df["apyborrow"], color="red", linewidth=2, marker="o", label="borrow apy")

# Set the x-axis ticks and labels using linspace and date index
plt.xticks(np.linspace(0, len(df) - 1, 10), df.index[np.linspace(0, len(df) - 1, 10).astype(int)])

# Set the y-axis labels and colors for all axes
ax.set_ylabel("supply/borrow amount (in Metis)", color="black", ha='right')
axb.set_ylabel("price ($)", color="black", ha='left')
axc.set_ylabel("apys (%)", color="black", ha='left')
ax.tick_params(axis='y', labelcolor='black')
axb.tick_params(axis='y', labelcolor='black')
axc.tick_params(axis='y', labelcolor='black')

# Set the y-axis scale to linear for all axes
ax.set_yscale("linear")
axb.set_yscale("linear")
axc.set_yscale("linear")

# Set the y-ticks for all axes with 5 values each
ymin1, ymax1 = 0, max(df["totalsupply"])
ymin2, ymax2 = 0.8 * min(df["price"]), 1.2 * max(df["price"])
ymin3, ymax3 = 0, max(max(df["apysupply"]), max(df["apyborrow"]))

ax.set_yticks(np.linspace(ymin1, ymax1, 10))
axb.set_yticks(np.linspace(ymin2, ymax2, 10))
axc.set_yticks(np.linspace(ymin3, ymax3, 10))

# Add labels, titles, legends, and other customizations
ax.set_title("AAVE supply/borrow stats for Metis", color="black")
ax.set_xlabel("date", color="black")
ax.legend([b[0] for b in [b1, b2, b3, b4]], ["totalsupply", "supplied", "borrowcap", "borrowed"], loc=2)
# axb.legend([l[0] for l in [l1]], ["price"], loc=1)
axc.legend([l[0] for l in [l1, l2, l3]], ["price","supply apy", "borrow apy"], loc=3)
ax.tick_params(axis='both', colors='black')
axb.tick_params(axis='both', colors='black')
axc.tick_params(axis='both', colors='black')
plt.tight_layout()

# Set the background color of the figure to white
fig.set_facecolor("white")

# Adjust the position of the third axis
axc.spines['right'].set_position(('outward', 60))

# Save the plot as a PNG file with 300 dpi
fig.savefig("data/plot.png", dpi=300, bbox_inches="tight")
now = datetime.now().strftime("%Y%m%d_%H%M")
fig.savefig("data/Graph/plot"+now+".png", dpi=300, bbox_inches="tight")


# plt.show()
