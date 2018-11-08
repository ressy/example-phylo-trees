all: alignment.ph

clusters.fasta:
	python3 simulate.py > $@

# Align the input sequences and output in FASTA format, and also save the guide
# tree in Phylip format.
alignment.fasta: clusters.fasta
	clustalw2 -infile=$^ -outfile=$@ -align -output=fasta -newtree=alignment.dnd

# Make a phylogenetic tree from the alignment in the Phylip format.
alignment.ph: alignment.fasta
	clustalw2 -infile=$^ -outfile=$@ -tree

# Make a phylogenetic tree from the alignment in the Phylip format, with bootstrap details.
# It seems to ignore -outfile for this one.
alignment.phb: alignment.fasta
	clustalw2 -infile=$^ -outfile=$@ -bootstrap

clean:
	rm -f alignment.dnd alignment.fasta alignment.ph alignment.phb clusters.fasta
