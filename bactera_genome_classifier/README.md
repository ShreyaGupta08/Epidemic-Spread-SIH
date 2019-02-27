# Bacterial genome classification (HP/non-HP)
Original paper: https://www.nature.com/articles/srep39194
Bacterial pathogenicity prediction using ML over the NGS sequencing data for it's genome and protein structure. 
Philosophy: Current sequence alignment methods rely heavily on availability of similar genomes which not always the case. RL based method to find HP bacteria is much more robust and has wider range of application.

## Theory
- NGS: Next generation sequencing - A new state of the art technology (methodology) to collect sequence data of genomes. It replaced sanger sequencing. (look up sanger sequencing to understand things better) 
- FASTA: Fast-all - A format to store the DNA sequence in textual format. A unique symbol for each base
    - Thymine: T
    - Guanine: G
    - Adenine: A
    - Cytosine: C
- AT - CG pairs with double and triple covalent bonds
- A always pair with T, C always pairs with G
- A and G are double ringed purine based while T and C are single ringed pyridimine based
- HP bacteria: Human pathogenic bacteria - Harmful to us x_x
- DNA sequence unit: Measured in bp (250bp FASTA reads are used in this repo)
- Peptides = ? = chains of amino acids linked via peptide bonds (-COH-NH2-)


## nani da fak is this data?
- final_data.csv ftw
- Genome reads: Make k-mers upto 4 (as per the paper) and store it's occurrence rate in separate column
- Protein reads: Store AAIndex (Amino acid index) stats for 32 most prominent ones (again as per the original paper)

## Model?
- Original paper used random forest
- We use deep neural network: 2 hidden layers.

## Results
Achieved a 95% accuracy that is 7% more than 88% accuracy achieved in the original paper (without the use of other models).
This is.. 
![](https://i.imgur.com/P8O5Lr0.jpg)
