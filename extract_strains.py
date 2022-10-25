import argparse
import bte
from pango_aliasor.aliasor import Aliasor
global_aliasor = Aliasor()

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--tree",help="Path to a MAT protocol buffer containing the global phylogeny to analyze.",required=True)
    parser.add_argument("-f","--reference",help="Path to the root genome for the input MAT protocol buffer in fasta format.",default="./NC_045512v2.fa")
    parser.add_argument("-o","--outreference",help="Indicate a path for an imputed haplotype fasta containing each annotation in the tree.",required=True)
    parser.add_argument("-v","--verbose",action='store_true',help='Use to print status updates.')
    parser.add_argument("-t","--table",help="Path to a table containing output summary statistics for each lineage.",default=None)
    parser.add_argument("-g","--gtf",help="Path to a GTF to perform translation of nucleotides to amino acid changes. Required for -t output.",default=None)
    return parser.parse_args() 

def parse_reference(refpath):
    refstr = []
    with open(refpath) as inf:
        for entry in inf:
            if entry[0] != ">":
                refstr.append(entry.strip())
    return "".join(refstr)

def process_mutstr(mstr):
    loc = int(mstr[1:-1])
    alt = mstr[-1]
    return (loc,alt)

def impute_haplotype(refstr, mutd):
    update = list(refstr)
    for m in mutd:
        loc,alt = process_mutstr(m)
        update[loc] = alt
    return "".join(update)

def tabledata(tree, nid, translation, ancestor):
    subs = []
    aa_subs = []
    new_subs = []
    new_aa_subs = []
    new_reversions = []
    new_aa_reversions = []
    new = True
    for n in tree.rsearch(nid,True):
        if n.id == ancestor:
            new = False

        for m in n.mutations:
            for om in subs:
                if m[1:-1] == om[1:-1]:
                    nm = om[0] + m[1:]
                    break

            subs.append(m)
            if new:
                new_subs.append(nm)
        
        trand = translation.get(n.id,[])        
        for aa in trand:
            naa = aa
            for oaa in aa_subs:
                if aa.gene == oaa.gene and aa.aa_index == oaa.aa_index:
                    #merge these 
                    naa.original_aa = oaa.original_aa
                    naa.original_codon = oaa.original_codon
                    naa.original_nt = oaa.original_nt
            aa_subs.append(naa)
            if new:
                new_aa_subs.append(naa)
def main():
    args = argparser()
    t = bte.MATree(args.tree)
    if args.table != None:
        if args.gtf == None:
            raise Exception("-g GTF file required for -t output!")
        if args.verbose:
            print("Translating...")
        translation = t.translate(reference=args.reference,gtf=args.gtf)
    available_annotes = t.dump_annotations()
    refgenome = parse_reference(args.reference)
    if args.table:
        outf = open(args.table,"w+")
        print('\t'.join(['lineage_name','unaliased_lineage_name','substitutions','aa_substitutions','new_substitutions','new_aa_substitutions','new_reversions','new_aa_reversions']))
    for ann, base_node in available_annotes.items():
        if args.verbose:
            print("Imputing haplotype for {}.")
        mutd = t.get_haplotype(base_node)
        newref = impute_haplotype(refgenome, mutd)
        with open(args.outreference,"w+") as of:
            print(">"+ann,file=of)
            print(newref,file=of)
        if args.table:
            ancestor = global_aliasor.compress(".".join(global_aliasor.decompress(ann).split(".")[:-1]))
            td = tabledata(tree, base_node, translation, ancestor)
            print("\t".join([ann, global_aliasor.decompress(ann)] + td), file=outf)
            

if __name__ == '__main__':
    main()