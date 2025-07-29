import subprocess
from Bio import AlignIO

# Use the full path to muscle.exe
# https://drive5.com/muscle/downloads_v3.htm
muscle_exe = "data/muscle3.8.31_i86win32.exe"

try:
    # Run MUSCLE using subprocess
    subprocess.run([
        muscle_exe,
        "-in", "data/fasta_1.fasta",
        "-out", "data/aligned_sequences.fasta"
    ], check=True)
    
    # Read and print the aligned sequences
    alignment = AlignIO.read("data/aligned_sequences.fasta", "fasta")
    print(alignment)
    
except FileNotFoundError:
    print("Error: MUSCLE executable not found. Check the path:", muscle_exe)
except subprocess.CalledProcessError as e:
    print(f"Error running MUSCLE: {e}")
