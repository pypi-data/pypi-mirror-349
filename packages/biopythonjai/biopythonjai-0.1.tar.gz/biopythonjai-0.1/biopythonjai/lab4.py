from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

#Function to convert FASTA file to GenBank format 
def convert_fasta_to_genbank(fasta_file, genbank_file):
  #Parse the FASTA file and read sequences 
  records = []
  for record in SeqIO.parse(fasta_file, "fasta"):
    #Extract the sequence and description from FASTA
    sequence = record.seq
    description = record.description
    #Create SeqRecord object for GenBank with basic annotations
    genbank_record = SeqRecord(
      sequence,
      id=record.id,
      name="Example_Gene",
      description=description, 
      annotations={
        "molecule_type": "DNA", # Required for GenBank format 
        "gene": "ExampleGene",
        "function": "Hypothetical protein"
      }
    )

    records.append(genbank_record) # Add the record to the list the list 

  # Write all SeqRecords to GenBank format at once
  with open(genbank_file, "w") as output_handle:
    SeqIO.write(records, output_handle, "genbank")

  print(f"All FASTA sequences converted to GenBank format and saved as {genbank_file}") # Define input and output file paths

fasta_file = "data/fasta_1.fasta" # Replace with your actual FASTA file path 
genbank_file = "data/example_output.gb" # Output GenBank file

#Call the function to convert FASTA to GenBank
convert_fasta_to_genbank(fasta_file, genbank_file)
