Pharma Inventory Management Tool - By Saksham Goyal
(Backend and UI)

Technology Used:
1) Python - Backend development
2) Flask - RESTful APIS and UI framework
3) XAMPP - MySQL Database, Apache Web Server
4) mySQL - Querying the database

API Information
1) '/' : To upload CSV file and index data to the database
2) '/getStockForSupplier/'  :  To query the database based on certain parameters

Query parameters:
1) 'supplier' : To filter based on a single or list of suppliers
2) 'searchParam' : To enter search phrase for filtering the data based on product names
3) 'expiryFlag' : Set this to True to get only unexpired products
4) 'page' : To set the page number for pagination

Example End Point Usage:
http://127.0.0.1:5000/getStockForSupplier?supplier=product_name_1,product_name_2&searchParam=dolo&expiryFlag=True&page=2
