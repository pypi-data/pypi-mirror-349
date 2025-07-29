from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

#Step 1: Create a DNA sequence
dna_sequence = Seq("ATGCGTACGTAGCTAGCTAG")

#Step 2: Create a SeqRecord object with the sequence 
record = SeqRecord(
  dna_sequence,
  id="seq1",
  name="Example_Gene",
  description="An example DNA sequence for gene annotation.",
)

#Step 3: Add annotations for the gene
record.annotations["gene"] = "ExampleGene"
record.annotations["function"] = "Hypothetical protein"
record.annotations["organism"] = "Synthetic organism"

#Step 4: Add afeature for the gene (start and end positions) 
from Bio.SeqFeature import SeqFeature, FeatureLocation
gene_feature = SeqFeature(FeatureLocation(0, 21), type="gene", qualifiers={"gene": "ExampleGene"})
record.features.append(gene_feature)

#Step 5: Modify the annotation (change function description)
record.annotations["function"] = "Hypothetical protein with modified function"

#Step 6: Print the updated SeqRecord 
print(f"ID: {record.id}")
print(f"Name: {record.name}")
print(f"Description: {record.description}")
print(f"Annotations: {record.annotations}")
print(f"Features: {record.features}")
