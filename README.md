# PAD_GradeCalculator

## Requests
**!!!Nota: toti parametri la GET trebuie sa fie cu query string (?parametru1=valoare&parametru2=valoare2)**


#### Serviciu de tip 1:
- `POST /init-student {“student”: “NumePrenume”, “grupa” :”FAF”}`
- `PUT /nota { “student”: “NumePrenume1”, “nota”:10, “type”: “teorie”, “nr_atestare”:1}      type teorie/practica`
- `GET /status {“student” :”NumePrenume”}  => {“status” :”processing}`
- `GET /nota-atestare => {“student”: “NumePrenume”, “grupa”: “FAF171”, “nr_atestare” :”nr_atestare”, “nota” : “nota”}`

#### Serviciu de tip 2:
- `POST /nota-examen { “student”: “NumePrenume1”, “nota”:7}`
- `GET /nota-examen {"student": "NumePrenume"}`
- `POST /s2-nota-atestare { “student”: “NumePrenume1”, “nota”: 9, “nr_atestare”:1}`
- `GET /s2-nota-atestare { “student”: “NumePrenume1”, “nr_atestare”:1}`
- `GET /nota-finala => {“student”: “NumePrenume1”, “note_atestari”: [“atest1”: nota, “atest2”: “”] “nota_examen” : nota_examen ,“nota_finala”: 9.88} (daca o atestare lipseste, sau examenul, la nota finala ii returneaza eroare)`
- `POST /s2-validate-student-marks => {"student": "NumePrenume", "tip": "atestare"}    "tip" poate fi 'examen' sau 'atestare'

- `GET /get-all-exam-marks`
- `GET /get-all-midterm-marks`

- `GET /status {“student” :”NumePrenume”}  => {“status” :”processing}`


#### Request register service: (de la servicii spre gateway)
- `POST /service-register cu parametrii {“service_name”, “ip”, “type”} (type poate sa fie type1 sau type2)`


## Docker
Commands to run gateway in docker:
(use sudo if needed)

from folder Gateway:

`$docker build -t flask-gateway .`

`$docker-compose up`
