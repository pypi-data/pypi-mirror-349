"Python utilities for sourmash plugins and scripts."
import sourmash
from sourmash import sourmash_args
from sourmash.cli import utils as sourmash_cli

from enum import Enum

__all__ = ['FracMinHash',
           'add_standard_minhash_args']
           

DEFAULTS = dict(
    DNA=dict(ksize=31, scaled=1000),
    protein=dict(ksize=10, scaled=200),
    dayhoff=dict(ksize=16, scaled=200),
    hp=dict(ksize=42, scaled=200),
    skipm1n3=dict(ksize=21, scaled=1000),
    skipm2n3=dict(ksize=21, scaled=1000),
)
    
           
class FracMinHash(sourmash.MinHash):
    "An updated MinHash class with nicer constructor arguments."
    def __init__(self, *,
                 ksize=31,
                 scaled=1000,
                 moltype='DNA',
                 track_abundance=False,
                 **kwargs):

        kwargs = dict(kwargs)
        assert 'is_protein' not in kwargs
        assert 'dayhoff' not in kwargs
        assert 'hp' not in kwargs

        if scaled is None:
            raise ValueError(f"must specify scaled")
        else:
            scaled = int(scaled)

        if ksize is None:
            raise ValueError(f"must specify ksize")
        else:
            ksize = int(ksize)

        if moltype == 'DNA':
            kwargs['is_protein'] = False
            kwargs['dayhoff'] = False
            kwargs['hp'] = False
        elif moltype == 'protein':
            kwargs['is_protein'] = True
        elif moltype == 'dayhoff':
            kwargs['dayhoff'] = True
        elif moltype == 'hp':
            kwargs['hp'] = True
        elif moltype == 'skipm1n3':
            kwargs['skipm1n3'] = True
        elif moltype == 'skipm2n3':
            kwargs['skipm2n3'] = True
        else:
            raise ValueError(f"unknown moltype: '{moltype}'")

        super().__init__(n=0,
                         ksize=ksize,
                         scaled=scaled,
                         track_abundance=track_abundance,
                         **kwargs)

    def __str__(self):
        return f"k={self.ksize} scaled={self.scaled} moltype={self.moltype}"


def add_standard_minhash_args(parser):
    sourmash_cli.add_construct_moltype_args(parser)
    sourmash_cli.add_ksize_arg(parser)
    sourmash_cli.add_scaled_arg(parser)


def create_minhash_from_args(args, *, track_abundance=False, **defaults):
    default_moltype = defaults.get('moltype')
    moltype = sourmash_args.calculate_moltype(args, default=default_moltype)
    ksize = args.ksize or defaults.get('ksize')
    if not ksize:
        ksize = DEFAULTS[moltype]['ksize']
    scaled = args.scaled or defaults.get('scaled')
    if not scaled:
        scaled = DEFAULTS[moltype]['scaled']

    return FracMinHash(moltype=moltype,
                       ksize=ksize,
                       scaled=scaled,
                       track_abundance=track_abundance)


def load_index_and_select(filename, minhash_obj, *, raise_on_empty=True):
    """Load a sourmash Index object from filename,
    selecting sketches compatible with minhash_obj.
    """
    idx = sourmash.load_file_as_index(filename)
    idx = idx.select(ksize=minhash_obj.ksize,
                     moltype=minhash_obj.moltype,
                     scaled=minhash_obj.scaled,
                     abund=minhash_obj.track_abundance)
    if not idx:
        raise ValueError(f"no matching sketches in '{filename}' for k={minhash_obj.ksize} moltype={minhash_obj.moltype} scaled={minhash_obj.scaled}")
    return idx
