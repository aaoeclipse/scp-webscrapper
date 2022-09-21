from scp_scrapper import multiple_scp_scrape
from database_manager import save_df


scps_I = [x for x in range(2,1000)]

new_df = multiple_scp_scrape(scps_I)

new_df.to_csv('test.csv')
save_df(new_df)