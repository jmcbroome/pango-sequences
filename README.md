# Consensus sequences for each Pango lineage

This fork contains automatically generated root sequences for each annotated lineage on the global phylogeny. This includes Pango lineages, Nextstrain clades, and any other annotations present within the annotation data associated with the latest phylogeny. As with the main repository, these sequences are not real sequences in databases but  algorithmically constructed consensus sequences that represent the inferred common ancestor sequence of that lineage. They are based on the global phylogeny produced and maintained by UCSC. 

Please be aware that due to the automatic generation of these synthetic sequences, they can contain errors. Notably, none of these inferred sequences will contain structural variants, as the global phylogeny does not currently include insertion or deletion information.

The repository contains:

- "lineage_roots.fasta.zst": A zst compressed fasta file with all annotation root sequences. It can be decompressed with `zstdcat data/lineage_roots.fasta.zst > lineages.fasta`. You can pick a sequence of interest using `seqkit grep -r -p "B.1.1.7" lineages.fasta`.
- "pango_consensus_seequences.fasta.zstd": A zst compressed fasta file with pango root sequences alone, inferred as described in the [main fork](https://github.com/corneliusroemer/pango-sequences/blob/main/README.md)
- "extract_strains.py", "NC_045512v2.fa", and "env.yml": The script we use to extract the root sequence fasta and table from a global phylogeny, the SARS-CoV-2 global phylogeny root reference sequence, and a conda environment file with dependencies for this script, respectively.

If you need to be sure that a sequence is correct, e.g. when you're creatin a Spike protein for an experiment, please double check using the pango designation issue (if such an issue exists) and the annotation on the Usher tree - which is independently curated by @AngieHinrichs. Also, see <https://github.com/ucscGenomeBrowser/kent/blob/master/src/hg/utils/otto/sarscov2phylo/pango.clade-mutations.tsv> for the paths extracted from the Usher tree for each lineage.
