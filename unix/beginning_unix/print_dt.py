#!/opt/anaconda3/envs/td/bin/python3
# to direct output to a file (append): ./print_dt.py >> ./cron.log

from datetime import datetime
print(datetime.now().strftime("%Y%m%d"))
