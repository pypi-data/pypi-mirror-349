from Bio.Seq import Seq

#Step 1: Create a DNA sequence object
dna_sequence = Seq("ATGCTAGCTAGCTAGCTG")

#Step 2: Slice the sequence from index 3 to 10 
sliced_sequence = dna_sequence[3:11]
print("Sliced Sequence:", sliced_sequence)

#Step 3: Concatenate with another sequence
another_sequence = Seq("GGCTAG")
concatenated_sequence = sliced_sequence + another_sequence 
print("Concatenated Sequence:", concatenated_sequence)

#Step 4: Transcribe the concatenated sequence into RNA
rna_sequence = concatenated_sequence.transcribe() 
print("RNA Sequence:", rna_sequence)

#Step 5: Translate the RNA sequence into a protein sequence 
protein_sequence = rna_sequence.translate()
print("Protein Sequence:", protein_sequence)
