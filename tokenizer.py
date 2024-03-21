import os 
from pathlib import Path
from tokenizers import BertWordPieceTokenizer
from transformers import BertTokenizer
import tqdm

from data import get_data


import re
import transformers, datasets
import numpy as np
from torch.optim import Adam
import math

 
pairs = get_data('datasets/movie_conversations.txt', "datasets/movie_lines.txt")

# WordPiece tokenizer

### save data as txt file
os.mkdir('data')
text_data = []
file_count = 0


for sample in tqdm.tqdm([x[0] for x in pairs]):
    text_data.append(sample)

    # once we hit the 10K mark, save to file
    if len(text_data) == 10000:
        with open(f'data/text_{file_count}.txt', 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(text_data))
        text_data = []
        file_count += 1

paths = [str(x) for x in Path('data').glob('**/*.txt')]


### Training own tokenizer
tokenizer = BertWordPieceTokenizer(
    clean_text=True,
    handle_chinese_chars=False,
    strip_accents=False,
    lowercase=True
)


tokenizer.train(
    files=paths,
    min_frequency=5,
    limit_alphabet=1000,
    wordpieces_prefix="##",
    special_tokens=["[PAD]", "[CLS]", "[SEP]", "[MASK]", "[UNK]"]
)


os.mkdir("bert-it-1")
tokenizer.save_model("bert-it-1", "bert-it")
