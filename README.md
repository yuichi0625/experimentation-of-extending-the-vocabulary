# Experimentation of [Extending the Vocabulary of Fictional Languages using Neural Networks](https://arxiv.org/abs/2201.07288)

I experimented the paper with English and Esperanto, which is more fictional than natural languages.

## data
I collected corpora from [Tatoeba](https://tatoeba.org/ja) and [Leipzig Corpora Collection](https://wortschatz.uni-leipzig.de/en).
- [Tatoeba - Download](https://tatoeba.org/ja/downloads)
- [Leipzig Corpora Collection - Download Corpora English](https://wortschatz.uni-leipzig.de/en/download/English)
- [Leipzig Corpora Collection - Download Corpora Esperanto](https://wortschatz.uni-leipzig.de/en/download/Esperanto)

The paper didn't mention how to split train / dev / test, so I counted word frequencies, sorted and split them accordingly.
- train: `data[:200]`, `data[:850]`, or `data[:8000]`
- dev: `data[8000:9300]`
- test: `data[9300:10600]` or manually collected from the paper

## training
[What the loss should be when the model converge normally?](https://github.com/shentianxiao/language-style-transfer/issues/5)
