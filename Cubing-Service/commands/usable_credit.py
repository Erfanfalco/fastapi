
daily_usable_credit_cmd = ('''SELECT  customer_data.branch_name, SUM(usable_credit), date_to_ge
                    FROM customer_credit_data
                    INNER join customer_data ON customer_data.account_number = customer_credit_data.account_number
                    WHERE TO_DATE(customer_credit_data.date_to_ge, 'DD/MM/YYYY') = '{0}'
                    GROUP BY customer_data.branch_name, date_to_ge
                    ''')

usable_credit_cube_query = 'INSERT INTO "brokerCube".usable_credit_cube (branch_name, sum_credit, date) VALUES (%s, %s, %s) ;'


checking_date_usable_credit_cube = '''SELECT * FROM "brokerCube".usable_credit_cube WHERE date = '{0}';'''

updating_amount_usable_credit_cube = '''UPDATE "brokerCube".usable_credit_cube SET sum_credit = '{0}' WHERE date = '{1}';'''

creating_usable_credit_cube = ('''CREATE TABLE IF NOT EXISTS "brokerCube".usable_credit_cube (
                    "date" text NULL,
                    branch_name text NULL,
                    sum_credit float8 NULL
                    );''')
