import argparse
import sys
import bte

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--tree",help="Path to a MAT protocol buffer containing the global phylogeny to analyze.",required=True)
    parser.add_argument("-f","--reference",help="Path to the root genome for the input MAT protocol buffer in fasta format.",default="./NC_045512v2.fa")
    parser.add_argument("-o","--outreference",help="Indicate a path for an imputed haplotype fasta containing each annotation in the tree.",required=True)
    parser.add_argument("-v","--verbose",action='store_true',help='Use to print status updates.')
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

def main():
    args = argparser()
    t = bte.MATree(args.tree)
    available_annotes = t.dump_annotations()
    if args.verbose:
        print(f"{len(available_annotes)} annotations to be included.",file=sys.stderr)
    refgenome = parse_reference(args.reference)
    of = open(args.outreference,"w+")
    for ann, base_node in available_annotes.items():
        if args.verbose:
            print(f"Imputing haplotype for {ann}.",file=sys.stderr)
        mutd = t.get_haplotype(base_node)
        newref = impute_haplotype(refgenome, mutd)
        print(">"+ann,file=of)
        print(newref,file=of)
    of.close()

if __name__ == '__main__':
    main()