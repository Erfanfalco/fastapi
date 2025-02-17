
weekly_wage_cmd = ('''SELECT DATE_PART('week', (tr_ge_date + INTERVAL '2 days' - INTERVAL '12 weeks')::date) AS Week_Number,
                    SUM(interest) AS Total_Interest,
                    MIN(tr_ge_date) as tr_ge_date
                    FROM public.financial_status_data fs
                    WHERE fs.tr_ge_date = '{0}'
                    GROUP BY Week_Number 
                    ORDER BY tr_ge_date DESC
                    ''')


weekly_wage_cube_query = 'INSERT INTO "brokerCube".weekly_wage_cube (week_number, total_interest, tr_ge_date) VALUES (%s, %s, %s) ;'


checking_date_weekly_wage_cube = ('''SELECT * FROM "brokerCube".weekly_wage_cube
                                  WHERE week_number = DATE_PART('week', ('{0}'::date + INTERVAL '2 days' - INTERVAL '12 weeks')::date); 
                                  ''')


updating_amount_weekly_wage_cube = '''UPDATE "brokerCube".weekly_wage_cube SET total_interest = '{0}' WHERE tr_ge_date = '{1}';'''


creating_weekly_wage_cube = '''CREATE TABLE IF NOT EXISTS "brokerCube".weekly_wage_cube (week_number int4 NULL, total_interest float8 NULL, tr_ge_date date NULL);'''


