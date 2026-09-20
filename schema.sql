use cse;
select * from doctor where salary between 30000 and 50000

select * FROM employees
WHERE department IN ('HR', 'Finance')
AND salary NOT BETWEEN 30000 AND 50000;

 -- from where groupby having order by
 
SELECT DISTINCT branch FROM students;
SELECT * FROM students 
WHERE name LIKE '_____';
-- name exactly 5 characters


select * from students
where (rating>=1800) and department in ('cse', 'it', 'aiml');


SELECT DISTINCT status FROM orders 
WHERE order_date >= '2025-01-01' AND order_date <= '2025-12-31';
-- select status from order table in 2025 that shows status that its active, pending , etc


SELECT category, AVG(price) AS average_price FROM products
WHERE price IS NOT NULL
GROUP BY category;
-- find the average price of products per category, excluding products with null prices


select MAX(salary) as second_highest_salary from employees
WHERE salary < (SELECT MAX(salary) FROM employees);
-- find the second highest salary in the employees table(without window functions)


SELECT Branch, AVG(CGPA) as Avg_CGPA FROM Students
GROUP BY Branch HAVING AVG(CGPA) > 7.5;
-- group students by branch, find average cgpa per branch, show only branches with avg cgpa>7.5


SELECT customer_id, COUNT(order_id) AS order_count FROM orders
GROUP BY customer_id HAVING COUNT(order_id) > 3;
-- find all customers who have placed more than 3 orders, group by customer_id, filter using having


SELECT department, MAX(salary) AS max_salary FROM employees
GROUP BY department HAVING MAX(salary) > (SELECT AVG(salary) FROM employees);
-- list departments where the maximum salary is greater than the company-wise average salary


SELECT department, job_title FROM employees
GROUP BY department, job_title HAVING COUNT(*) = 1;
-- group employees by department and job_title. find combinations where employee count is exactly 1


SELECT name, cgpa FROM students
ORDER BY cgpa DESC, name ASC
LIMIT 5;
-- list top 5 students by cgpa(descending). if cgpa is tied, order alphabetically by name

SELECT * FROM employees
ORDER BY hire_date ASC
LIMIT 10 OFFSET 20;
-- implement pagination: fetch records 21-30 from the employees table ordered by hire_date

SELECT DISTINCT salary FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
-- find the 3rd highest salary using order by + limit + offset(without a subquery)


SELECT * FROM orders WHERE customer_id = 'C123'
ORDER BY order_date DESC
LIMIT 10;
-- fetch the latest 10 orders placed by specific customer, ordered by most recent first


SELECT product_name, category, price FROM products
ORDER BY category ASC, price DESC
LIMIT 20;
-- list all products stored by category(A-Z), then by price descending within each category. limit to 20
