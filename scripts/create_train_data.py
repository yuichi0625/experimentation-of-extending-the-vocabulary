from pathlib import Path

from absl import app
from absl import flags

FLAGS = flags.FLAGS
flags.DEFINE_string('data_dir', '../data', '')
flags.DEFINE_string('en_word2freq', 'en_word2freq.tsv', '')
flags.DEFINE_string('eo_word2freq', 'eo_word2freq.tsv', '')
flags.DEFINE_integer('num_train', 8000, '')
flags.DEFINE_integer('num_dev', 1300, '')
flags.DEFINE_integer('num_test', 1300, '')
flags.DEFINE_string('exclude_en_words', 'test/en-eo/paper.0', '')
flags.DEFINE_string('exclude_eo_words', 'test/eo-en/paper.0', '')


def load_word2freq(word2freq_path: Path) -> dict[str, int]:
    word2freq = {}
    for line in word2freq_path.read_text(encoding='utf-8').splitlines():
        word, freq = line.split('\t')
        word2freq[word] = freq

    return word2freq


def load_exclude_words(exclude_words_path: Path) -> set[str]:
    return set(exclude_words_path.read_text(encoding='utf-8').splitlines())


def save_train_data(
    data_dir: Path,
    en_words: list[str],
    eo_words: list[str],
    exclude_en_words: set[str],
    exclude_eo_words: set[str],
) -> None:
    en_words = [' '.join(word) for word in en_words]
    en_words = [word for word in en_words if word not in exclude_en_words]
    en_words = en_words[: FLAGS.num_train + FLAGS.num_dev + FLAGS.num_test]
    eo_words = [' '.join(word) for word in eo_words]
    eo_words = [word for word in eo_words if word not in exclude_eo_words]
    eo_words = eo_words[: FLAGS.num_train + FLAGS.num_dev + FLAGS.num_test]

    save_words(data_dir / 'train' / 'en200-eo8000' / 'train.0', en_words[:200])
    save_words(
        data_dir / 'train' / 'en200-eo8000' / 'train.1', eo_words[: FLAGS.num_train]
    )
    save_words(data_dir / 'train' / 'en850-eo8000' / 'train.0', en_words[:850])
    save_words(
        data_dir / 'train' / 'en850-eo8000' / 'train.1', eo_words[: FLAGS.num_train]
    )
    save_words(data_dir / 'train' / 'eo200-en8000' / 'train.0', eo_words[:200])
    save_words(
        data_dir / 'train' / 'eo200-en8000' / 'train.1', en_words[: FLAGS.num_train]
    )
    save_words(data_dir / 'train' / 'eo850-en8000' / 'train.0', eo_words[:850])
    save_words(
        data_dir / 'train' / 'eo850-en8000' / 'train.1', en_words[: FLAGS.num_train]
    )

    save_words(
        data_dir / 'dev' / 'en-eo' / 'dev.0',
        en_words[FLAGS.num_train : FLAGS.num_train + FLAGS.num_dev],
    )
    save_words(
        data_dir / 'dev' / 'en-eo' / 'dev.1',
        eo_words[FLAGS.num_train : FLAGS.num_train + FLAGS.num_dev],
    )
    save_words(
        data_dir / 'dev' / 'eo-en' / 'dev.0',
        eo_words[FLAGS.num_train : FLAGS.num_train + FLAGS.num_dev],
    )
    save_words(
        data_dir / 'dev' / 'eo-en' / 'dev.1',
        en_words[FLAGS.num_train : FLAGS.num_train + FLAGS.num_dev],
    )

    save_words(
        data_dir / 'test' / 'en-eo' / 'test.0',
        en_words[FLAGS.num_train + FLAGS.num_dev :],
    )
    save_words(
        data_dir / 'test' / 'en-eo' / 'test.1',
        eo_words[FLAGS.num_train + FLAGS.num_dev :],
    )
    save_words(
        data_dir / 'test' / 'eo-en' / 'test.0',
        eo_words[FLAGS.num_train + FLAGS.num_dev :],
    )
    save_words(
        data_dir / 'test' / 'eo-en' / 'test.1',
        en_words[FLAGS.num_train + FLAGS.num_dev :],
    )


def save_words(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(words), encoding='utf-8')


def main(_argv):
    data_dir = Path(FLAGS.data_dir)
    en_word2freq = load_word2freq(data_dir / FLAGS.en_word2freq)
    eo_word2freq = load_word2freq(data_dir / FLAGS.eo_word2freq)
    exclude_en_words = load_exclude_words(data_dir / FLAGS.exclude_en_words)
    exclude_eo_words = load_exclude_words(data_dir / FLAGS.exclude_eo_words)

    save_train_data(
        data_dir,
        list(en_word2freq.keys()),
        list(eo_word2freq.keys()),
        exclude_en_words,
        exclude_eo_words,
    )


if __name__ == "__main__":
    app.run(main)
