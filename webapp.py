from flask import Flask, render_template, request
import sqlite3
from theparser import get_vacancies_from_hhru

def load_vacancies_to_db(vacancies_data, db_path='InfoVac.db'):
#загрузим данные о вакансиях в базу данных SQLite3.  
#vacancies_data: Список словарей с данными о вакансиях.
        
    db = sqlite3.connect('InfoVac.db')
    curs = db.cursor()

    #curs.execute("DROP TABLE vacanciestab1")

    curs.execute('''
        CREATE TABLE IF NOT EXISTS vacanciestab1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            salary TEXT,
            job_experience TEXT,
            schedule TEXT,
            link TEXT
        )
    ''')

    # Очистка таблицы перед загрузкой новых данных
    curs.execute("DELETE FROM vacanciestab1")

    for vacancy in vacancies_data:
        curs.execute(
            "INSERT INTO vacanciestab1 (name, salary, job_experience, schedule, link) VALUES (?, ?, ?, ?, ?)",
            (vacancy['name'], vacancy['salary'], vacancy['job_experience'], vacancy['schedule'], vacancy['link'])
        )

    db.commit()
    db.close()

#load_vacancies_to_db(get_vacancies_from_hhru("python-разработчик"))

def get_vacancies_from_db(db_path='InfoVac.db', limit=20, salary=None, job_experience=None, schedule=None):
# функция получает данные о вакансиях из базы данных SQLite3 с фильтрацией.

    #db_path: Путь к файлу базы данных.
    #limit: Максимальное количество вакансий для получения.
    #experience: Фильтр по опыту работы.
    #salary: Фильтр по зарплате.
    #schedule: Фильтр по графику работы.
    
    db = sqlite3.connect("InfoVac.db")
    curs = db.cursor()

    query = "SELECT * FROM vacanciestab1"

    conditions = []
    if salary:
        conditions.append(f"salary LIKE '%{salary}%'")
    if job_experience:
        conditions.append(f"job_experience LIKE '%{job_experience}%'")
    if schedule:
        conditions.append(f"schedule LIKE '%{schedule}%'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += f" LIMIT {limit}"

    curs.execute(query)
    vacancies_ext = curs.fetchall()
    db.close()

    vacancies_list = []
    for vacancy in vacancies_ext:
        vacancies_list.append({
            'id': vacancy[0],
            'name': vacancy[1],
            'salary': vacancy[2],
            'job_experience': vacancy[3],
            'schedule': vacancy[4],
            'link': vacancy[5]
        })

    return vacancies_list

app = Flask(__name__)

@app.route("/search",methods=['GET', 'POST'])
@app.route("/",methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        vacancies_ins = get_vacancies_from_hhru(search_query)
        if vacancies_ins:
            load_vacancies_to_db(vacancies_ins)
    return render_template("search.html")

@app.route("/results",methods=['GET', 'POST'])
def results():
    job_experience = request.form.get('job_experience')
    salary = request.form.get('salary')
    schedule = request.form.get('schedule')

    vacancies_ld = get_vacancies_from_db(salary=salary, job_experience=job_experience, schedule=schedule)

    return render_template('results.html', vacancies_ld=vacancies_ld, salary=salary, job_experience=job_experience, schedule=schedule)
    

if __name__ == "__main__":
    app.run(debug=True)