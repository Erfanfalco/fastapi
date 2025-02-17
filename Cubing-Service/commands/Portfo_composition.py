

portfo_composition_cmd = ('''SELECT stock_ins_max_l_code, Sum(stock_price) as stock_price, cs.date_to_ge, sum(cd.usable_credit) as usable_credit
                            from customer_stock cs
                            INNER join customer_credit_data cd
                            on cd.account_number = cs.account_number
                            WHERE TO_DATE(cs.date_to_ge, 'YYYY-MM-DD') = '{0}'
                            GROUP by cs.stock_ins_max_l_code, cs.date_to_ge;
                            ''')

portfo_composition_cube_query = '''INSERT INTO brokerCube.portfo_composition_cube (stock_code, stock_price, date_to_ge, usable_credit) VALUES (%s, %s, %s, %s)'''


checking_date_portfo_composition_cube = '''SELECT * FROM "brokerCube".portfo_composition_cube WHERE date_to_ge = '{0}';'''


updating_amount_portfo_composition_cube = ''' UPDATE "brokerCube".portfo_composition_cube SET usable_credit = '{0}' WHERE date_to_ge = '{1}'; '''

creation_portfo_composition_cube = ('''CREATE TABLE IF NOT EXISTS "brokerCube".portfo_composition_cube (
                            stock_code text NULL,
                            stock_price float8 NULL,
                            date_to_ge text NULL,
                            usable_credit float8 NULL
                            );''')
