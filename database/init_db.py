from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")
    
    #Create table turno
    cursor.execute("create table if not exists turno(" \
    "id integer primary key autoincrement," \
    "nome text not null);")

    #create table professor
    cursor.execute("create table if not exists professor(" \
    "id integer primary key autoincrement," \
    "nome text not null," \
    "matricula text);")

    #create table agenda
    cursor.execute("create table if not exists agenda(" \
    "id integer primary key autoincrement," \
    "dia text not null," \
    "id_turno integer not null," \
    "id_professor integer not null," \
    "foreign key(id_turno) references turno(id)," \
    "foreign key(id_professor) references professor(id));")

    #create table disciplina
    cursor.execute("create table if not exists disciplina(" \
    "id integer primary key autoincrement," \
    "nome text not null," \
    "carga_horaria text not null);")

    #create table professor_disciplina
    cursor.execute("create table if not exists professor_disciplina(" \
    "id integer primary key autoincrement," \
    "id_disciplina integer not null," \
    "id_professor integer not null," \
    "foreign key(id_disciplina) references disciplina(id)," \
    "foreign key(id_professor) references professor(id));")

    # create table curso
    cursor.execute("create table if not exists curso(" \
    "id integer primary key autoincrement," \
    "nome text not null," \
    "carga_horaria text not null);")

    #create table curso_disciplina
    cursor.execute("create table if not exists curso_disciplina(" \
    "id integer primary key autoincrement," \
    "id_disciplina integer not null," \
    "id_curso integer not null," \
    "foreign key(id_disciplina) references disciplina(id)," \
    "foreign key(id_curso) references curso(id));")

    #create table turma
    cursor.execute("create table if not exists turma(" \
    "id integer primary key autoincrement," \
    "nome text not null," \
    "empresa text not null," \
    "localidade text not null);")

    #create table aula
    cursor.execute("create table if not exists aula(" \
    "id integer primary key autoincrement," \
    "id_professor integer not null," \
    "id_disciplina integer not null," \
    "id_curso integer not null," \
    "id_agenda integer not null," \
    "id_turno integer not null," \
    "id_turma integer not null," \
    "foreign key(id_professor) references professor(id)," \
    "foreign key(id_disciplina) references disciplina(id)," \
    "foreign key(id_curso) references curso(id)," \
    "foreign key(id_agenda) references agenda(id)," \
    "foreign key(id_turno) references turno(id)," \
    "foreign key(id_turma) references turma(id));")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    conn.commit()
    conn.close()