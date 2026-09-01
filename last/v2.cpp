#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#include "libs/CLI11.hpp"
#include "libs/json.hpp"

using namespace std;

using json = nlohmann::json;

// CONSTANTS

const int JOB_WEEK_LENGHT = 5;
const int MAX_LESSON_IN_DAY = 8;

// RANDOM

int randint(int min, int max) {
    static __gnu_cxx::sfmt19937 rng(
        std::random_device{}() ^
        static_cast<unsigned>(std::chrono::high_resolution_clock::now().time_since_epoch().count())
    );

    std::uniform_int_distribution<int> dist(min, max);
    return dist(rng);
}

// DATA

class Data {
public:
    json teachers, classes, lessons, subjects;
    vector<int> hards;

    Data() {
        subjects = json::parse(ifstream("data/subjects.json"));
        teachers = json::parse(ifstream("data/teachers.json"));
        classes = json::parse(ifstream("data/classes.json"));

        lessons = json::parse(ifstream("data/lessons.json"));

        json temp = json::parse(ifstream("data/hards.json"));

        hards.assign(subjects.size() + 1, 0);

        for (auto& [key, value] : temp.items()) {
            for (int i = 0; i < subjects.size(); i++) {
                if (key == subjects[i]) {
                    hards[i + 1] = value;
                }
            }
        }
    }
};

Data& getData() {
    static Data instance;

    return instance;
}

struct Teacher;
struct Slot;

struct Week;
struct Day;
struct Lesson;

map<int, string> teacherNameByID;
map<string, int> IDByTeacherName;

map<int, string> subjectNameByID;
map<string, int> IDBySubjectName;

vector<Teacher> teachers;
vector<Week> classes;

struct Teacher {
    int name = 0;

    vector<vector<bool>> work;

    Teacher() {
        work.assign(JOB_WEEK_LENGHT, vector<bool>(MAX_LESSON_IN_DAY, false));
    }

    Teacher(string name_) {
        name = IDByTeacherName[name_];

        work.assign(JOB_WEEK_LENGHT, vector<bool>(MAX_LESSON_IN_DAY, false));
    }

    Teacher(int name_) {
        name = name_;

        work.assign(JOB_WEEK_LENGHT, vector<bool>(MAX_LESSON_IN_DAY, false));
    }
};

struct Lesson {
    int subject = 0, teacher = 0;

    bool empty = true;

    Lesson() {
        subject = 0;
        teacher = 0;
    }

    Lesson(string subject_, string teacher_) {
        subject = IDBySubjectName[subject_];
        teacher = IDByTeacherName[teacher_];

        empty = false;
    }

    Lesson(int subject_, int teacher_) {
        subject = subject_;
        teacher = teacher_;

        empty = false;
    }

    json save() {
        return json{
            {"teacher", (teacher == 0 ? "#" : teacherNameByID[teacher])},
            {"subject", (subject == 0 ? "#" : subjectNameByID[subject])}
        };
    }
};

struct Day {
    vector<Lesson> lessons;

    Day() {
        lessons.assign(MAX_LESSON_IN_DAY, Lesson());
    }

    Day(vector<Lesson> lessons_) {
        lessons = lessons_;
    }

    json save() {
        json answer = json::array();

        for (auto lesson : lessons) {
            answer.push_back(lesson.save());
        }

        return answer;
    }
};

struct Week {
    vector<Day> days;

    string name = "";
    int idx = 0;

    Week() {
        days.assign(JOB_WEEK_LENGHT, Day());
    }

    Week(int idx_, string name_) {
        days.assign(JOB_WEEK_LENGHT, Day());

        name = name_;
        idx = idx_;
    }

    Week(int idx_, string name_, vector<Day> days_) {
        days = days_;

        name = name_;
        idx = idx_;
    }

    void init() {
        Data& data = getData();

        vector<pair<Lesson, int>> que;

        for (auto type : data.lessons[name]) {
            if (type["hours"] == nullptr) {
                continue;
            }

            que.push_back({Lesson(type["subject"], type["teacher"].get<string>()), type["hours"]});
        }

        int iter = 0;

        for (auto& [lesson, cnt] : que) {
            while (cnt > 0) {
                int day = randint(0, JOB_WEEK_LENGHT - 1);
                int lsn = randint(0, MAX_LESSON_IN_DAY - 1);

                if (teachers[lesson.teacher].work[day][lsn] == true || days[day].lessons[lsn].empty == false) {
                    continue;
                }

                cnt--;

                teachers[lesson.teacher].work[day][lsn] = true;

                days[day].lessons[lsn] = lesson;

                iter += 1;
            }
        }
    }

    bool can(int day1, int lesson1, int day2, int lesson2) {
        int teacher1 = days[day1].lessons[lesson1].teacher;
        int teacher2 = days[day2].lessons[lesson2].teacher;

        bool f1 = teachers[teacher1].work[day2][lesson2] == false;
        bool f2 = teachers[teacher2].work[day1][lesson1] == false;

        return f1 && f2;
    }

    json save() {
        json answer = json::array();

        for (auto day : days) {
            answer.push_back(day.save());
        }

        return answer;
    }
};

struct Weights {
    inline static double equalLessons = 5;
    inline static double notEqualsLessonsCountOnDay = 15;
    inline static double lessonsEmptySlots = 200;
    inline static double daysByHard = 5;
    inline static double teacherFreeTime = 5;

    inline static double equalLessonsCapacity = 1;
    inline static double notEqualsLessonsCountOnDayCapacity = 1;
    inline static double lessonsEmptySlotsCapacity = 1;
    inline static double daysByHardCapacity = 1;
    inline static double teacherFreeTimeCapacity = 1;

    static void init(const json& data) {
        equalLessons = data.value("equalLessons", equalLessons);
        notEqualsLessonsCountOnDay = data.value("notEqualsLessonsCountOnDay", notEqualsLessonsCountOnDay);
        lessonsEmptySlots = data.value("lessonsOrder", lessonsEmptySlots);
        daysByHard = data.value("daysByHard", daysByHard);
        teacherFreeTime = data.value("teacherFreeTime", teacherFreeTime);

        equalLessonsCapacity = data.value("equalLessonsCapacity", equalLessonsCapacity);
        notEqualsLessonsCountOnDayCapacity = data.value("notEqualsLessonsCountOnDayCapacity", notEqualsLessonsCountOnDayCapacity);
        lessonsEmptySlotsCapacity = data.value("lessonsOrderCapacity", lessonsEmptySlotsCapacity);
        daysByHardCapacity = data.value("daysByHardCapacity", daysByHardCapacity);
        teacherFreeTimeCapacity = data.value("teacherFreeTimeCapacity", teacherFreeTimeCapacity);
    }
};

class Functions {
public:
    static double equalLessons(vector<int>& subjects) {
        int value = 0;

        for (int i = 0; i < subjects.size(); i++) {
            for (int j = i + 1; j < subjects.size(); j++) {
                if (subjects[i] == 0 || subjects[j] == 0) {
                    continue;
                }

                if (subjects[i] == subjects[j]) {
                    value += 1;
                }
            }
        }

        return Weights::equalLessons * pow(value, Weights::equalLessonsCapacity);
    }

    static double notEqualsLessonsCountOnDay(vector<int>& lenghts) {
        double sum = 0;

        for (auto lenght : lenghts) {
            sum += lenght;
        }

        double avr = sum / lenghts.size();

        double value = 0;

        for (auto lenght : lenghts) {
            value += abs(lenght - avr);
        }

        return Weights::notEqualsLessonsCountOnDay * pow(value, Weights::notEqualsLessonsCountOnDayCapacity);
    }

    static double lessonsEmptySlots(vector<int>& subjects) {
        double value = 0;

        for (const auto& subject : subjects) {
            if (subject == 0) {
                value += 1;
            }
        }

        return Weights::lessonsEmptySlots * pow(value, Weights::lessonsEmptySlotsCapacity);
    }

    inline static vector<double> capacityDaysByHard{1, 1.4, 1.4, 1, 1.4, 1, 1};

    static double daysByHard(Week& week) {
        Data& data = getData();

        vector<int> hards(JOB_WEEK_LENGHT, 0);

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            for (auto lesson : week.days[day].lessons) {
                if (lesson.empty) {
                    continue;
                }

                hards[day] += int(data.hards[lesson.subject]);
            }

            hards[day] *= capacityDaysByHard[day];
        }

        double sum = 0;

        for (auto lenght : hards) {
            sum += lenght;
        }

        double avr = sum / hards.size();

        double value = 0;

        for (auto lenght : hards) {
            value += abs(lenght - avr);
        }

        return Weights::daysByHard * pow(value / JOB_WEEK_LENGHT, Weights::daysByHardCapacity);
    }

    static double teacherFreeTime(Teacher& teacher) {
        double value = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int first = -1;
            int end = -1;

            int cnt = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                if (first == -1 && teacher.work[day][lesson]) {
                    first = lesson;
                }

                if (teacher.work[day][lesson]) {
                    end = lesson;
                    cnt++;
                }
            }

            value += Weights::teacherFreeTime * pow(end - first - cnt + 1 + max(0, 3 - cnt), Weights::teacherFreeTimeCapacity);
        }

        return value / JOB_WEEK_LENGHT;
    }
};

map<string, double> point = {
    {"equal-lessons", 0},
    {"not-equals-lessons-count-on-day", 0},
    {"lessons-order", 0},
    {"days-by-hard", 0}
};

map<string, double> getClassPoint(Week& week) {
    map<string, double> answer = point;

    vector<int> lenghts(week.days.size(), 0);

    for (int i = 0; i < week.days.size(); i++) {
        Day& day = week.days[i];

        int end = 0;

        for (int j = 0; j < day.lessons.size(); j++) {
            if (day.lessons[j].empty == false) {
                end = j;
            }
        }

        lenghts[i] = end;

        vector<int> subjects;

        for (int j = 0; j < day.lessons.size(); j++) {
            if (j > end) {
                break;
            }

            subjects.push_back(day.lessons[j].subject);
        }

        answer["equal-lessons"] += Functions::equalLessons(subjects);
        answer["lessons-order"] += Functions::lessonsEmptySlots(subjects);
    }

    answer["not-equals-lessons-count-on-day"] += Functions::notEqualsLessonsCountOnDay(lenghts);
    answer["days-by-hard"] += Functions::daysByHard(week);

    return answer;
}

map<string, double> getClassPoint() {
    map<string, double> answer = point;

    for (auto& week : classes) {
        for (auto& [key, value] : getClassPoint(week)) {
            answer[key] += value;
        }
    }

    return answer;
}

double getClassTotal(Week& week) {
    double ans = 0;

    for (auto& [key, value] : getClassPoint(week)) {
        ans += value;
    }

    return ans;
}

double getClassTotal() {
    double ans = 0;

    for (auto& week : classes) {
        ans += getClassTotal(week);
    }

    return ans;
}

json save() {
    Data& data = getData();

    json answer;

    for (int idx = 0; idx < data.classes.size(); idx++) {
        answer[data.classes[idx]] = classes[idx].save();
    }

    return answer;
}

int main(int argc, char** argv){
    CLI::App app;

    int iterations = 1e6;
    app.add_option("--iterations", iterations);

    string weights = "null";
    app.add_option("--weights", weights);

    string output = "answer.json";
    app.add_option("--output", output);

    CLI11_PARSE(app, argc, argv);

    if (weights != "null") {
        ifstream file(weights);

        if (file.is_open()) {
            Weights::init(json::parse(file));

        } else {
            throw runtime_error("Cannot open weights");
        }
    }

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    Data& data = getData();

    teachers.push_back(Teacher());

    for (int idx = 0; idx < data.teachers.size(); idx++) {
        auto teacher = data.teachers[idx];

        teacherNameByID[idx + 1] = teacher;
        IDByTeacherName[teacher] = idx + 1;

        teachers.push_back(Teacher(idx + 1));
    }

    for (int idx = 0; idx < data.subjects.size(); idx++) {
        auto subject = data.subjects[idx];

        subjectNameByID[idx + 1] = subject;
        IDBySubjectName[subject] = idx + 1;
    }

    for (int idx = 0; idx < data.classes.size(); idx++) {
        string name = data.classes[idx];

        classes.push_back(Week(idx, name));
        classes.back().init();
    }

    cout << fixed << setprecision(2) << endl;

    double long total = getClassTotal();

    for (int idx = 0; idx < data.teachers.size(); idx++) {
        total += Functions::teacherFreeTime(teachers[idx]);
    }

    double temperature = 100;

    int equal = 0;

    for (int iter = 0; iter < iterations; iter++) {
        temperature *= 0.999998;

        int cls = randint(0, classes.size() - 1);

        int day1 = randint(0, JOB_WEEK_LENGHT - 1);
        int day2 = randint(0, JOB_WEEK_LENGHT - 1);

        int lesson1 = randint(0, MAX_LESSON_IN_DAY - 1);
        int lesson2 = randint(0, MAX_LESSON_IN_DAY - 1);

        int teacher1 = classes[cls].days[day1].lessons[lesson1].teacher;
        int teacher2 = classes[cls].days[day2].lessons[lesson2].teacher;

        double last = getClassTotal(classes[cls]);

        double lastTeacherFree = 0;

        if (teacher1 != 0) {
            lastTeacherFree += Functions::teacherFreeTime(teachers[teacher1]);
        }

        if (teacher2 != 0 && teacher2 != teacher1) {
            lastTeacherFree += Functions::teacherFreeTime(teachers[teacher2]);
        }

        if (classes[cls].can(day1, lesson1, day2, lesson2)) {
            swap(classes[cls].days[day1].lessons[lesson1], classes[cls].days[day2].lessons[lesson2]);

            if (teacher1 != 0) {
                teachers[teacher1].work[day1][lesson1] = false;
                teachers[teacher1].work[day2][lesson2] = true;
            }

            if (teacher2 != 0) {
                teachers[teacher2].work[day2][lesson2] = false;
                teachers[teacher2].work[day1][lesson1] = true;
            }

            double now = getClassTotal(classes[cls]);

            double nowTeacherFree = 0;

            if (teacher1 != 0) {
                nowTeacherFree += Functions::teacherFreeTime(teachers[teacher1]);
            }

            if (teacher2 != 0 && teacher2 != teacher1) {
                nowTeacherFree += Functions::teacherFreeTime(teachers[teacher2]);
            }

            double delta = (now - last) + (nowTeacherFree - lastTeacherFree);

            if (delta < 0 || double(randint(1, 1e7)) / 1e7 < exp(-delta / temperature)) {
                total = total - last + now - lastTeacherFree + nowTeacherFree;

                if (delta > 0) {
                    equal += 1;

                } else {
                    equal = 0;
                }

            } else {
                swap(classes[cls].days[day1].lessons[lesson1], classes[cls].days[day2].lessons[lesson2]);

                if (teacher1 != 0) {
                    teachers[teacher1].work[day1][lesson1] = true;
                    teachers[teacher1].work[day2][lesson2] = false;
                }

                if (teacher2 != 0) {
                    teachers[teacher2].work[day2][lesson2] = true;
                    teachers[teacher2].work[day1][lesson1] = false;
                }

                equal += 1;
            }

            if (equal == 1000 || (iter + 1) % 10000 == 0) {
                cout << "\n";

                if (equal == 1000) {
                    cout << "[EQUAL]";

                } else {
                    cout << "[PRINT]";
                }

                cout << " " << iter + 1 << " " << temperature << " " << total << " " << equal << "\n";

                double var = total;

                for (auto& [key, value] : getClassPoint()) {
                    cout << key << ": " << value << "; ";

                    var -= value;
                }

                cout << "teacher-free-time: " << var << "; ";

                cout << "\n";
            }

            if (equal == 1000) {
                temperature = min(100.0, 2 * temperature);

                equal = 0;
            }
        }
    }

    std::ofstream file(output);

    file << std::setw(4) << save() << std::endl;
    file.close();

    return 0;
}
