from matplotlib import dates as mdates
from matplotlib import pyplot as plt


EXPORT_TYPE = 'image'


def _plot_balance(table, start_date, end_date):

    dates = table.data[table.date_columns[0]]
    balance = table.data['balance']

    dates_sorted, balance_sorted = zip(*sorted(zip(dates, balance)))

    figure = plt.figure(figsize=(12, 8))
    plt.plot(dates_sorted, balance_sorted)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Balance / £', fontsize=16)
    plt.title(
        'Balance of {} between {} and {}'.format(
            table.name, start_date, end_date
        ),
        fontsize=20
    )

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(0, 30, 5)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    ax.tick_params(axis='both', which='both', labelsize=14)

    plt.show()

    return figure