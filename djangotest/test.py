import pandas as pd

data = pd.read_csv("/home/hertz/MyGit/djangotest/trending.csv",engine="python",encoding='gb18030',error_bad_lines=False,names=['User','Date','Location','Text'],parse_dates=[0],index_col=0,squeeze=True)
