from scp_scrapper import multiple_scp_scrape

scps_I = [x for x in range(2,10)]

new_df = multiple_scp_scrape(scps_I)

new_df.to_csv('test2.csv')
# save_df(new_df)