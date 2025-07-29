from Bio import SeqIO

#Function to read sequences from a FASTA file and print description and sequence 
def read_fasta(file_path):

  #Parse the FASTA file
  for record in SeqIO.parse(file_path, "fasta"):

    #Print the description (header) and sequence 
    print(f"Description: {record.description}") 
    print(f"Sequence: {record.seq}")
    print() 
    
#Specify the path to your FASTA file
fasta_file = "data/fasta_1.fasta" 

#Call the function to read and print the sequence data 
read_fasta(fasta_file)
