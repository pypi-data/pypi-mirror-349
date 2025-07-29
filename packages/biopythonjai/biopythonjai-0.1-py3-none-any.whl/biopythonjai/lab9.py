from Bio import Phylo, AlignIO
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt

#Loadthe sequence alignment
alignment = AlignIO.read("data/aligned_sequences.aln", "clustal")

#Computedistance matrix
calculator = DistanceCalculator("identity")
distance_matrix = calculator.get_distance(alignment)

#Build the phylogenetic tree using UPGMA
constructor = DistanceTreeConstructor()
tree = constructor.upgma(distance_matrix)

#Save tree
Phylo.write(tree, "data/phylogenetic_tree.nwk", "newick")

#Drawthetree
fig = plt.figure(figsize=(8, 5)) # Set figure size
ax = fig.add_subplot(1, 1, 1) # Ensure only one subplot is used
Phylo.draw(tree, axes=ax) # Draw the tree on the specified axis
plt.show() # Display the tree
