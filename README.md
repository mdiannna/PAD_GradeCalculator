# PAD_GradeCalculator


## Requests
#### Serviciu de tip 1:
- `POST /init-student {“student”: “NumePrenume”, “grupa” :”FAF”}`
- `PUT /nota { “student”: “NumePrenume1”, “nota”:10, “type”: “teorie”, “nr_atestare”:1}      type teorie/practica`
- `GET /status {“student” :”NumePrenume”}  => {“status” :”processing}`
- `GET /nota-atestare/nr_atestare/NumePrenume // sau cu ? => {“student”: “NumePrenume”, “grupa”: “FAF171”, “nr_Atestare” :”nr_atestare”, “nota” : “nota”}`

#### Serviciu de tip 2:
- `POST /nota-examen { “student”: “NumePrenume1”, “nota”:7}`
- `GET /nota-examen/NumePrenume // sau cu ?`
- `POST /nota-atestare { “student”: “NumePrenume1”, “nota”: 9, “nr_atestare”}`
- `GET /nota-finala/NumePrenume1 => {“student”: “NumePrenume1”, “note_atestari”: [“atest1”: nota, “atest2”: “”] “nota_examen” : nota_examen ,“nota_finala”: 9.88} (daca o atestare lipseste, sau examenul, la nota finala ii returneaza eroare)`

#### Request register service: (de la servicii spre gateway)
- `POST /service-register cu parametrii {“service_name”, “ip”, “type”} (type poate sa fie type1 sau type2)`
