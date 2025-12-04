import numpy as np
from tqdm import tqdm
import pickle
from typing import List, Tuple, Dict
import re

import torch
from transformers import BertTokenizer, BertModel

def _clean(seq):
    seq = seq.strip().upper().replace(" ", "").replace("-", "")
    seq = re.sub(r"[UZOB]", "X", seq)
    return " ".join(list(seq))


@torch.no_grad()
def _embed_seqs(
    seqs: List[str],
    tokenizer: BertTokenizer,
    model: BertModel,
    device: str,
    batch_size: int,
) -> np.ndarray:
    all_vecs = []
    for i in range(0, len(seqs), batch_size):
        batch = [_clean(s) for s in seqs[i:i + batch_size]]
        enc = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=1024,
            return_tensors="pt",
        )
        input_ids = enc["input_ids"].to(device)
        attn = enc["attention_mask"].to(device)

        out = model(input_ids=input_ids, attention_mask=attn).last_hidden_state  # (B,L,H)
        out = out[:, 1:-1, :]                      # drop CLS/SEP
        mask = attn[:, 1:-1].unsqueeze(-1)         # (B,L-2,1)

        pooled = (out * mask).sum(1) / mask.sum(1).clamp(min=1)  # (B,H)
        all_vecs.append(pooled.cpu().numpy().astype(np.float32))

    if not all_vecs:
        return np.zeros((0, model.config.hidden_size), dtype=np.float32)
    return np.concatenate(all_vecs, axis=0)


def _get_faa(path: str, max_length: int = 0) -> Tuple[List[str], List[str]]:
    idents: List[str] = []
    seqs: List[str] = []
    seq_chunks: List[str] = []

    with open(path) as file:
        for line in file:
            line = line.rstrip()
            if line.startswith('>'):
                idents.append(line)
                if len(seq_chunks) > 0:
                    seq = ''.join(seq_chunks).replace('-', '')
                    if max_length > 0:
                        seq = seq[:max_length]
                    seqs.append(seq)
                    seq_chunks = []
            else:
                seq_chunks.append(line)
    # last sequence
    if len(seq_chunks) > 0:
        seq = ''.join(seq_chunks).replace('-', '')
        if max_length > 0:
            seq = seq[:max_length]
        seqs.append(seq)

    # protbert_bfd can only handle sequences < 5096aa (pre-existing comment)
    return idents, seqs


def protbert_bfd_embed(faa_path: str, max_length: int, num_gpus: int, batch_size: int) -> Dict[str, np.ndarray]:
    identifiers, sequences = _get_faa(faa_path, max_length=max_length)

    protbert_bfd_tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert_bfd", do_lower_case=False)
    protbert_bfd_model = BertModel.from_pretrained("Rostlab/prot_bert_bfd")
    device = "cuda" if (num_gpus > 0 and torch.cuda.is_available()) else "cpu"
    protbert_bfd_model.to(device)
    protbert_bfd_model.eval()

    # batch sequence embedding to reduce memory, as in the original code
    d: Dict[str, np.ndarray] = {}

    sequence_batch = 100

    for i in range(int(len(sequences) / sequence_batch) + 1):
        start = i * sequence_batch
        end = (i + 1) * sequence_batch
        # account for instance when there is no remainder
        if start == len(sequences):
            continue

        s_vectors = _embed_seqs(
            seqs=sequences[start:end], 
            tokenizer=protbert_bfd_tokenizer,
            model=protbert_bfd_model,
            device=device,
            batch_size=batch_size)
        d.update(dict(zip(identifiers[start:end], s_vectors)))

    return d
