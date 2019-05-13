import time
import datetime as dt
import pytz

utc=pytz.utc
eastern=pytz.timezone('US/Eastern')

format_without_tz   ='%Y/%m/%d %H:%M:%S'
format_with_tz      = '%Y/%m/%d %H:%M:%S %Z%z'

dt_time_str_full_list = ['2002/10/27 01:20:00 EDT', '2002/10/27 01:20:00 EST']
for dt_time_str_full in dt_time_str_full_list:
    dt_time_str = dt_time_str_full[0:-4]
    dt_time_tz  = dt_time_str_full[-3:]
    if dt_time_tz == 'EDT':
        is_dst_flag = True
    else:
        is_dst_flag = False
   
    dt_time = dt.datetime.strptime(dt_time_str, format_without_tz)
    # print(dt_time_str)
    # print(is_dst_flag)
    # print(dt_time)
    # dt_time = dt.datetime.now().strftime(format)
    dt_time_with_tz = eastern.localize(dt_time, is_dst=is_dst_flag)
    dt_time_with_tz2uct = dt_time_with_tz.astimezone(utc)
    # dt_time_edt = eastern.localize(, is_dst=True)
    print('{}=>{}'.format(dt_time_with_tz.strftime(format_with_tz), dt_time_with_tz2uct.strftime(format_with_tz)))
