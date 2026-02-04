from database.db import get_connection


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("pragma foreign_keys = on;")

    #crete table turno
    cursor.execute("""
        create table if not exists turno (
            id integer primary key autoincrement,
            nome text not null
        );
    """)

    #crete table professor
    cursor.execute("""
        create table if not exists professor (
            id integer primary key autoincrement,
            nome text not null,
            matricula text
        );
    """)
   #crete table disciplina
    cursor.execute("""
        create table if not exists disciplina (
            id integer primary key autoincrement,
            nome text not null,
            carga_horaria text not null
        );
    """)

   #crete table curso
    cursor.execute("""
        create table if not exists curso (
            id integer primary key autoincrement,
            nome text not null,
            carga_horaria text not null
        );
    """)

   #crete table turma
    cursor.execute("""
        create table if not exists turma (
            id integer primary key autoincrement,
            nome text not null,
            empresa text not null,
            localidade text not null,
            id_curso integer not null,
            foreign key (id_curso) references curso(id)
        );
    """)

   #crete table professor_disciplina
    cursor.execute("""
        create table if not exists professor_disciplina (
            id integer primary key autoincrement,
            id_disciplina integer not null,
            id_professor integer not null,
            foreign key (id_disciplina) references disciplina(id),
            foreign key (id_professor) references professor(id)
        );
    """)

   #crete table curso_disciplina
    cursor.execute("""
        create table if not exists curso_disciplina (
            id integer primary key autoincrement,
            id_disciplina integer not null,
            id_curso integer not null,
            foreign key (id_disciplina) references disciplina(id),
            foreign key (id_curso) references curso(id)
        );
    """)

   #crete table aula
    cursor.execute("""
        create table if not exists aula (
            id integer primary key autoincrement,
            id_professor integer not null,
            id_disciplina integer not null,
            id_curso integer not null,
            id_turno integer not null,
            id_turma integer not null,
            data text not null,
            foreign key (id_professor) references professor(id),
            foreign key (id_disciplina) references disciplina(id),
            foreign key (id_curso) references curso(id),
            foreign key (id_turno) references turno(id),
            foreign key (id_turma) references turma(id)
        );
    """)

   #crete table professor_indisponibilidade
    cursor.execute("""
        create table if not exists professor_indisponibilidade (
            id integer primary key autoincrement,
            id_professor integer not null,
            data text not null,
            id_turno integer not null,
            motivo text,
            foreign key (id_professor) references professor(id),
            foreign key (id_turno) references turno(id)
        );
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
