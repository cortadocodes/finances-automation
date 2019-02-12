def calculate_category_totals_across_accounts(self, start_date=None, end_date=None, positive_expenses=True):
    self.export_type = 'csv'

    start_date = start_date or self.start_date
    end_date = end_date or self.end_date

    columns = (self.table_to_store.date_columns + ['tables_analysed'] + self.all_categories)
    columns.remove('credit_card')
    totals = pd.DataFrame(columns=columns)

    for category in self.all_categories:

        category_total = 0

        for table in self.tables_to_analyse:

            conditions = (
                (table.data['category'] == category)
                & (table.data[table.date_columns[0]] >= start_date)
                & (table.data[table.date_columns[0]] <= end_date)
            )

            table_category_total = (
                table.data[conditions][table.monetary_columns[0]].sum()
                - table.data[conditions][table.monetary_columns[1]].sum()
            )

            if positive_expenses:
                if category in self.categories['expense']:
                    table_category_total = - table_category_total

            category_total += table_category_total

        totals.loc[0, category] = round(category_total, 2)

    return totals