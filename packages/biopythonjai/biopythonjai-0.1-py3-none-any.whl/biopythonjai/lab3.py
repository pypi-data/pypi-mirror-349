from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord 
from Bio import SeqIO

#Step 1: Create a DNA sequence
dna_sequence = Seq("ATGCGTACGTAGCTAGCTAG")

#Step 2: Create a SeqRecord object with annotations 
record = SeqRecord(
  dna_sequence,
  id="seq1",
  name="Example_Gene",
  description="Example gene sequence",
  annotations={
    "molecule_type": "DNA", # Required for GenBank
    "gene": "ExampleGene",
    "function": "Hypothetical protein"
  }
)

#Step 3: Write the SeqRecord object to a GenBank file
output_file_path = "data/genbank_1.gb" 
with open(output_file_path, "w") as output_file:
  SeqIO.write(record, output_file, "genbank")

print("GenBank file written successfully.")

#Step 4: Open and read the GenBank file 
with open(output_file_path, "r") as input_file:
  record_read = SeqIO.read(input_file, "genbank") 

  print("\nContents of the GenBank file:") 
  print(record_read)
