# SQL commands string to be executed against the database


future_settlements_cmd = ('''DECLARE @StartDate DATE = dateadd(day, 2, CAST(GETDATE() AS DATE));
                          DECLARE @EndDate DATE = dateadd(day, -4, CAST(GETDATE() AS DATE));
                          SELECT SUM(Amount),COUNT(Amount) ,CAST( RequestDate AS DATE)
                          FROM [HamtaDb].[dbo].[PaymentRequests]
                          WHERE [RequestDate] >= @EndDate AND [RequestDate] <= @StartDate
                          GROUP BY RequestDate
                          ORDER BY RequestDate asc
                          ''')


customer_remain_cmd = ('''SELECT  SUM(f.remain) AS total_remain,customer_data.branch_id,customer_data.branch_name
                        FROM financial_status_data f 
                        INNER JOIN customer_data ON customer_data.account_number = f.account_number 
                        GROUP BY customer_data.branch_id, customer_data.branch_name ORDER BY total_remain;
                        ''')


weekly_wage_cmd = ('''SELECT Week_Number,
                    Total_Interest,
                    tr_ge_date
                    FROM brokerCube.weekly_wage_cube
                    WHERE tr_ge_date <= {0}
                    ORDER BY tr_ge_date DESC
                    LIMIT 20;
                    ''')


daily_usable_credit_cmd = ('''SELECT date, branch_name, sum_credit
                    FROM brokerCube.usable_credit_cube
                    WHERE TO_DATE(date, 'DD/MM/YYYY') = {0};
                    ''')

daily_final_credit_cmd = ('''SELECT branch_name,final_credit,tr_ge_date
                    FROM brokerCube.final_credit_cube
                    WHERE TO_DATE(tr_ge_date, 'YYYY-MM-DD') = {0};
                    ''')


daily_transactions_cmd = (''' SELECT *
                    FROM brokerCube.transaction_cube
                    WHERE TO_DATE(date, 'YYYY-MM-DD') = {0};
                    ''')


daily_portfo_composition = ('''SELECT *
                    FROM brokerCube.portfo_composition_cube
                    where TO_DATE(date_to_ge, 'YYYY-MM-DD') = {0};
                    ''')


credit_kpi_cmd = ('''WITH usable_credit as (SELECT 
                    AVG(sum_credit)  as avg_credit, 
                    DATE_PART('week', ((TO_DATE(date, 'DD-MM-YYYY') + INTERVAL '2 days') - INTERVAL '12 weeks')::date) AS Week_Number,
                    Min(date) as date
                    FROM 
                        brokerCube.usable_credit_cube uc
                    GROUP by Week_Number
                    )
                    
                    SELECT (us.avg_credit/ww.total_interest) as kpi, ww.tr_ge_date, us.week_number
                    FROM brokerCube.weekly_wage_cube ww
                    INNER join usable_credit us
                    on us.Week_Number = ww.week_number
                    where ww.tr_ge_date <= {0}
                    order by ww.tr_ge_date desc
                    limit 20;
                    ''')


