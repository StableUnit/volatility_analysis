import requests as r
import csv
import time

data = []

# fieldNames = ['id', 'timems', 'amount', 'price']

startTime = 1523116468121
currentTime = 1535869293000
t0 = time.time()

# while True:
while startTime < currentTime:
    with open('daiHistory.csv', mode='a') as f:
        response = r.get('https://api.bitfinex.com/v2/trades/tDAIUSD/hist?limit=1000&sort=1&start={}'.format(startTime)).json()
        if 'error' not in response:
            startTime = response[-1][1]
            print(startTime)
            print(len(response))
            response = response[:-1]
            writer = csv.writer(f, delimiter=',')

            for row in response:
                writer.writerow(row)
        time.sleep(5)

print(time.time()-t0)
# with open('daiHistory.csv') as f:
#     reader = csv.reader(f, delimiter=',')
#     for row in reader:
#         print(row)






















# import pandas as pd
# import krakenex
#
# import datetime
# import calendar
# import time
#
# # takes date and returns nix time
# def date_nix(str_date):
#     return calendar.timegm(str_date.timetuple())
#
# # takes nix time and returns date
# def date_str(nix_time):
#     return datetime.datetime.fromtimestamp(nix_time).strftime('%m, %d, %Y')
#
# # return formatted TradesHistory request data
# def data(start, end, ofs):
#     req_data = {'type': 'all',
#                 'trades': 'true',
#                 'start': str(date_nix(start)),
#                 'end': str(date_nix(end)),
#                 'ofs': str(ofs)
#                 }
#     return req_data
#
# k = krakenex.API()
# k.load_key('kraken.key')
#
# data = []
# count = 0
# for i in range(1,11):
#     start_date = datetime.datetime(2016, i+1, 1)
#     end_date = datetime.datetime(2016, i+2, 29)
#     th = k.query_private('TradesHistory', data(start_date, end_date, 1))
#     time.sleep(.25)
#     print(th)
#     th_error = th['error']
#     if int(th['result']['count'])>0:
#         count += th['result']['count']
#         data.append(pd.DataFrame.from_dict(th['result']['trades']).transpose())
#
# trades = pd.DataFrame
# trades = pd.concat(data, axis = 0)
# trades = trades.sort_values(columns='time', ascending=True)
# trades.to_csv('data.csv')