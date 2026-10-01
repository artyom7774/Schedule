# SuperZavych - Schedule Generator

**SuperZavych** is a digital assistant for automatic schedule generation. It helps educational process organizers create timetables while taking into account many constraints: teacher workloads, classroom availability, subject difficulty, and more.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

- **Repository:** [https://github.com/artyom7774/Schedule](https://github.com/artyom7774/Schedule)
- **Site:** [https://superzavych.pythonanywhere.com/](https://superzavych.pythonanywhere.com/)

## Features

The program provides a full workflow for scheduling — from entering initial data to exporting the final result:

- **Flexible configuration** — number of days per week, lessons per day, parallel classes, subjects, and shifts.
- **Class management** — set weekly subject loads for each class.
- **Classroom management** — create classroom groups and assign them to subjects.
- **Teacher setup** — specify subjects, classes, and available time for each teacher.
- **AI assistant** — import data from files and get answers to project-related questions.
- **Constants and groups** — freeze specific lessons and create profile groups.
- **Automatic generation** — simulated annealing algorithm on a graph.
- **Viewing and export** — view schedules for classes and teachers, export to `.xlsx`.

## 🚀 Installation

1. Download the latest release from the [Releases](https://github.com/artyom7774/Schedule/releases) section.
2. Run the application.
3. Fill in the tabs sequentially: **Settings** > **Classes** > **Classrooms** > **Teachers**.
4. Click **Run** and wait for the schedule to be generated.

> Detailed documentation is available at: [https://superzavych.pythonanywhere.com/](https://superzavych.pythonanywhere.com/)

## Quick Start

1. **Install the program** — download and run the application.
2. **Fill in the data** — configure all tabs sequentially.
3. **Start generation** — click **Run** and wait for the result.

## Program Structure

The interface is divided into **10 logical tabs**. Work on a project proceeds sequentially — from basic settings to export.

| Stage          | Tabs                                            | Purpose                                                |
|----------------|-------------------------------------------------|--------------------------------------------------------|
| **Settings**   | Settings > Classes > Classrooms > Teachers > AI | Enter initial data, import and edit with AI assistance |
| **Refinement** | Constants > Groups                              | Define specific lessons and create groups/profiles     |
| **Result**     | Run > View > Export                             | Generate, review, and export the schedule              |

### Settings

Basic parameters are specified: number of days per week, lessons per day, parallel classes, subjects, and shifts. For each subject, a name and difficulty are set. For each parallel, the number of classes and the study shift are specified.

### Classes

For each class and subject, you specify how many times per week the subject is taught.

### Classrooms

Classrooms and their groups are defined. You can add and remove groups, and include specific classrooms in them.

### Teachers

All teachers, their subjects, and available time are specified. For each subject, classes are selected and the priority of classroom groups (or no classroom requirement) is set.

## Algorithm

The algorithm is based on **simulated annealing on a graph**. Each generated schedule is scored against a number of criteria, each multiplied by a configurable weight. The algorithm's goal is to **minimize the resulting score**.

### Criterions

| Criterion                               | Description                                                                |
|-----------------------------------------|----------------------------------------------------------------------------|
| **Repeated lessons**                    | Penalty for two or more identical lessons in one day for a class           |
| **Incorrect number of lessons per day** | Penalty for unequal number of lessons across days                          |
| **Gaps in lessons**                     | Penalty for each gap in a class's schedule                                 |
| **Difficulty distribution**             | Penalty for uneven lesson difficulty across days                           |
| **Teacher free time**                   | Penalty for each gap in a teacher's schedule                               |
| **Group bonus**                         | Points deducted for each lesson with multiple groups simultaneously        |
| **Shift lesson overlaps**               | Penalty for each lesson overlap between shifts                             |
| **Gaps in groups**                      | Penalty for a lesson where one group has no activity but has later lessons |

## AI Assistant

The AI assistant makes it convenient to work with the project:

- **Interface** - chat with the AI and submit files for processing.
- **Capabilities** - answers user questions and questions about submitted files; imports data from a file into the project.
- **Supported formats**: `.db`, `.sqlite`, `.sqlite3`, `.xlsx`, `.xls`, `.txt`, `.csv`, `.json`, `.md`, `.markdown`, `.html`, `.xml`, `.pdf`, `.docx`.

## Export

- **Lesson times** - for each shift and lesson, you can set the time.
- **Export** - the schedule is exported by class and by teacher in `.xlsx` format.

## License

This project is licensed under the **Apache License 2.0**.
