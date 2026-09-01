#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#include "libs/CLI11.hpp"
#include "libs/json.hpp"

using namespace std;

using json = nlohmann::json;

// CONSTANTS

const int JOB_WEEK_LENGHT = 5;
const int MAX_LESSON_IN_DAY = 10;

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

map<int, string> teacherNameByID;
map<string, int> IDByTeacherName;

map<int, string> subjectNameByID;
map<string, int> IDBySubjectName;

map<int, string> classNameByID;
map<string, int> IDByClassName;

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

        for (int idx = 0; idx < subjects.size(); idx++) {
            auto subject = subjects[idx];

            subjectNameByID[idx + 1] = subject;
            IDBySubjectName[subject] = idx + 1;
        }

        for (int idx = 0; idx < teachers.size(); idx++) {
            auto teacher = teachers[idx];

            teacherNameByID[idx + 1] = teacher;
            IDByTeacherName[teacher] = idx + 1;
        }

        for (int idx = 0; idx < classes.size(); idx++) {
            auto subject = classes[idx];

            classNameByID[teachers.size() + idx + 1] = subject;
            IDByClassName[subject] = teachers.size() + idx + 1;
        }
    }
};

Data& getData() {
    static Data instance;

    return instance;
}

struct edge {
    int id = 0, value = 0;

    edge() {

    }

    edge(int id_, int value_) {
        id = id_;
        value = value_;
    }
};

vector<vector<edge>> graph;

struct Weights {
    inline static double equalLessons = 5;
    inline static double notEqualsLessonsCountOnDay = 25;
    inline static double lessonsEmptySlots = 200;
    inline static double daysByHard = 2;
    inline static double teacherFreeTime = 5;

    static void init(const json& data) {
        equalLessons = data.value("equalLessons", equalLessons);
        notEqualsLessonsCountOnDay = data.value("notEqualsLessonsCountOnDay", notEqualsLessonsCountOnDay);
        lessonsEmptySlots = data.value("lessonsEmptySlots", lessonsEmptySlots);
        daysByHard = data.value("daysByHard", daysByHard);
        teacherFreeTime = data.value("teacherFreeTime", teacherFreeTime);
    }
};

class Functions {
public:
    static double equalLessons(int cls, int day) {
        double value = 0;

        for (int i = day * MAX_LESSON_IN_DAY; i < (day + 1) * MAX_LESSON_IN_DAY; i++) {
            for (int j = i + 1; j < (day + 1) * MAX_LESSON_IN_DAY; j++) {
                if (graph[cls][i].value == 0 || graph[cls][j].value == 0) {
                    continue;
                }

                if (graph[cls][i].value == graph[cls][j].value) {
                    value += 1;
                }
            }
        }

        return Weights::equalLessons * value;
    }

    static double notEqualsLessonsCountOnDay(int cls) {
        int lenghts[JOB_WEEK_LENGHT] = {0};

        double sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int end = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                if (graph[cls][day * MAX_LESSON_IN_DAY + lesson].id != 0) {
                    end = lesson;
                }
            }

            lenghts[day] = end;
            sum += end;
        }

        double avr = sum / JOB_WEEK_LENGHT;

        double value = 0;

        for (auto lenght : lenghts) {
            value += pow(lenght - avr, 2.0);
        }

        return Weights::notEqualsLessonsCountOnDay * value;
    }

    static double lessonsEmptySlots(int cls, int day) {
        double value = 0;

        int temp = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (graph[cls][day * MAX_LESSON_IN_DAY + lesson].id != 0) {
                value += temp;
                temp = 0;

            } else {
                temp += 1;
            }
        }

        return Weights::lessonsEmptySlots * value;
    }

    inline static vector<double> capacityDaysByHard{1, 1.4, 1.4, 1, 1.4, 1, 1};

    static double daysByHard(int cls) {
        Data& data = getData();

        double hards[JOB_WEEK_LENGHT] = {0};

        double sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                hards[day] += data.hards[graph[cls][day * MAX_LESSON_IN_DAY + lesson].value];
            }

            hards[day] /= capacityDaysByHard[day];
            sum += hards[day];
        }

        double avr = sum / JOB_WEEK_LENGHT;

        double value = 0;

        for (auto hard : hards) {
            value += abs(avr - hard);
        }

        return Weights::daysByHard * value;
    }

    static double teacherFreeTime(int teacher) {
        double value = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int start = -1;
            int end = -1;

            int cnt = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                if (graph[teacher][day * MAX_LESSON_IN_DAY + lesson].id != 0) {
                    if (start == -1) {
                        start = lesson;
                    }

                    end = lesson;
                    cnt += 1;
                }
            }

            if (cnt == 0) {
                continue;
            }

            value += end - start - cnt + 1 + max(0, 4 - cnt);
        }

        return Weights::teacherFreeTime * value;
    }
};

const int FUNCTIONS_ARGUMENTS_COUNT = 5;

vector<double> getClassPoint(int cls) {
    vector<double> answer(FUNCTIONS_ARGUMENTS_COUNT, 0);

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        answer[0] += Functions::equalLessons(cls, day);
        answer[2] += Functions::lessonsEmptySlots(cls, day);
    }

    answer[1] += Functions::notEqualsLessonsCountOnDay(cls);
    answer[3] += Functions::daysByHard(cls);

    return answer;
}

vector<double> getClassPoint() {
    Data& data = getData();

    vector<double> answer(FUNCTIONS_ARGUMENTS_COUNT, 0);

    for (int cls = data.teachers.size() + 1; cls < data.teachers.size() + data.classes.size() + 1; cls++) {
        vector<double> temp = getClassPoint(cls);

        for (int i = 0; i < FUNCTIONS_ARGUMENTS_COUNT; i++) {
            answer[i] += temp[i];
        }
    }

    return answer;
}

double getClassTotal(int cls) {
    double answer = 0;

    vector<double> temp = getClassPoint(cls);

    for (int i = 0; i < FUNCTIONS_ARGUMENTS_COUNT; i++) {
        answer += temp[i];
    }

    return answer;
}

double getClassTotal() {
    Data& data = getData();

    double answer = 0;

    for (int cls = data.teachers.size() + 1; cls < data.teachers.size() + data.classes.size() + 1; cls++) {
        answer += getClassTotal(cls);
    }

    return answer;
}

json save() {
    Data& data = getData();

    json answer;

    for (int cls = data.teachers.size() + 1; cls < data.teachers.size() + data.classes.size() + 1; cls++) {
        string& name = classNameByID[cls];

        answer[name] = json::array();

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            answer[name].push_back(json::array());

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                int slot = day * MAX_LESSON_IN_DAY + lesson;

                answer[name][day].push_back(json{
                    {"subject", graph[cls][slot].id == 0 ? "#" : subjectNameByID[graph[cls][slot].value]},
                    {"teacher", graph[cls][slot].id == 0 ? "#" : teacherNameByID[graph[cls][slot].id]}
                });
            }
        }
    }

    return answer;
}

int main(int argc, char** argv) {
    CLI::App app;

    int iterations = 5e7;
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
            throw runtime_error("Can not open weights");
        }
    }

    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    Data& data = getData();

    int size = data.teachers.size() + data.classes.size() + 3;

    graph.assign(size, vector(JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY, edge()));

    for (auto& key : data.classes) {
        json& value = data.lessons[key];

        for (auto subject : value) {
            for (int i = 0; i < subject["hours"]; i++) {
                int color = randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);

                int teacher = IDByTeacherName[subject["teacher"]];
                int cls = IDByClassName[key];

                while (graph[teacher][color].id != 0 || graph[cls][color].id != 0) {
                    color = randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);
                }

                cout << teacher << " " << cls << " " << color << "\n";

                graph[teacher][color] = edge(cls, IDBySubjectName[subject["subject"]]);
                graph[cls][color] = edge(teacher, IDBySubjectName[subject["subject"]]);
            }
        }
    }

    double total = getClassTotal();

    for (int teacher = 1; teacher <= data.teachers.size(); teacher++) {
        total += Functions::teacherFreeTime(teacher);
    }

    double temperature = 100;

    int equal = 0;
    int count = 0;

    for (int iter = 0; iter < iterations; iter++) {
        temperature *= 0.9999999;

        if (equal == 10000 || (iter + 1) % 100000 == 0) {
            cout << "\n" << (equal == 10000 ? "[EQUAL]" : "[PRINT]") << " ";
            cout << iter + 1 << " " << temperature << " " << total << " " << equal << "\n";

            for (auto element : getClassPoint()) {
                cout << element << " ";
            }

            cout << "\n";
        }

        if (equal == 10000) {
            temperature = 20;

            equal = 0;
        }

        int teacher1 = randint(1, data.teachers.size());
        int teacher2 = randint(1, data.teachers.size());

        if (teacher1 == teacher2) {
            continue;
        }

        int color1 = randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);
        int color2 = randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);

        if (color1 == color2) {
            continue;
        }

        int cls1 = graph[teacher1][color1].id;
        int cls2 = graph[teacher2][color2].id;

        if (cls1 == cls2 || ((cls1 == 0 || cls2 == 0) && randint(1, 3) != 1)) {
            continue;
        }

        if (graph[teacher1][color2].id != 0 || graph[teacher2][color1].id != 0) {
            continue;
        }

        if (graph[cls1][color2].id != 0 || graph[cls2][color1].id != 0) {
            continue;
        }

        int subject1 = graph[cls1][color1].value;
        int subject2 = graph[cls2][color2].value;

        double before = getClassTotal(cls1) + getClassTotal(cls2);

        if (teacher1 != 0) {
            before += Functions::teacherFreeTime(teacher1);
        }

        if (teacher2 != 0) {
            before += Functions::teacherFreeTime(teacher2);
        }

        auto swapper = [&]() {
            swap(graph[teacher1][color1], graph[teacher1][color2]);
            swap(graph[teacher2][color2], graph[teacher2][color1]);

            swap(graph[cls1][color1], graph[cls1][color2]);
            swap(graph[cls2][color2], graph[cls2][color1]);
        };

        count++;

        swapper();

        double after = getClassTotal(cls1) + getClassTotal(cls2);

        if (teacher1 != 0) {
            after += Functions::teacherFreeTime(teacher1);
        }

        if (teacher2 != 0) {
            after += Functions::teacherFreeTime(teacher2);
        }

        double delta = after - before;

        if (delta < 0 || double(randint(1, 1e7)) / 1e7 < exp(-delta / temperature)) {
            total = total - before + after;
            equal = 0;

        } else {
            swapper();
            equal += 1;
        }
    }

    std::ofstream file(output);

    file << std::setw(4) << save() << std::endl;
    file.close();

    cout << count << endl;

    return 0;
}
