import pandas as pd

df = pd.read_csv('book_scraper/test.csv')
df.drop_duplicates(subset=['link', 'name'], inplace=True)
df.to_csv('test_ans.csv', index=False)