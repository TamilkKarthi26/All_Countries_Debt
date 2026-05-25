CREATE DATABASE international_debt;
USE international_debt;

CREATE TABLE debt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_name VARCHAR(100),
    country_code VARCHAR(20),
    series_name TEXT,
    series_code VARCHAR(50),
    year INT,
    debt DOUBLE
);

SELECT SUM(debt) AS total_debt
FROM debt_data;

SELECT country_name, SUM(debt) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT country_name, SUM(debt) AS total_debt
FROM debt_data
GROUP BY country_name
ORDER BY total_debt ASC
LIMIT 10;

SELECT series_name, SUM(debt) AS total_debt
FROM debt_data
GROUP BY series_name
ORDER BY total_debt DESC
LIMIT 10;

SELECT year, SUM(debt) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY year;

SELECT COUNT(*) FROM debt_data;