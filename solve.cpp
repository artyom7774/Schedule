#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#include "json.hpp"

using namespace std;

using json = nlohmann::json;

static __gnu_cxx::sfmt19937 rng(std::random_device{}());

int randint(int min, int max) {
    std::uniform_int_distribution<int> dist(min, max);

    return dist(rng);
}

class Data {
public:
    json teachers, classes, lessons;

    Data() {
        teachers = json::parse(std::ifstream("data/teachers.json"));
        classes = json::parse(std::ifstream("data/classes.json"));

        lessons = json::parse(std::ifstream("data/lessons.json"));
    }
};

Data& getData() {
    static Data instance;

    return instance;
}

struct Teacher;

struct Week;
struct Day;
struct Lesson;

vector<Week> classes;
set<Teacher> teachers;

struct Teacher {
    int code = 0, day = 0, lesson = 0;

    Teacher() {

    }

    Teacher(string name, int day_, int lesson_) {
        code = hash<string>{}(name);

        day = day_;
        lesson = lesson_;
    }

    Teacher(int code_, int day_, int lesson_) {
        code = code_;

        day = day_;
        lesson = lesson_;
    }

    bool operator<(const Teacher& another) const {
        if (code != another.code) {
            return code < another.code;
        }

        if (day != another.day) {
            return day < another.day;
        }

        return lesson < another.lesson;
    }
};

struct Lesson {
    string subject;
    int teacher = 0;

    bool empty = true;

    Lesson() {
        subject = "#";
        teacher = 0;
    }

    Lesson(string subject_, string teacher_) {
        subject = subject_;
        teacher = hash<string>{}(teacher_);

        empty = false;
    }

    Lesson(string subject_, int teacher_) {
        subject = subject_;
        teacher = teacher_;

        empty = false;
    }
};

struct Day {
    vector<Lesson> lessons;

    Day() {
        lessons.assign(10, Lesson());
    }

    Day(vector<Lesson> lessons_) {
        lessons = lessons_;
    }
};

struct Week {
    vector<Day> days;

    string name = "";
    int idx = 0;

    Week() {
        days.assign(5, Day());
    }

    Week(int idx_, string name_) {
        days.assign(5, Day());

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
                int day = randint(0, 4);
                int lsn = randint(0, 9);

                Teacher teacher = Teacher(lesson.teacher, day, lsn);

                if (teachers.count(teacher) == 1 || (days[day].lessons[lsn].empty == false)) {
                    continue;
                }

                cnt--;

                teachers.insert(teacher);

                days[day].lessons[lsn] = lesson;

                cout << iter << " " << lesson.subject << " - " << lesson.teacher << "\n";

                iter += 1;
            }
        }
    }

    bool can(int day1, int lesson1, int day2, int lesson2) {
        int teacher1 = days[day1].lessons[lesson1].teacher;
        int teacher2 = days[day2].lessons[lesson2].teacher;

        bool f1 = teachers.count(Teacher(teacher2, day1, lesson1)) == 0;
        bool f2 = teachers.count(Teacher(teacher1, day2, lesson2)) == 0;

        return f1 && f2;
    }
};

class Functions {
public:
    static double equalLessons(vector<string>& subjects) {
        set<string> unique;

        for (const auto& subject : subjects) {
            unique.insert(subject);
        }

        double value = subjects.size() - unique.size();

        return 10 * pow(value, 2.0);
    }

    static double notEqualsLessonsCountOnDay(vector<int>& lenghts) {
        double sum = 0;

        for (auto lenght : lenghts) {
            sum += lenght;
        }

        double avr = sum / lenghts.size();

        double value = 0;

        for (auto lenght : lenghts) {
            value += pow(lenght - avr, 2.0);
        }

        return 10 * pow(value, 1.7);
    }

    static double lessonsOrder(vector<string>& subjects) {
        double value = 0;

        for (const auto& subject : subjects) {
            if (subject == "#") {
                value += 1;
            }
        }

        return 500 * pow(value, 2.0);
    }
};

map<string, double> point = {
    {"equal-lessons", 0},
    {"not-equals-lessons-count-on-day", 0},
    {"lessons-order", 0}
};

map<string, double> getClassPoint(Week week) {
    map<string, double> answer = point;

    vector<int> lenghts(5, 0);

    for (int i = 0; i < week.days.size(); i++) {
        Day& day = week.days[i];

        int end = 0;

        for (int j = 0; j < day.lessons.size(); j++) {
            if (day.lessons[j].empty == false) {
                end = j;
            }
        }

        lenghts[i] = end;

        vector<string> subjects;

        for (int j = 0; j < day.lessons.size(); j++) {
            if (j > end) {
                break;
            }

            subjects.push_back(day.lessons[j].subject);
        }

        answer["equal-lessons"] += Functions::equalLessons(subjects);
        answer["lessons-order"] += Functions::lessonsOrder(subjects);
    }

    answer["not-equals-lessons-count-on-day"] += Functions::notEqualsLessonsCountOnDay(lenghts);

    return answer;
}

map<string, double> getClassPoint() {
    map<string, double> answer = point;

    for (auto week : classes) {
        for (auto& [key, value] : getClassPoint(week)) {
            answer[key] += value;
        }
    }

    return answer;
}

double getClassTotal(Week week) {
    double ans = 0;

    for (auto& [key, value] : getClassPoint(week)) {
        ans += value;
    }

    return ans;
}

double getClassTotal() {
    double ans = 0;

    for (auto week : classes) {
        ans += getClassTotal(week);
    }

    return ans;
}

int main(){
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    Data& data = getData();

    for (int idx = 0; idx < data.classes.size(); idx++) {
        string name = data.classes[idx];

        classes.push_back(Week(idx, name));
        classes.back().init();
    }

    cout << fixed << setprecision(2) << endl;

    double total = getClassTotal();
    double temperature = 100;

    int equal = 0;

    for (int iter = 0; iter < 1e5; iter++) {
        temperature *= 0.999998;

        int cls = randint(0, classes.size() - 1);

        int day1 = randint(0, 4);
        int day2 = randint(0, 4);

        int lesson1 = randint(0, 9);
        int lesson2 = randint(0, 9);

        int teacher1 = classes[cls].days[day1].lessons[lesson1].teacher;
        int teacher2 = classes[cls].days[day2].lessons[lesson2].teacher;

        double last = getClassTotal(classes[cls]);

        if (classes[cls].can(day1, lesson1, day2, lesson2)) {
            swap(classes[cls].days[day1].lessons[lesson1], classes[cls].days[day2].lessons[lesson2]);

            double now = getClassTotal(classes[cls]);

            double delta = now - last;

            if (delta < 0 || double(randint(1, 1e7)) / 1e7 < exp(-delta / temperature)) {
                total = total - last + now;

                if (teacher1 != 0) {
                    teachers.insert(Teacher(teacher1, day2, lesson2));
                    teachers.erase(Teacher(teacher1, day1, lesson1));
                }

                if (teacher2 != 0) {
                    teachers.insert(Teacher(teacher2, day1, lesson1));
                    teachers.erase(Teacher(teacher2, day2, lesson2));
                }

                if (delta > 0) {
                    equal += 1;

                } else {
                    equal = 0;
                }

            } else {
                swap(classes[cls].days[day1].lessons[lesson1], classes[cls].days[day2].lessons[lesson2]);

                equal += 1;
            }

            if (equal == 1000 || (iter + 1) % 1000 == 0) {
                cout << "\n";

                if (equal == 1000) {
                    cout << "[EQUAL]";

                } else {
                    cout << "[PRINT]";
                }

                cout << " " << iter + 1 << " " << temperature << " " << total << " " << equal << "\n";
            }

            if (equal == 1000) {
                temperature = max(20.0, temperature);

                equal = 0;
            }
        }
    }

    return 0;
}
