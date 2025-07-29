from Bio import Entrez

#Step 1: Provide your email for NCBI's Entrez system
Entrez.email = "jaigupta.is22@bmsce.ac.in"

#Step 2: Specify the accession number of the sequence
accession_number = "NM_001301717" # Example accession number for a human gene

#Step 3: Fetch the sequence from GenBank using Entrez
handle = Entrez.efetch(db="nucleotide", id=accession_number, rettype="gb",retmode="text") 
record = handle.read()
handle.close() 

#Step 4: Parse the sequence and metadata 
from Bio import SeqIO
import io
#UseSeqIOto parse the GenBank format sequencedata 
handle = io.StringIO(record) 
handle.seek(0)
seq_record = SeqIO.read(handle, "genbank")

#Step 5: Print the sequence and metadata
print(f"Accession Number: {seq_record.id}")
print(f"Description: {seq_record.description}")
print(f"Organism: {seq_record.annotations['organism']}")
print(f"Sequence: {seq_record.seq}")
print(f"Length of Sequence: {len(seq_record.seq)}") 
print(f"Features: {seq_record.features}")
