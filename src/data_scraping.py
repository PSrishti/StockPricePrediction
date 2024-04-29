import numpy as np     import requestsfrom finrl.meta.preprocessor.yahoodownloader import YahooDownloaderimport yfinance as yffrom urllib.request import urlopen, Requestfrom bs4 import BeautifulSoupfrom datetime import dateimport pandas as pdimport osimport sys#import jsonfrom nltk.sentiment.vader import SentimentIntensityAnalyzerimport nltkcurrent_dir = os.path.abspath(sys.argv[0])data_folder = os.path.join(current_dir, 'data')"""Part 1: Web Scraping the Stock Price Data"""def get_sp500_tickers():    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')    soup = BeautifulSoup(resp.text, 'lxml')    table = soup.find('table', {'class': 'wikitable sortable'})    tickers = []    for row in table.findAll('tr')[1:]:        ticker = row.findAll('td')[0].text        tickers.append(ticker)            tickers = np.char.replace(tickers, ".", "-")    ticker_list = np.sort(tickers)    ticker_list = np.array([ticker.replace('\n', '') for ticker in ticker_list])    return ticker_listdef download_stock_prices(ticker_list, start_date, end_date):    df = YahooDownloader(start_date = start_date,                     end_date = end_date,                     ticker_list = ticker_list).fetch_data()    df['date'] = pd.to_datetime(df['date'])    return df"""Web Scraping Latest News Headlines and calculating their sentiment score"""def scrape_news_headlines(ticker):    nltk.download('vader_lexicon')    finwiz_url = 'https://finviz.com/quote.ashx?t='    url = finwiz_url + ticker    req = Request(url=url, headers={'user-agent': 'Mozilla/5.0'})    response = urlopen(req)    # Read the contents of the file into 'html'    html = BeautifulSoup(response)    # Find 'news-table' in the Soup and load it into 'news_table'    news_table = html.find(id='news-table')    return news_table#Printing the scraped data for Appledef print_scraped_news_headlines(tic):    dat = news_tables['AAPL']    # Get all the table rows tagged in HTML with <tr> into 'aapl_tr'    dat_tr = dat.findAll('tr')        for i, table_row in enumerate(dat_tr):        # Read the text of the element 'a' into 'link_text'        a_text = table_row.a.text        # Read the text of the element 'td' into 'data_text'        td_text = table_row.td.text        # Print the contents of 'link_text' and 'data_text'        print(a_text)        print(td_text)        # Exit after printing n rows of data        if i == 5:            breakdef parse_news(file_name, news_table):    # Iterate through all tr tags in 'news_table'    for x in news_table.findAll('tr'):        # read the text from each tr tag into text        # get text from a only        text = x.a.get_text()        # splite text in the td tag into a list        date_scrape = x.td.text.split()        # if the length of 'date_scrape' is 1, load 'time' as the only element        if len(date_scrape) == 1:            time = date_scrape[0]        # else load 'date' as the 1st element and 'time' as the second        else:            date = date_scrape[0]            time = date_scrape[1]        # Extract the ticker from the file name, get the string up to the 1st '_'        ticker = file_name.split('_')[0]        # Append ticker, date, time and headline as a list to the 'parsed_news' list        parsed_news.append([ticker, date, time, text])def sentiment_analysis(news):    # Instantiate the sentiment intensity analyzer    vader = SentimentIntensityAnalyzer()        # Set column names    columns = ['ticker', 'date', 'time', 'headline']        # Convert the parsed_news list into a DataFrame called 'parsed_and_scored_news'    parsed_and_scored_news = pd.DataFrame(news, columns=columns)        # Iterate through the headlines and get the polarity scores using vader    scores = parsed_and_scored_news['headline'].apply(vader.polarity_scores).tolist()        # Convert the 'scores' list of dicts into a DataFrame    scores_df = pd.DataFrame(scores)        # Join the DataFrames of the news and the list of dicts    parsed_and_scored_news = parsed_and_scored_news.join(scores_df, rsuffix='_right')        # Convert the date column from string to datetime    parsed_and_scored_news['date'] = parsed_and_scored_news['date'].replace('Today', 'Feb-01-24')    parsed_and_scored_news['date'] = pd.to_datetime(parsed_and_scored_news.date, format='%b-%d-%y')    return parsed_and_scored_newsif __name__ == "__main__":    ticker_list = get_sp500_tickers()    start_date = '2018-02-08'    end_date = date.today()    df = download_stock_prices(ticker_list, start_date, end_date)    file_path = os.path.join(data_folder, 'StockPriceDataWebScraped.parquet')    df.to_parquet(file_path, index=False)    '''    #Scrape news headlines for all the companies and store as a dictionary in news_tables    news_tables = {}    try:        for ticker in ticker_list:            print(ticker)            news_table = scrape_news_headlines(ticker)            # Add the table to our dictionary            if news_table is not None:                news_tables[ticker] = news_table            else:                print(f"No 'news-table' found for {ticker}")                    except Exception as e:        print(f"Error fetching data for {ticker}: {e}")          print_scraped_news_headlines('AAPL')    # Iterate through the news    parsed_news = []    for file_name, news_table in news_tables.items():        parse_news(file_name, news_table)    parsed_news[:1]        #Sentiment Analysis of parsed news    parsed_and_scored_news = sentiment_analysis(parsed_news)        df1 = parsed_and_scored_news.drop(['time', 'headline'], axis=1).groupby(['ticker','date']).agg('mean').reset_index()    df1.rename({'ticker': 'tic'}, axis='columns', inplace = True)    df1.date = pd.to_datetime(df1.date)            file_path = os.path.join(data_folder, 'SentimentScoreData.csv')    df1.to_csv(file_path, index=False)'''    