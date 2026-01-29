# 📅 Teacher Scheduling System

A system designed to **manage teachers, shifts, and classes**, providing an organized and efficient way to control academic schedules and teaching workloads.

---

## 🎯 Purpose

The purpose of this system is to centralize and organize information related to **teachers**, **subjects**, **shifts**, and **classes**, helping to avoid schedule conflicts and improving academic management.

---

## 🚀 Features

* 👨‍🏫 Teacher registration and management
* 📚 Subject registration
* ⏰ Shift management (morning, afternoon, evening, or custom shifts)
* 🗓️ Class scheduling by teacher
* ❌ Schedule conflict validation
* 🔍 Schedule visualization by:

  * Teacher
  * Shift
  * Day of the week
* ✏️ Edit and delete scheduled classes
* 📊 Teaching workload reports per teacher

---

## 🛠️ Technologies Used

* **Language:** Python
* **Database:** SQLite
* **Interface:** CLI / Desktop / Web (depending on implementation)
* **ORM (optional):** SQLAlchemy

---

## 🗂️ System Data Structure

The database was designed using **SQLite** with well-defined relationships to ensure data integrity and avoid scheduling conflicts.

### Turno (Shift)

* `id` (PK)
* `nome`

Used to define time periods such as Morning, Afternoon, or Evening.

---

### Professor (Teacher)

* `id` (PK)
* `nome`
* `matricula`

Stores teacher identification data.

---

### Disciplina (Subject)

* `id` (PK)
* `nome`
* `carga_horaria`

Represents subjects taught by teachers.

---

### Curso (Course)

* `id` (PK)
* `nome`
* `carga_horaria`

Represents academic courses.

---

### Turma (Class Group)

* `id` (PK)
* `nome`
* `empresa`
* `localidade`

Represents student groups or classes.

---

### Agenda

* `id` (PK)
* `dia`
* `id_turno` (FK → Turno)
* `id_professor` (FK → Professor)

Defines the weekly availability of each teacher by day and shift.

---

### Professor_Disciplina

* `id` (PK)
* `id_professor` (FK → Professor)
* `id_disciplina` (FK → Disciplina)

Many-to-many relationship between teachers and subjects.

---

### Curso_Disciplina

* `id` (PK)
* `id_curso` (FK → Curso)
* `id_disciplina` (FK → Disciplina)

Many-to-many relationship between courses and subjects.

---

### Aula (Class Session)

* `id` (PK)
* `id_professor` (FK → Professor)
* `id_disciplina` (FK → Disciplina)
* `id_curso` (FK → Curso)
* `id_agenda` (FK → Agenda)
* `id_turno` (FK → Turno)
* `id_turma` (FK → Turma)

Represents an actual class session, linking teacher, subject, course, shift, agenda, and class group.

---

### 🔗 Relationship Summary

* One **Professor** can have many **Agenda** records
* One **Turno** can be linked to many **Agenda** and **Aula** records
* Professors and Disciplines have a **many-to-many** relationship
* Courses and Disciplines have a **many-to-many** relationship
* Each **Aula** connects all core entities, ensuring full schedule consistency

---

## ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/teacher-scheduling-system.git
   ```

2. Access the project directory:

   ```bash
   cd teacher-scheduling-system
   ```

3. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\\Scripts\\activate     # Windows
   ```

4. Install dependencies (if any):

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python main.py
   ```

---

## ▶️ How to Use

1. Run the system as an administrator
2. Register teachers and subjects
3. Configure available shifts
4. Schedule classes
5. View schedules and reports

---

## 📈 System Benefits

* Prevents scheduling conflicts
* Improves teaching workload control
* Centralized and organized data
* Easy to maintain and extend

---

## 📝 Future Improvements

* 📱 Graphical user interface (GUI)
* 📅 Calendar integration
* 📊 Dashboard with charts
* 🔔 Automatic notifications for schedule changes

---

💡 *Ideal for schools, colleges, and educational institutions that need efficient teacher scheduling and class management.*
