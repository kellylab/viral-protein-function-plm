from biotransformers import BioTransformers
from tqdm import tqdm
import pickle
from typing import List
import numpy as np

### TO DO: conver the logging steps to Value Exceptions

def _embed_seqs(transformer: BioTransformers, sequences: List[str], batch_size: int) -> np.ndarray:
    vectors = np.empty(shape = (0,1024), dtype=np.float32)
    emb = transformer.compute_embeddings(sequences, pool_mode=('mean'), batch_size=batch_size)
    vectors = np.concatenate((vectors, emb['mean']), axis=0)
    
    return vectors

def _get_faa(path: str, max_length: int) -> List[str]:
    seqs = []
    seq = []

    with(open(path)) as file:
        for line in file:
            line = line.rstrip()
            if line.startswith('>'):
                if len(seq) > 0:
                    seqs.append(''.join(seq).replace('-', ''))
                    seq = []
            else:
                seq.append(line)
    seqs.append(''.join(seq).replace('-', ''))

    # protbert_bfd can only handle sequences < 5096aa
    if max_length > 0:
        seqs = [x[0:max_length] for x in seqs]

    return seqs

def protbert_bfd_embed(faa_path: str, max_length: int, num_gpus: int, batch_size: int) -> np.ndarray:

    seqs = _get_faa(faa_path, max_length=max_length)
    transformer_bfd = BioTransformers(backend='protbert_bfd', num_gpus=num_gpus)

    # if len(seqs) < 1:
    #     with open(log.output) as f:
    #         logging.info('{0} had no sequences after converting msa to sequences for input to embedding function.' ''.format(faa))

    s_vectors = _embed_seqs(transformer=transformer_bfd, sequences=seqs, batch_size=batch_size)

    # if len(s_vectors) != len(seqs):
    #     logging.info('{0} had non-equal len(vectors) and len(sequences).' ''.format(faa))

    return s_vectors
