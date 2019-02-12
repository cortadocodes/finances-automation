# import datetime as dt
# import math
#
# import numpy as np
# import pandas as pd
#
# EXPORT_TYPE = 'csv'
#
#
# def _calculate_averages(table, categories, start_date, end_date, time_window=30):
#
#     all_categories = categories['income'] + categories['expense']
#
#     time_window = dt.timedelta(days=time_window)
#     total_duration_available = end_date - start_date + dt.timedelta(1)
#     number_of_windows = math.floor(total_duration_available / time_window)
#
#     if time_window > total_duration_available:
#         raise ValueError('time_window should be <= end_date - start_date')
#
#     period_totals = pd.DataFrame(columns=all_categories)
#
#     averages = pd.DataFrame(columns=(
#         ['tables_analysed', 'analysis_type']
#         + table_to_store.date_columns
#         + all_categories
#     ))
#
#     start_dates = np.array([start_date + i * time_window for i in range(number_of_windows)])
#
#     for i, start_date in enumerate(start_dates):
#         end_date = start_date + time_window
#         totals = calculate_category_totals(start_date, end_date)[all_categories]
#         period_totals = period_totals.append(totals)
#
#     for column in all_categories:
#         averages.loc[0, column] = period_totals[column].mean().round(2)
#
#     return averages