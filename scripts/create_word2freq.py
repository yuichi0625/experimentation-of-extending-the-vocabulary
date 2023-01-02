import re
from collections import Counter
from itertools import chain
from pathlib import Path
from typing import Literal

from absl import app
from absl import flags
from absl import logging

EN_ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
EO_ALPHABETS = 'abcĉdefgĝhĥijĵklmnoprsŝtuŭvz'
# For including English contracted forms (such as I've, he's)
WORD_REGEX = re.compile(r'\w+\'?\w+')
EN_WORD_REGEX = re.compile(rf'[{EN_ALPHABETS}\']{{2,}}')
EO_WORD_REGEX = re.compile(rf'[{EO_ALPHABETS}]{{2,}}')

FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', '../data', '')
flags.DEFINE_string(
    'leipzig_corpora_collection_dirname', 'leipzig', '', short_name='leipzig_dirname'
)
flags.DEFINE_string('tatoeba_dirname', 'tatoeba', '')


def create_word2freq(
    leipzig_dir: Path, tatoeba_dir: Path, lang: Literal['en', 'eo']
) -> dict[str, int]:
    sents = []
    sents.extend(extract_sentences(leipzig_dir, data_src='leipzig', lang=lang))
    sents.extend(extract_sentences(tatoeba_dir, data_src='tatoeba', lang=lang))
    uniq_sents = set(sents)
    logging.info(f'({lang}) num of sentences: {len(sents):,} -> {len(uniq_sents):,}')

    words = list(chain.from_iterable(sent.split(' ') for sent in uniq_sents))
    word2freq = Counter(words)
    word2freq = dict(sorted(word2freq.items(), key=lambda x: x[1], reverse=True))
    logging.info(f'({lang}) num of words: {len(words):,} -> {len(word2freq):,}')

    return word2freq


def extract_sentences(
    data_dir: Path,
    data_src: Literal['leipzig', 'tatoeba'],
    lang: Literal['en', 'eo'],
    lowercase: bool = True,
) -> list[str]:
    logging.info(f'({lang}) Start extracting: {data_src} ...')
    if data_src == 'leipzig':
        prefix = 'eng' if lang == 'en' else 'epo'
    else:
        prefix = lang
    suffix = '.txt' if data_src == 'leipzig' else '.tsv'
    filename = f'{prefix}*{suffix}'

    sents = []
    for path in data_dir.rglob(filename):
        with open(path, encoding='utf-8') as f:
            for line in f:
                if lowercase:
                    line = line.lower()
                sent = line.split('\t')[1 if data_src == 'leipzig' else 2]
                sent = clean_sentence(sent, lang=lang)
                sents.append(sent)
        logging.info(f'  Completed {path}')
        logging.info(f'    (e.g. {sents[-1]})')

    return sents


def clean_sentence(sent: str, lang: Literal['en', 'eo']) -> str:
    lang_word_regex = EN_WORD_REGEX if lang == 'en' else EO_WORD_REGEX

    words = WORD_REGEX.findall(sent)
    words = [word for word in words if lang_word_regex.fullmatch(word)]

    return ' '.join(words)


def deduplicate(word2freq: dict[str, int], words: set[str]) -> dict[str, int]:
    dedup_word2freq = {
        word: freq for word, freq in word2freq.items() if word not in words
    }
    logging.info(f'Deduplicated: {len(word2freq)} -> {len(dedup_word2freq)}')

    return dedup_word2freq


def save_word2freq(path: Path, word2freq: dict[str, int]) -> None:
    path.write_text(
        '\n'.join([f'{word}\t{freq}' for word, freq in word2freq.items()]),
        encoding='utf-8',
    )


def main(_argv):
    data_dir = Path(FLAGS.data_dir)
    leipzig_dir = data_dir / FLAGS.leipzig_corpora_collection_dirname
    tatoeba_dir = data_dir / FLAGS.tatoeba_dirname

    en_word2freq = create_word2freq(leipzig_dir, tatoeba_dir, lang='en')
    eo_word2freq = create_word2freq(leipzig_dir, tatoeba_dir, lang='eo')
    eo_word2freq = deduplicate(eo_word2freq, set(list(en_word2freq.keys())[:15000]))
    save_word2freq(data_dir / 'en_word2freq.tsv', en_word2freq)
    save_word2freq(data_dir / 'eo_word2freq.tsv', eo_word2freq)


if __name__ == "__main__":
    app.run(main)
