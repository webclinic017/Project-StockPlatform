import quandl


quandl.ApiConfig.api_key = '9Tz2zcj3zgq9VtxpsaMR'
data = quandl.get('BCHARTS/BITFLYERUSD', start_date='2020-05-07', end_date='2020-05-07')

print(data)