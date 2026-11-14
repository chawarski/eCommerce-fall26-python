# from .webapp import app
import pymysql

def main() -> None:
    print("Hello from eCom")

    # Basic SQL query for local test DB
    conn = pymysql.connect(host='localhost', user='root', password='chargerhorse', database='inventory_db')
    cur = conn.cursor()
    sql = "SELECT * FROM `products`;" 
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
    cur.close()

    # Basic flask webapp
    # app.run(debug=True)


if __name__ == "__main__":
    main()