# from . import core
# my_ctools/__init__.py

# 将所有模块导入进来并重新绑定函数名到 my_ctools 层级

from . import cal_std_mean
from . import cal_cpr
from . import cal_all_largest_indicators
from . import cal_all_longest_indicators
from . import cal_longest_dd_recover
from . import cal_max_dd
from . import cal_rolling_gain_loss


cal_std_mean = cal_std_mean.cal_std_mean
cal_std_mean_simd = cal_std_mean.cal_std_mean_simd
cal_cpr = cal_cpr.cal_cpr
cal_all_largest_indicators = cal_all_largest_indicators.cal_all_largest_indicators
cal_all_longest_indicators = cal_all_longest_indicators.cal_all_longest_indicators
cal_longest_dd_recover = cal_longest_dd_recover.cal_longest_dd_recover
cal_max_dd = cal_max_dd.cal_max_dd
cal_rolling_gain_loss = cal_rolling_gain_loss.cal_rolling_gain_loss
