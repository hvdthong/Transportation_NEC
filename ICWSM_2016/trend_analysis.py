import pandas as pd
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

start = time.time()
tagged_tweets = pd.read_json('C:/Users/vdthoang/Google Drive/LARC - NEC Project/icwsm2016/data/tweet_short_event_tagged_for_icwsm2016.json')
end = time.time()
print end - start

# start = time.time()
# sentiment_tagged_tweets = pd.read_json('data/tweet_short_sentiment_tagged_for_icwsm2016.json')
# end = time.time()
# print end - start


# start = time.time()
# tagged_tweets['hour'] = tagged_tweets['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').hour + 8)
# tagged_tweets['dow'] = tagged_tweets['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# end = time.time()
# print end - start

# print tagged_tweets.head()

def plot_weekly_boxplot(data, valueField, filename):
    grouped = data.groupby(['woy','dow'])
    bp_data = [[] for i in range(7)]
    for idx, group in grouped:
        bp_data[idx[1]].append(group[valueField].count())
    # print bp_data
    pp = PdfPages(filename)
    plt.clf()
    fig = plt.figure(1, figsize=(9,6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(bp_data)
    ax.set_xticklabels(['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday'])
    # plt.show()
    pp.savefig()
    pp.close()


def plot_hourly_boxplot(data, valueField, filename):
    grouped = data.groupby(['hour','dow'])
    bp_data = [[] for i in range(24)]
    for idx, group in grouped:
        bp_data[idx[0]].append(group[valueField].count())
    # print bp_data
    pp = PdfPages(filename)
    plt.clf()
    fig = plt.figure(1, figsize=(9, 6))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(bp_data)
    ax.set_xticklabels(range(24))
    plt.show()
    # pp.savefig()
    # pp.close()

# all
# tagged_tweets['hour'] = tagged_tweets['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# tagged_tweets['dow'] = tagged_tweets['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# tagged_tweets['woy'] = tagged_tweets['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
#
# df_weekday = tagged_tweets[tagged_tweets['dow'] < 5]
# df_weekend = tagged_tweets[tagged_tweets['dow'] >= 5]
#
# plot_hourly_boxplot(df_weekday[['hour', 'dow']], 'distribution', 'hourly.pdf')

# sentiment = [[0,1],[2],[3,4]]
# sentiment_names = ['negative', 'neutral', 'positive']
# for i in range(3):
#     print sentiment[i]
#     df = sentiment_tagged_tweets[sentiment_tagged_tweets['sentiment'].isin(sentiment[i])]
#     df['hour'] = df['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
#     df['dow'] = df['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
#     df['woy'] = df['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
#     plot_weekly_boxplot(df[['woy','dow','sentiment']], 'sentiment', 'data/sentiment_' + sentiment_names[i] + '-trend.pdf')
#     df_weekday = df[df['dow'] < 5]
#     df_weekend = df[df['dow'] >= 5]
#     plot_hourly_boxplot(df_weekday[['hour','dow','sentiment']], 'sentiment', 'data/sentiment_' + sentiment_names[i] + '-trend-weekday-hourly.pdf')
#     plot_hourly_boxplot(df_weekend[['hour','dow','sentiment']], 'sentiment', 'data/sentiment_' + sentiment_names[i] + '-trend-weekend-hourly.pdf')


# #accident
print 'accident'
# accident = tagged_tweets[tagged_tweets['accident'] == 1]
# accident['hour'] = accident['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# accident['dow'] = accident['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# accident['woy'] = accident['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(accident[['woy','dow','accident']], 'accident', 'data/accident-trend.pdf')
# accident_weekday = accident[accident['dow'] < 5]
# accident_weekend = accident[accident['dow'] >= 5]
# plot_hourly_boxplot(accident_weekday[['hour','dow','accident']], 'accident', 'data/accident-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(accident_weekend[['hour','dow','accident']], 'accident', 'data/accident-trend-weekend-hourly.pdf')
#
# #crowd
# print 'crowd'
# crowd = tagged_tweets[tagged_tweets['crowd'] == 1]
# crowd['hour'] = crowd['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# crowd['dow'] = crowd['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# crowd['woy'] = crowd['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(crowd[['woy','dow','crowd']], 'crowd', 'data/crowd-trend.pdf')
# crowd_weekday = crowd[crowd['dow'] < 5]
# crowd_weekend = crowd[crowd['dow'] >= 5]
# plot_hourly_boxplot(crowd_weekday[['hour','dow','crowd']], 'crowd', 'data/crowd-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(crowd_weekend[['hour','dow','crowd']], 'crowd', 'data/crowd-trend-weekend-hourly.pdf')
#
#
# #slow
# print 'slow'
# slow = tagged_tweets[tagged_tweets['slow'] == 1]
# slow['hour'] = slow['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# slow['dow'] = slow['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# slow['woy'] = slow['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(slow[['woy','dow','slow']], 'slow', 'data/slow-trend.pdf')
# slow_weekday = slow[slow['dow'] < 5]
# slow_weekend = slow[slow['dow'] >= 5]
# plot_hourly_boxplot(slow_weekday[['hour','dow','slow']], 'slow', 'data/slow-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(slow_weekend[['hour','dow','slow']], 'slow', 'data/slow-trend-weekend-hourly.pdf')
#
# #missing
# print 'missing'
# missing = tagged_tweets[tagged_tweets['missing'] == 1]
# missing['hour'] = missing['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# missing['dow'] = missing['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# missing['woy'] = missing['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(missing[['woy','dow','missing']], 'missing', 'data/missing-trend.pdf')
# missing_weekday = missing[missing['dow'] < 5]
# missing_weekend = missing[missing['dow'] >= 5]
# plot_hourly_boxplot(missing_weekday[['hour','dow','missing']], 'missing', 'data/missing-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(missing_weekend[['hour','dow','missing']], 'missing', 'data/missing-trend-weekend-hourly.pdf')
#
# #wait
# print 'wait'
# wait = tagged_tweets[tagged_tweets['wait'] == 1]
# wait['hour'] = wait['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# wait['dow'] = wait['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# wait['woy'] = wait['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(wait[['woy','dow','wait']], 'wait', 'data/wait-trend.pdf')
# wait_weekday = wait[wait['dow'] < 5]
# wait_weekend = wait[wait['dow'] >= 5]
# plot_hourly_boxplot(wait_weekday[['hour','dow','wait']], 'wait', 'data/wait-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(wait_weekend[['hour','dow','wait']], 'wait', 'data/wait-trend-weekend-hourly.pdf')
#
# #skip
# print 'skip'
# skip = tagged_tweets[tagged_tweets['skip'] == 1]
# skip['hour'] = skip['createAtMilis'].map(lambda x: (pd.to_datetime(x, unit='ms').hour + 8) % 24)
# skip['dow'] = skip['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').dayofweek)
# skip['woy'] = skip['createAtMilis'].map(lambda x: pd.to_datetime(x, unit='ms').weekofyear)
# # plot_weekly_boxplot(skip[['woy','dow','skip']], 'skip', 'data/skip-trend.pdf')
# skip_weekday = skip[skip['dow'] < 5]
# skip_weekend = skip[skip['dow'] >= 5]
# plot_hourly_boxplot(skip_weekday[['hour','dow','skip']], 'skip', 'data/skip-trend-weekday-hourly.pdf')
# plot_hourly_boxplot(skip_weekend[['hour','dow','skip']], 'skip', 'data/skip-trend-weekend-hourly.pdf')