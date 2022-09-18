from scp_scrapper import multiple_scp_scrape

scps_I = ['00{}'.format(x) if x <= 9 else '0{}'.format(x) for x in range(2,500)]

new_df = multiple_scp_scrape(scps_I)
new_df.to_csv('dataSCPIv2.csv')