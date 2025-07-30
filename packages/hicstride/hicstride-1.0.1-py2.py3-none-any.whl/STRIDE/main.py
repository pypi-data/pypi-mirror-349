import os, sys
from . import MFPT
import argparse
from scipy import sparse
import importlib
import numpy as np
import h5py
from joblib import Parallel, delayed
from collections import Counter
import pandas as pd


class CommaSeparationAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(","))


class GetNormAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values.isdigit():
            values = int(values)
        elif values == "None":
            values = None
        elif values == "inf":
            values = np.inf
        elif values in ("nuc", "fro"):
            pass
        else:
            raise argparse.ArgumentError(
                self,
                message="The norm should be in {int, inf, 'fro', 'nuc', None}")
        setattr(namespace, self.dest, values)


class OutputDirectoryAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        values = os.path.abspath(values)
        if not os.path.isdir(values):
            os.makedirs(values)
        setattr(namespace, self.dest, values)


def readBedFile(fileName, res, chrlen):
    p1, p2, values = [], [], []
    with open(fileName, 'rt') as fin:
        for line in fin:
            p, q, v = line.strip().split()
            p = int(p) // res
            q = int(q) // res
            if p == q:
                v = float(v) / 2
            else:
                v = float(v)
            p1.append(p)
            p2.append(q)
            values.append(v)
    s = chrlen // res + 1
    y = sparse.csr_array((values, (p1, p2)), shape=(s, s))
    return (y + y.T).toarray()


def readHiCFile(hicFile, res, chrName):
    hicstraw = importlib.import_module("hicstraw")
    hic = hicstraw.HiCFile(hicFile)
    try:
        cname = chrName
        chrLen = [i.length for i in hic.getChromosomes() if i.name == cname][0]
    except IndexError:
        cname = chrName.replace("chr", "")
        chrLen = [i.length for i in hic.getChromosomes() if i.name == cname][0]
    mdz = hic.getMatrixZoomData(cname, cname, "observed", "NONE", "BP",
                                res).getRecords(0, chrLen, 0, chrLen)
    p1 = np.asarray([int(i.binX / res) for i in mdz], dtype=int)
    p2 = np.asarray([int(i.binY / res) for i in mdz], dtype=int)
    c = np.asarray(
        [i.counts / 2 if i.binX == i.binY else i.counts for i in mdz],
        dtype=float)
    y = sparse.csr_array((c, (p1, p2)),
                         shape=[int(chrLen / res) + 1,
                                int(chrLen / res) + 1])
    y = y + y.T
    return y.toarray()


class RunBatch(object):

    def __init__(self, args):
        MFPT.__config__["min_coverage"] = args.min_coverage
        MFPT.__config__["KR_tol"] = args.KR_tolerance
        MFPT.__config__["device"] = args.device
        self.res = args.resolution
        self.threads = args.threads
        self.input_dir = args.input
        self.input_files = [
            i for i in os.listdir(self.input_dir) if i.endswith(".txt")
        ]
        self.input_names = [os.path.splitext(i)[0] for i in self.input_files]
        self.input_files = [
            os.path.join(self.input_dir, i) for i in self.input_files
        ]
        self.output_file = os.path.join(args.output_dir,
                                        f"{args.name}_batch.txt")
        self.length = args.chrlen
        return

    def _loadContactData(self):
        self.cm = Parallel(n_jobs=self.threads)(
            delayed(readBedFile)(i, self.res, self.length)
            for i in self.input_files)

        def forOne(mat):
            if MFPT.__config__["min_coverage"] > 0:
                f = MFPT.mask_low_coverage(
                    mat, min_coverage=MFPT.__config__["min_coverage"])
            else:
                f = np.ones(mat.shape[0]).astype(bool)
            f = MFPT.get_largest_compnoent(mat,
                                           return_indicator=True,
                                           pre_masked=f)
            y = MFPT.KRNorm(mat[f, :][:, f], tol=MFPT.__config__["KR_tol"])
            M = MFPT.get_mfpt_large_mem(y)
            M = MFPT.symmetrize(M)
            return np.log2(M), tuple(f)

        x = Parallel(n_jobs=self.threads)(delayed(forOne)(i) for i in self.cm)
        f = list(Counter([i[1] for i in x]).items())
        f.sort(key=lambda v: v[1])
        f = f[-1][0]
        y = {
            n: m
            for n, (m, flag) in zip(self.input_names, x)
            if flag == f and np.isfinite(m).all()
        }
        return y

    def __call__(self):
        matrices = self._loadContactData()
        mat = np.array(list(matrices.values()))
        dot_prod = np.einsum("imk,jmk->ij", mat, mat)
        norm_sq = np.diag(dot_prod)
        n = np.sqrt(norm_sq[:, None] + norm_sq[None, :] - 2 * dot_prod)
        d = np.sqrt(norm_sq[:, None] + norm_sq[None, :] + 2 * dot_prod) / 2
        y = pd.DataFrame(n / d,
                         index=list(matrices.keys()),
                         columns=list(matrices.keys()))
        y.to_csv(self.output_file, header=True, index=True, sep="\t")
        return


def getMFPT(mat):
    flag = MFPT.mask_low_coverage(mat,
                                  min_coverage=MFPT.__config__["min_coverage"])
    flag = MFPT.get_largest_compnoent(mat,
                                      pre_masked=flag,
                                      return_indicator=True)
    cm = mat[flag, :][:, flag]
    lm = cm - np.diag(np.diag(cm))
    y = MFPT.KRNorm(lm, tol=MFPT.__config__["KR_tol"])
    try:
        M = MFPT.get_mfpt_large_mem(y)
    except:
        M = MFPT.get_mfpt(y)
    P = MFPT.symmetrize(M)
    return MFPT.rescale_back_and_calc_plr(P, flag)


def run_mfpt(args):
    MFPT.__config__["min_coverage"] = args.min_coverage
    MFPT.__config__["KR_tol"] = args.KR_tolerance
    MFPT.__config__["device"] = args.device
    with h5py.File(os.path.join(args.output_dir, f"{args.name}.hdf"),
                   'w') as hdf:
        if args.file_type == "txt":
            P = getMFPT(readBedFile(args.input, args.resolution, args.chrlen))
            hdf.create_dataset("STRIDE", data=P)
        else:
            for chrName in args.ch:
                P = getMFPT(
                    readHiCFile(args.input,
                                res=args.resolution,
                                chrName=chrName))
                hdf.create_dataset(chrName, data=P)
    return


def run_stride(args):
    MFPT.__config__["min_coverage"] = args.min_coverage
    MFPT.__config__["KR_tol"] = args.KR_tolerance
    MFPT.__config__["device"] = args.device
    MFPT.__config__["norm"] = args.norm
    y = {}
    if args.file_type == "txt":
        M1 = readBedFile(args.input1, args.resolution, args.chrlen)
        M2 = readBedFile(args.input2, args.resolution, args.chrlen)
        y["STRIDE"] = MFPT.core(M1, M2)
    else:
        for chrName in args.ch:
            M1 = readHiCFile(args.input1, res=args.resolution, chrName=chrName)
            M2 = readHiCFile(args.input2, res=args.resolution, chrName=chrName)
            y[chrName] = MFPT.core(M1, M2)
            print(chrName)
    with open(os.path.join(args.output_dir, f"{args.name}_score.txt"),
              'wt') as fout:
        for k, v in y.items():
            fout.write(f"{k}\t{v}\n")
    return


def main(*args):
    parser = argparse.ArgumentParser(
        prog="stride",
        description=
        "STRIDE: A Robust Dissimilarity Measurement for Chromatin Conformation Capture Data Based on Sequencing Depth-Insensitive Representation."
    )
    subparsers = parser.add_subparsers(
        title="command",
        dest="command",
        required=True,
        description="The subcommand which should be executed.")
    parser_mfpt = subparsers.add_parser(
        "mfpt",
        description="Calculate the MFPT representation for a contact map.")
    parser_stride = subparsers.add_parser(
        "stride",
        description="Calculate the STRIDE distances for two given contact maps."
    )
    parser_batch = subparsers.add_parser(
        "batch",
        description=
        "Calculate the pairwise STRIDE distances for a batch of contact maps.")
    for p in [parser_stride, parser_mfpt, parser_batch]:
        p.add_argument(
            "-d",
            "--device",
            action="store",
            default="cpu",
            help=
            "The device on which the calculation will be executed if pytorch is available, or it will be omitted."
        )
        p.add_argument(
            "-c",
            "--min-coverage",
            action="store",
            type=float,
            default=0.02,
            help=
            "Proportion of bins with low coverage to be filtered in the KR normalization."
        )
        p.add_argument(
            "-k",
            "--KR-tolerance",
            action="store",
            type=float,
            default=1e-12,
            help=
            "The precision of the KR normalization. When standard deviations of row sums go below it, the normalization will be stopped."
        )
        p.add_argument("-t",
                       "--file-type",
                       default="hic",
                       choices=("hic", "txt"),
                       action="store",
                       help="The format of the input file(s). ")
        p.add_argument(
            "--ch",
            action=CommaSeparationAction,
            default="",
            help=
            "The chromosomes which should be processed when the format of the input file(s) are .hic. Multiple chromosomes can be provieded through a comma seperated list. It will be omitted if the input format is txt."
        )
        p.add_argument(
            "-l",
            "--chr-length",
            dest="chrlen",
            action="store",
            type=int,
            default=0,
            help=
            "The length of the chromosomes. The value will be taken if the input format is txt, or it will be omitted. "
        )
        p.add_argument(
            "-r",
            "--resolution",
            action="store",
            default=50000,
            type=int,
            help=
            "The resolution used when the format of the input file(s) are .hic. It will be omitted if the input format is txt."
        )
        p.add_argument(
            "-o",
            "--output-dir",
            default=".",
            action=OutputDirectoryAction,
            help=
            "The output directory. It will be created automatically if not exist."
        )
        p.add_argument(
            "-n",
            "--name",
            action="store",
            default="STRIDE",
            help=
            "The name of the project. It will be used as the names of the output files."
        )
    parser_mfpt.add_argument("input",
                             action="store",
                             help="The path to the input file.")
    parser_batch.add_argument("input",
                              action="store",
                              help="The path to the input folder.")
    parser_batch.add_argument(
        "-p",
        "--n-threads",
        dest="threads",
        action="store",
        default=1,
        type=int,
        help="The number of threads used in loading the contact maps.")
    for i in [1, 2]:
        parser_stride.add_argument(
            f"input{i}",
            action="store",
            help=f"The path to the {'first' if i==1 else 'second'} input file."
        )
    parser_stride.add_argument(
        "--norm",
        default=2,
        action=GetNormAction,
        help=
        "The matrix norm used in the calculation. It must be supported by scipy.linalg.norm."
    )
    args = parser.parse_args()
    if args.command == "stride":
        run_stride(args=args)
    elif args.command == "mfpt":
        run_mfpt(args=args)
    elif args.command == "batch":
        RunBatch(args=args)()
    else:
        sys.exit(255)


if __name__ == "__main__":
    main()
