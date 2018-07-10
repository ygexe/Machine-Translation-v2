import os
import pickle
import zipfile

import jieba
import nltk
from tqdm import tqdm

from config import start_word, stop_word, unknown_word
from config import train_folder, valid_folder, test_a_folder, test_b_folder
from config import train_translation_folder, train_translation_zh_filename


def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def extract(folder):
    filename = '{}.zip'.format(folder)
    print('Extracting {}...'.format(filename))
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('data')


def build_train_vocab_zh():
    translation_path = os.path.join(train_translation_folder, train_translation_zh_filename)

    with open(translation_path, 'r') as f:
        data = f.readlines()

    print('building {} train vocab (zh)')
    vocab = set()
    max_len = 0
    longest_sentence = None
    for sentence in tqdm(data):
        seg_list = jieba.cut(sentence)
        length = 0
        for word in seg_list:
            vocab.add(word)
            length = length + 1

        if length > max_len:
            longest_sentence = sentence
            max_len = length

    vocab.add(start_word)
    vocab.add(stop_word)
    vocab.add(unknown_word)

    print('max_len(zh): ' + str(max_len))
    print('len(vocab): ' + str(len(vocab)))
    print('longest_sentence: ' + longest_sentence)

    filename = 'data/vocab_train_zh.p'
    with open(filename, 'wb') as encoded_pickle:
        pickle.dump(sorted(vocab), encoded_pickle)


def build_train_vocab_en():
    translation_path = os.path.join(train_translation_folder, train_translation_zh_filename)

    with open(translation_path, 'r') as f:
        data = f.readlines()

    print('building {} train vocab (en)')
    vocab = set()
    max_len = 0
    longest_sentence = None
    for sentence in tqdm(data):
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            vocab.add(token)
        length = len(tokens)
        if length > max_len:
            longest_sentence = sentence
            max_len = length

    vocab.add(start_word)
    vocab.add(stop_word)
    vocab.add(unknown_word)

    print('max_len(en): ' + str(max_len))
    print('len(vocab): ' + str(len(vocab)))
    print('longest_sentence: ' + longest_sentence)

    filename = 'data/vocab_train_en.p'
    with open(filename, 'wb') as encoded_pickle:
        pickle.dump(sorted(vocab), encoded_pickle)


if __name__ == '__main__':
    ensure_folder('data')

    if not os.path.isdir(train_folder):
        extract(train_folder)

    if not os.path.isdir(valid_folder):
        extract(valid_folder)

    if not os.path.isdir(test_a_folder):
        extract(test_a_folder)

    if not os.path.isdir(test_b_folder):
        extract(test_b_folder)

    if not os.path.isfile('data/vocab_train_zh.p'):
        build_train_vocab_zh()

    if not os.path.isfile('data/vocab_train_en.p'):
        build_train_vocab_en()
