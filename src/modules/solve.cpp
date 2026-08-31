#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#include "libs/CLI11.hpp"
#include "libs/json.hpp"

using namespace std;

using json = nlohmann::json;

int JOB_WEEK_LENGHT   = 5;
int MAX_LESSON_IN_DAY = 10;
int NUMBER_OF_SHIFTS  = 1;

int SLOTS = 0;

vector<string> CLASSES_LETTERS = {"-", "А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Э", "Ю", "Я"};

string input = "settings.json";
string output = "answer.json";


int randint(int min, int max) {
    static __gnu_cxx::sfmt19937 rng(
        std::random_device{}() ^
        static_cast<unsigned>(std::chrono::high_resolution_clock::now().time_since_epoch().count())
    );

    std::uniform_int_distribution<int> dist(min, max);

    return dist(rng);
}


map<int, string> teacherNameByID;
map<string, int> IDByTeacherName;

map<int, string> subjectNameByID;
map<string, int> IDBySubjectName;

map<int, string> classNameByID;
map<string, int> IDByClassName;


class Data {
public:
    json lessons;

    vector<vector<int>> free;

    map<string, int> hards;
    vector<string> teachers, classes;
    
    vector<int> shifts;
    vector<int> shiftByClass;

    vector<double> hardsById;
    vector<double> capacityDaysByHard;
    
    vector<int> classShiftOffset;
    vector<vector<int>> classesByShift;

    Data() {
        ifstream file(input);

        json settings;

        if (file.is_open()) {
            settings = json::parse(file);

        } else {
            throw runtime_error("Can not open input file: " + input);
        }

        JOB_WEEK_LENGHT   = settings["working_days_per_week"];
        MAX_LESSON_IN_DAY = settings["max_lesson_count_per_day"];
        NUMBER_OF_SHIFTS  = settings["number_of_shifts"];

        SLOTS = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * NUMBER_OF_SHIFTS;

        for (auto element : settings["subjects"]) {
            hards[element[0]] = element[1];
        }

        for (auto element : settings["classes"]["shift"]) {
            shifts.push_back(element);
        }

        for (int i = 1; i <= settings["classes"]["count"].size(); i++) {
            for (int j = 1; j <= settings["classes"]["count"][i - 1]; j++) {
                classes.push_back(to_string(i) + " " + CLASSES_LETTERS[j]);
                shiftByClass.push_back(i - 1);
            }
        }

        for (auto& [teacher, value] : settings["teachers"].items()) {
            teachers.push_back(teacher);

            vector<int> exclude;

            for (int i = 0; i < NUMBER_OF_SHIFTS; i++) {
                for (vector<int> element : value["free"][i]) {
                    exclude.push_back(JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * i + MAX_LESSON_IN_DAY * element[0] + element[1]);
                }
            }

            free.push_back(vector<int>());

            for (int i = 0; i < SLOTS; i++) {
                bool find = false;

                for (int j = 0; j < exclude.size(); j++) {
                    if (i == exclude[j]) {
                        find = true;
                        break;
                    }
                }

                if (find) {
                    continue;
                }

                free.back().push_back(i);
            }
        }

        for (string& cls : classes) {
            lessons[cls] = json::array();

            for (auto& [subject, count] : settings["classes"]["lessons"][cls].items()) {
                vector<string> temp;

                for (string& teacher : teachers) {
                    for (auto& element : settings["teachers"][teacher]["subjects"]) {
                        if (element["subject"] == subject) {
                            bool find = false;

                            for (auto use : element["classes"]) {
                                if (use == cls) {
                                    find = true;
                                }
                            }

                            if (find) {
                                temp.push_back(teacher);
                            }
                        }
                    }
                }

                if (temp.size()) {
                    lessons[cls].push_back({
                        {"subject", subject},
                        {"teachers", temp},
                        {"hours", count}
                    });

                } else {
                    cout << "[WARNING]: " << cls << " not found teacher for " << subject << "\n";
                }
            }
        }

        for (int idx = 0; idx < settings["subjects"].size(); idx++) {
            auto subject = settings["subjects"][idx][0];

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

        hardsById.assign(settings["subjects"].size() + 1, 0);

        for (int idx = 0; idx < settings["subjects"].size(); idx++) {
            hardsById[idx + 1] = hards[settings["subjects"][idx][0]];
        }

        capacityDaysByHard.assign(JOB_WEEK_LENGHT, 1.0);

        if (settings.contains("capacityDaysByHard")) {
            auto arr = settings["capacityDaysByHard"];

            for (int i = 0; i < min((int)arr.size(), JOB_WEEK_LENGHT); i++) {
                capacityDaysByHard[i] = arr[i];
            }
        }

        classShiftOffset.assign(teachers.size() + classes.size() + 1, 0);

        for (int idx = 0; idx < (int)classes.size(); idx++) {
            classShiftOffset[teachers.size() + idx + 1] = shifts[shiftByClass[idx]] * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;
        }

        classesByShift.assign(NUMBER_OF_SHIFTS, vector<int>());

        for (int idx = 0; idx < (int)classes.size(); idx++) {
            int cls = teachers.size() + idx + 1;
            classesByShift[shifts[shiftByClass[idx]]].push_back(cls);
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

vector<vector<vector<edge>>> graph;
vector<vector<bool>> teacherAllowed;

inline bool occupied(int row, int slot) {
    return !graph[row][slot].empty();
}

inline int slotValue(int row, int slot) {
    return graph[row][slot].empty() ? 0 : graph[row][slot][0].value;
}

struct Lesson {
    int cls, base, subjectID;
    string className, subjectName;
    vector<int> ids;

    Lesson(int cls_, int base_, vector<int> ids_, int subjectID_, string className_, string subjectName_) {
        cls = cls_;
        base = base_;
        ids = ids_;
        subjectID = subjectID_;
        className = className_;
        subjectName = subjectName_;
    }
};

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
        Data& data = getData();

        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        double value = 0;

        for (int i = base; i < base + MAX_LESSON_IN_DAY; i++) {
            for (int j = i + 1; j < base + MAX_LESSON_IN_DAY; j++) {
                int vi = slotValue(cls, i);
                int vj = slotValue(cls, j);

                if (vi == 0 || vj == 0) {
                    continue;
                }

                if (vi == vj) {
                    value += 1;
                }
            }
        }

        return Weights::equalLessons * value;
    }

    static double notEqualsLessonsCountOnDay(int cls) {
        Data& data = getData();
        int offset = data.classShiftOffset[cls];

        vector<int> lenghts(JOB_WEEK_LENGHT, 0);
        double sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int base = offset + day * MAX_LESSON_IN_DAY;
            int end = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                if (occupied(cls, base + lesson)) {
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
        Data& data = getData();
        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        double value = 0;
        int temp = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (occupied(cls, base + lesson)) {
                value += temp;
                temp = 0;

            } else {
                temp += 1;
            }
        }

        return Weights::lessonsEmptySlots * value;
    }

    static double daysByHard(int cls) {
        Data& data = getData();
        int offset = data.classShiftOffset[cls];

        vector<double> hards(JOB_WEEK_LENGHT, 0);

        double sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int base = offset + day * MAX_LESSON_IN_DAY;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                hards[day] += data.hardsById[slotValue(cls, base + lesson)];
            }

            hards[day] /= data.capacityDaysByHard[day];
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

        for (int shift = 0; shift < NUMBER_OF_SHIFTS; shift++) {
            for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
                int base = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;

                int start = -1, end = -1, cnt = 0;

                for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                    if (occupied(teacher, base + lesson)) {
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
                int slot = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY + lesson;

                if (!occupied(cls, slot)) {
                    answer[name][day].push_back(json{{"subject", "#"}, {"teachers", json::array()}});

                    continue;
                }

                answer[name][day].push_back(json{{"subject", subjectNameByID[graph[cls][slot][0].value]}, {"teachers", json::array()}});

                for (edge& e : graph[cls][slot]) {
                    answer[name][day].back()["teachers"].push_back(teacherNameByID[e.id]);
                }
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

    app.add_option("--input", input);
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

    graph.assign(size, vector<vector<edge>>(SLOTS));

    teacherAllowed.assign(size, vector<bool>(SLOTS, false));

    for (int t = 0; t < (int)data.teachers.size(); t++) {
        for (int slot : data.free[t]) {
            teacherAllowed[t + 1][slot] = true;
        }
    }

    vector<Lesson> pending;

    for (auto& key : data.classes) {
        json& value = data.lessons[key];

        int cls = IDByClassName[key];
        int base = data.classShiftOffset[cls];

        for (auto subject : value) {
            vector<int> ids;

            for (auto& tName : subject["teachers"]) {
                ids.push_back(IDByTeacherName[tName]);
            }

            int subjectID = IDBySubjectName[subject["subject"]];

            for (int i = 0; i < subject["hours"]; i++) {
                pending.push_back(Lesson{cls, base, ids, subjectID, key, (string)subject["subject"]});
            }
        }
    }

    int unplaced = 0;

    while (!pending.empty()) {
        int bestIdx = -1;
        vector<int> bestCandidates;

        for (int idx = 0; idx < (int)pending.size(); idx++) {
            Lesson& item = pending[idx];

            vector<int> candidates;

            for (int slot = item.base; slot < item.base + JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY; slot++) {
                if (occupied(item.cls, slot)) {
                    continue;
                }

                bool ok = true;

                for (int id : item.ids) {
                    if (!teacherAllowed[id][slot] || occupied(id, slot)) {
                        ok = false;

                        break;
                    }
                }

                if (ok) {
                    candidates.push_back(slot);
                }
            }

            if (bestIdx == -1 || candidates.size() < bestCandidates.size()) {
                bestIdx = idx;
                bestCandidates = candidates;
            }

            if (bestCandidates.empty()) {
                break;
            }
        }

        Lesson item = pending[bestIdx];
        pending.erase(pending.begin() + bestIdx);

        if (bestCandidates.empty()) {
            cout << "[WARNING]: no common free slot for " << item.className << " / " << item.subjectName << "\n";

            unplaced++;

            continue;
        }

        int color = bestCandidates[randint(0, bestCandidates.size() - 1)];

        vector<edge> group;

        for (int id : item.ids) {
            graph[id][color] = {edge(item.cls, item.subjectID)};

            group.push_back(edge(id, item.subjectID));
        }

        graph[item.cls][color] = group;
    }

    if (unplaced > 0) {
        cout << "[WARNING]: " << unplaced << " lesson(s) could not be placed during initial construction\n";
    }

    double total = getClassTotal();

    for (int teacher = 1; teacher <= (int)data.teachers.size(); teacher++) {
        total += Functions::teacherFreeTime(teacher);
    }

    double temperature = 100;

    int equal = 0;
    int count = 0;

    for (int iter = 0; iter < iterations; iter++) {
        temperature *= 0.9999999;

        if (equal == 10000 || (iter + 1) % 1000000 == 0) {
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

        if (randint(0, 1) == 0) {
            int shift = randint(0, NUMBER_OF_SHIFTS - 1);

            if (data.classesByShift[shift].empty()) {
                continue;
            }

            auto& shiftClasses = data.classesByShift[shift];
            int cls = shiftClasses[randint(0, shiftClasses.size() - 1)];
            int off = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

            int slotA = off + randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);
            int slotB = off + randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);

            if (slotA == slotB) {
                continue;
            }

            vector<edge>& groupA = graph[cls][slotA];
            vector<edge>& groupB = graph[cls][slotB];

            if (groupA.empty() && groupB.empty()) {
                continue;
            }

            set<int> teachersA, teachersB;

            for (auto& e : groupA) teachersA.insert(e.id);
            for (auto& e : groupB) teachersB.insert(e.id);

            bool ok = true;

            for (int t : teachersA) {
                if (!teacherAllowed[t][slotB] || (occupied(t, slotB) && !teachersB.count(t))) {
                    ok = false;
                    break;
                }
            }

            if (ok) {
                for (int t : teachersB) {
                    if (!teacherAllowed[t][slotA] || (occupied(t, slotA) && !teachersA.count(t))) {
                        ok = false;
                        break;
                    }
                }
            }

            if (!ok) {
                continue;
            }

            vector<int> involvedTeachers(teachersA.begin(), teachersA.end());

            for (int t : teachersB) {
                if (!teachersA.count(t)) {
                    involvedTeachers.push_back(t);
                }
            }

            double before = getClassTotal(cls);

            for (int t : involvedTeachers) {
                before += Functions::teacherFreeTime(t);
            }

            auto intraSwapper = [&]() {
                for (int t : involvedTeachers) {
                    swap(graph[t][slotA], graph[t][slotB]);
                }

                swap(graph[cls][slotA], graph[cls][slotB]);
            };

            count++;
            intraSwapper();

            double after = getClassTotal(cls);

            for (int t : involvedTeachers) {
                after += Functions::teacherFreeTime(t);
            }

            double delta = after - before;

            if (delta < 0 || double(randint(1, 1e7)) / 1e7 < exp(-delta / temperature)) {
                total = total - before + after;
                equal = 0;

            } else {
                intraSwapper();
                equal += 1;
            }

            continue;
        }

        int shift = randint(0, NUMBER_OF_SHIFTS - 1);

        if (data.classesByShift[shift].size() < 2) {
            continue;
        }

        auto& shifts = data.classesByShift[shift];

        int cls1 = shifts[randint(0, shifts.size() - 1)];
        int cls2 = shifts[randint(0, shifts.size() - 1)];

        if (cls1 == cls2) {
            continue;
        }

        int off = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

        int color1 = off + randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);
        int color2 = off + randint(0, JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY - 1);

        if (color1 == color2) {
            continue;
        }

        vector<edge>& group1 = graph[cls1][color1];
        vector<edge>& group2 = graph[cls2][color2];

        if (group1.empty() && group2.empty()) {
            continue;
        }

        if ((group1.empty() || group2.empty()) && randint(1, 3) != 1) {
            continue;
        }

        if (occupied(cls1, color2) || occupied(cls2, color1)) {
            continue;
        }

        set<int> teachers1, teachers2;

        for (auto& e : group1) {
            teachers1.insert(e.id);
        }

        for (auto& e : group2) {
            teachers2.insert(e.id);
        }

        bool ok = true;

        for (int t : teachers1) {
            if (!teacherAllowed[t][color2]) {
                ok = false;

                break;
            }

            if (occupied(t, color2) && !teachers2.count(t)) {
                ok = false;

                break;
            }
        }

        if (ok == false) {
            continue;
        }

        for (int t : teachers2) {
            if (!teacherAllowed[t][color1]) {
                ok = false;

                break;
            }

            if (occupied(t, color1) && !teachers1.count(t)) {
                ok = false;

                break;
            }
        }

        if (ok == false) {
            continue;
        }

        vector<int> involvedTeachers(teachers1.begin(), teachers1.end());

        for (int t : teachers2) {
            if (!teachers1.count(t)) {
                involvedTeachers.push_back(t);
            }
        }

        double before = getClassTotal(cls1) + getClassTotal(cls2);

        for (int t : involvedTeachers) {
            before += Functions::teacherFreeTime(t);
        }

        auto swapper = [&]() {
            for (int t : involvedTeachers) {
                swap(graph[t][color1], graph[t][color2]);
            }

            swap(graph[cls1][color1], graph[cls1][color2]);
            swap(graph[cls2][color1], graph[cls2][color2]);
        };

        count++;
        swapper();

        double after = getClassTotal(cls1) + getClassTotal(cls2);

        for (int t : involvedTeachers) {
            after += Functions::teacherFreeTime(t);
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

    cout << count << " " << total << endl;

    return 0;
}
