from database import get_connection

def create_tables():
    conn = get_connection
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_jeys = ON;")
    
    #Create table turno
    cursor.execute("create table if not exists turno(" \
    "id integer primary key autoincrement," \
    "nome text not null);")

    #create table professor
    cursor.execute("create table professor(" \
    "id integer primary key autoincrement," \
    "nome text not null" \
    "matricula text);")

    #create table agenda_professor
    cursor.execute("create table if not exists agenda_professor(" \
    "id integer primary key autoincrement," \
    "dia text not null," \
    "id_turno integer not null," \
    "id_professor integer not null," \
    "foreign key(id_turno) references turno(id)," \
    "foreign key(id_professor) references professor(id))")

    #create table disciplina
    cursor.execute("create table if not exists disciplina(" \
    "id integer primary key autoincrement," \
    "nome text not null," \
    "carga_horaria text not null)")

    #create table professor_disciplina
    cursor.execute("create table if not exists professor_disciplina(" \
    "id integer primary key auto_increment," \
    "id_disciplina integer not null," \
    "id_professor integer not null" \
    "foreign key(id_disciplina) references disciplina(id)" \
    "foreign key(id_professor) references professor(id);)")

    # create table curso
    cursor.execute("create table if not exists curso(" \
    ");")

    conn.commit()
    conn.close()