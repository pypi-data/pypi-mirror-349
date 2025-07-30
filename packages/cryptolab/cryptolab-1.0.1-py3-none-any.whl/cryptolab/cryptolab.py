import requests
import pandas as pd
import os
from datetime import datetime, timedelta

class CryptoLab:
    _BASE_API_ = 'https://api.crypto-lab.app/'
    _COLUMNS_TRADE_ = {'timestamp': 'int64', 'base_currency': 'category', 'counter_currency': 'category', 'trade_time':'int64', 'trade_id':'int64', 'price':'float64', 'size':'float64'}
   
    
    def __init__(self, apiKey:str, callback_error=None):
        self.headers = {'X-API-Key': apiKey}
        self.callback_error = callback_error
    
    def init_replayer(self, callback, exchange: str, market: str, start_date: str, end_date: str):
        self.callback = callback
        self.exchange = exchange
        self.market = market
        self.start_date = start_date
        self.end_date = end_date
        self.dates = self.__get_dates_to_replay(self.start_date, self.end_date)
        
        # Download files
        status_download = self.__download_files(self.exchange, self.market, self.start_date, self.end_date)
        if(not status_download):
            return

        # For each date selected
        for date in self.dates:
            
            # Read df
            trades = self.__read_df('cache-cl/{}/trade/{}/{}.csv.gz'.format(self.exchange, self.market, date))
            if(trades is None):
                self.__on_error('File cache-cl/{}/trade/{}/{}.csv.gz doesn\'t exist. Make sure a file exist for this exchange, market and date using API'.format(self.exchange, self.market, date))
                continue
            
            # Read event and callback for each trade        
            for last_trade in trades:
                self.callback(last_trade)
            
            # Free memory
            del trades
    
    def __read_df(self, filename: str):
        if(not os.path.exists(filename)):
            print('file ' + filename + ' not found')
            return False

        return pd.read_csv(filename, compression='gzip', sep='\t', quotechar='"', dtype=CryptoLab._COLUMNS_TRADE_).to_dict('records')
    
    # Get list of files matching to the parameters
    def get_files(self, exchange: str, market: str, start_date: str, end_date: str):
        try:
            data = requests.get(CryptoLab._BASE_API_ + 'data/' + exchange + '/' + market + '/' + start_date + '/' + end_date, headers=self.headers).json()
            if(data['success'] == True):
                return data['results']
            self.__on_error(data['message'])
            return False
        except Exception as err:
            print(err)
            return False
       
    # Get list of exhanges
    def get_exchanges(self):
        try:
            data = requests.get(CryptoLab._BASE_API_ + 'data/exchanges', headers=self.headers).json()
            if(data['success'] == True):
                return data['results']
            self.__on_error(data['message'])
            return False
        except Exception as err:
            print(err)
            return False
        
    # Get list of markets for an exchange
    def get_markets(self, exchange: str):
        try:
            data = requests.get(CryptoLab._BASE_API_ + 'data/' + exchange + '/markets', headers=self.headers).json()
            if(data['success'] == True):
                return data['results']
            self.__on_error(data['message'])
            return False
        except Exception as err:
            print(err)
            return False
        
    # Return df from file (download or find in cache)
    def __download_files(self, exchange: str, market: str, start_date: str, end_date: str):   
        # Download files usefull between params dates
        files = self.get_files(exchange, market, start_date, end_date)
        if(not files):
            self.__on_error('No file for this request')
            return False
        
        for file in files:
            # Try to download file in not in cache
            try:
                output_file = 'cache-cl/{}/{}/{}/{}.csv.gz'.format(exchange, 'trade', market, file['date'])
                if(not os.path.exists(output_file)):
                    req = requests.get(CryptoLab._BASE_API_ + 'data/file/' + exchange + '/' + market + '/' + file['date'], headers=self.headers,allow_redirects=True)
                    if(req.status_code == 200):
                        self.__create_subdirectory(output_file)
                        open(output_file, 'wb').write(req.content)
                        self.callback(None, 'File downloaded: ' + exchange + ' ' + market + ' ' + file['date'])
                    else:
                        self.__on_error(req.content)
                        return False
            except Exception as err:
                self.__on_error(req.content)
                return False
        return True
            
    # On download file, create subdirectory for the cache
    def __create_subdirectory(self, filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except Exception as err:
                print('Error creating directory: ' + err)
           
    # Return an array with all date to replay     
    def __get_dates_to_replay(self, start_date: str, end_date: str):
        end_d = datetime.strptime(end_date, '%Y-%m-%d')
        tmp_d = datetime.strptime(start_date, '%Y-%m-%d')
        res = []
        while(tmp_d <= end_d):
            res.append(str(tmp_d.strftime('%Y-%m-%d')))
            tmp_d += timedelta(days=1)
        return res
    
    # Call on error
    def __on_error(self, data):
        if(self.callback_error):
            self.callback_error(data)
        else:
            print(data)