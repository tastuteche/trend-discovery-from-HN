#load in libraries
import pandas as pd
import re
from nltk import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
#%matplotlib inline
# read in the data set
df_hn = pd.read_csv('../hacker-news-corpus/hacker_news_sample.csv',
                    parse_dates=['timestamp'], index_col=[8])
df = df_hn


def pre_text(text):
    return str(text).lower()


df['text_lower'] = df['text'].str.lower()
df['title_lower'] = df['title'].str.lower()


def distro_count(distro):
    return len(df[df['text_lower'].str.contains(distro) |
                  df['title_lower'].str.contains(distro)].index)


# df['text_unigram'] = df['text'].apply(
#     lambda x: word_tokenize(pre_text(x)))
# df['title_unigram'] = df['title'].apply(
#     lambda x: word_tokenize(pre_text(x)))

# import itertools
# wordlist = itertools.chain(*df["text_unigram"], *df["title_unigram"])
# word_count = Counter(wordlist)
# distro_count = Counter({word: count for word, count in word_count.items(
# ) if word in ['gentoo', 'ubuntu', 'fedora']})


df['year'] = df['timestamp'].map(lambda x: x.year)


def textFreq(df, topic_list):
    data = df
    #.copy()
    for i in topic_list:
        #data[i] = data['text_lower'].apply(lambda x: str(x).count(i))
        data[i] = data['text_lower'].apply(
            lambda x: len(re.findall(r'\b%s\b' % i, str(x))))
    return data


def GroupFreq(df, topic_list, grouping_column):
    topic_freq = textFreq(df, topic_list)
    topic_list_grouping_column = topic_list + [grouping_column]
    topic_freq = topic_freq[topic_list_grouping_column]
    topic_freq_col = topic_freq.groupby(topic_freq[grouping_column]).sum()
    return topic_freq_col

# for distro in topics_linux_distro:
#     print(distro_count(distro))

# plt.matshow(topic_freq_county.corr())


def plot_year(category, topics):
    topic_freq_year = GroupFreq(df, topics, 'year')
    topic_freq_year.plot()
    plt.ylabel("number of word counts")
    plt.xlabel("year")
    plt.savefig('topics_%s.png' % category, dpi=200)
    plt.clf()
    plt.cla()
    plt.close()


topics_language = ['python', 'ruby', 'java', 'r']
plot_year('language', topics_language)

topics_browser = ['firefox', 'chrome', 'ie']
plot_year('browser', topics_browser)

topics_linux_distro = ['gentoo', 'ubuntu', 'fedora']
plot_year('linux_distro', topics_linux_distro)

topics_phone = ['nokia', 'android', 'ios']
plot_year('phone', topics_phone)

topics_editor = ['emacs', 'vim', 'atom', 'light table']
plot_year('editor', topics_editor)

