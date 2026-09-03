#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#include "libs/CLI11.hpp"
#include "libs/json.hpp"

using namespace std;

using json = nlohmann::json;

int JOB_WEEK_LENGHT    = 5;
int MAX_LESSON_IN_DAY  = 8;
int NUMBER_OF_SHIFTS   = 1;
int SHIFT_CROSSING     = 0;

int SLOTS = 0;

const int MAX_GROUP_SUBJECTS = 2;

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

    map<int, set<int>> groupedWith;
    vector<vector<char>> groupedMatrix;

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
        SHIFT_CROSSING    = settings["shift_crossing"];

        SLOTS = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * NUMBER_OF_SHIFTS;

        for (auto element : settings["subjects"]) {
            hards[element[0]] = element[1];
        }

        for (auto element : settings["classes"]["shift"]) {
            shifts.push_back(element);
        }

        for (int s : shifts) {
            if (s < 0 || s >= NUMBER_OF_SHIFTS) {
                throw runtime_error(
                    "classes.shift содержит значение " + to_string(s) +
                    ", но number_of_shifts = " + to_string(NUMBER_OF_SHIFTS) +
                    " (допустимые индексы смены: 0.." + to_string(NUMBER_OF_SHIFTS - 1) + ")"
                );
            }
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
                if (count == 0) {
                    continue;
                }

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

        if (settings.contains("groups")) {
            set<string> groupKeys;

            for (auto& [key, val] : settings["groups"].items()) {
                if ((int)val != 0) {
                    groupKeys.insert(key);
                }
            }

            int subjectsCount = settings["subjects"].size();

            for (int i = 0; i < subjectsCount; i++) {
                for (int j = 0; j < subjectsCount; j++) {
                    if (i == j) continue;

                    string s1 = settings["subjects"][i][0];
                    string s2 = settings["subjects"][j][0];

                    if (groupKeys.count(s1 + "-" + s2)) {
                        groupedWith[i + 1].insert(j + 1);
                    }
                }
            }

            groupedMatrix.assign(subjectsCount + 1, vector<char>(subjectsCount + 1, 0));

            for (auto& [a, set_] : groupedWith) {
                for (int b : set_) {
                    groupedMatrix[a][b] = 1;
                }
            }

        } else {
            groupedMatrix.assign(settings["subjects"].size() + 1, vector<char>(settings["subjects"].size() + 1, 0));
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

struct SubjectSet {
    int values[MAX_GROUP_SUBJECTS];
    int size = 0;

    inline bool contains(int v) const {
        for (int i = 0; i < size; i++) {
            if (values[i] == v) {
                return true;
            }
        }

        return false;
    }

    inline void insert(int v) {
        if (size < MAX_GROUP_SUBJECTS && !contains(v)) {
            values[size++] = v;
        }
    }
};

inline SubjectSet slotSubjects(int row, int slot) {
    SubjectSet result;

    for (edge& e : graph[row][slot]) {
        result.insert(e.value);
    }

    return result;
}

bool canPlaceLesson(int cls, int slot, int subjectID) {
    if (!occupied(cls, slot)) {
        return true;
    }

    SubjectSet existing = slotSubjects(cls, slot);

    if (existing.contains(subjectID)) {
        return false;
    }

    if (existing.size >= MAX_GROUP_SUBJECTS) {
        return false;
    }

    Data& data = getData();

    for (int i = 0; i < existing.size; i++) {
        if (!data.groupedMatrix[existing.values[i]][subjectID]) {
            return false;
        }
    }

    return true;
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
    inline static double groupBonus = 10;
    inline static double incompleteGroupNotEnd = 35;
    inline static double lessonShiftCrossing = 250;

    static void init(const json& data) {
        equalLessons = data.value("equalLessons", equalLessons);
        notEqualsLessonsCountOnDay = data.value("notEqualsLessonsCountOnDay", notEqualsLessonsCountOnDay);
        lessonsEmptySlots = data.value("lessonsEmptySlots", lessonsEmptySlots);
        daysByHard = data.value("daysByHard", daysByHard);
        teacherFreeTime = data.value("teacherFreeTime", teacherFreeTime);
        groupBonus = data.value("groupBonus", groupBonus);
        incompleteGroupNotEnd = data.value("incompleteGroupNotEnd", incompleteGroupNotEnd);
        lessonShiftCrossing = data.value("lessonShiftCrossing", lessonShiftCrossing);
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
                SubjectSet si = slotSubjects(cls, i);
                SubjectSet sj = slotSubjects(cls, j);

                for (int k = 0; k < si.size; k++) {
                    if (sj.contains(si.values[k])) {
                        value += 1;
                    }
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
                SubjectSet subjects = slotSubjects(cls, base + lesson);

                for (int k = 0; k < subjects.size; k++) {
                    hards[day] += data.hardsById[subjects.values[k]];
                }
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

    static bool functionIsIncompleteGroup(int cls, int slot) {
        if (!occupied(cls, slot)) {
            return false;
        }

        SubjectSet subjects = slotSubjects(cls, slot);

        if (subjects.size != 1) {
            return false;
        }

        Data& data = getData();
        auto it = data.groupedWith.find(subjects.values[0]);

        return it != data.groupedWith.end() && !it->second.empty();
    }

    static double groupBonus(int cls, int day) {
        Data& data = getData();
        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        double value = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            SubjectSet subjects = slotSubjects(cls, base + lesson);

            if (subjects.size == 2) {
                value += 1;
            }
        }

        return -Weights::groupBonus * value;
    }

    static double incompleteGroupsAtEnd(int cls, int day) {
        Data& data = getData();
        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        double value = 0;

        for (int i = base; i < base + MAX_LESSON_IN_DAY; i++) {
            if (!functionIsIncompleteGroup(cls, i)) {
                continue;
            }

            for (int j = i + 1; j < base + MAX_LESSON_IN_DAY; j++) {
                if (occupied(cls, j) && !functionIsIncompleteGroup(cls, j)) {
                    value += 1;
                }
            }
        }

        return Weights::incompleteGroupNotEnd * value;
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

                value += Weights::teacherFreeTime * (pow(end - start - cnt + 1, 2) + 3 * max(0, 4 - cnt));

                if (shift == NUMBER_OF_SHIFTS - 1 || SHIFT_CROSSING <= 0) {
                    continue;
                }

                int another = (shift + 1) * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;

                for (int step = 0; step < SHIFT_CROSSING; step++) {
                    if (occupied(teacher, base + MAX_LESSON_IN_DAY - SHIFT_CROSSING + step) && occupied(teacher, another + step)) {
                        value += Weights::lessonShiftCrossing;
                    }
                }
            }
        }

        return value;
    }
};

const int FUNCTIONS_ARGUMENTS_COUNT = 6;

vector<double> getClassPoint(int cls) {
    vector<double> answer(FUNCTIONS_ARGUMENTS_COUNT, 0);

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        answer[0] += Functions::equalLessons(cls, day);
        answer[2] += Functions::lessonsEmptySlots(cls, day);
        answer[4] += Functions::groupBonus(cls, day);
        answer[5] += Functions::incompleteGroupsAtEnd(cls, day);
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
                    answer[name][day].push_back(json{{"subject", "#"}, {"teachers", json::array()}, {"extra", json::array()}});

                    continue;
                }

                vector<int> subjectOrder;
                map<int, vector<string>> teachersBySubject;

                for (edge& e : graph[cls][slot]) {
                    if (!teachersBySubject.count(e.value)) {
                        subjectOrder.push_back(e.value);
                    }

                    teachersBySubject[e.value].push_back(teacherNameByID[e.id]);
                }

                json entry;

                entry["subject"] = subjectNameByID[subjectOrder[0]];
                entry["teachers"] = teachersBySubject[subjectOrder[0]];
                entry["extra"] = json::array();

                for (int i = 1; i < (int)subjectOrder.size(); i++) {
                    entry["extra"].push_back(json{
                        {"subject", subjectNameByID[subjectOrder[i]]},
                        {"teachers", teachersBySubject[subjectOrder[i]]}
                    });
                }

                answer[name][day].push_back(entry);
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

    for (int teacher = 0; teacher < data.teachers.size(); teacher++) {
        for (int slot : data.free[teacher]) {
            teacherAllowed[teacher + 1][slot] = true;
        }
    }

    vector<Lesson> pending;

    for (auto& key : data.classes) {
        json& value = data.lessons[key];

        int cls = IDByClassName[key];
        int base = data.classShiftOffset[cls];

        for (auto subject : value) {
            vector<int> ids;

            for (auto& teacher : subject["teachers"]) {
                ids.push_back(IDByTeacherName[teacher]);
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
                if (!canPlaceLesson(item.cls, slot, item.subjectID)) {
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

        for (edge& e : group) {
            graph[item.cls][color].push_back(e);
        }
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
            ostringstream stream;

            stream << (equal == 10000 ? "[EQUAL]" : "[PRINT]") << " ";
            stream << iter + 1 << " " << temperature << " " << total << " " << equal;

            string prefix = stream.str();

            cout << prefix;

            int len = prefix.size();

            if (len < 40) {
                std::cout << string(40 - len, ' ');
            }

            cout << "| ";

            for (auto element : getClassPoint()) {
                cout << element << " ";
            }

            cout << "\n";
        }

        if (equal == 10000) {
            temperature = 20;

            equal = 0;
        }

        int type = randint(0, 2);

        if (type == 0) {
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
        }

        if (type == 1) {
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

            for (int teacher : involvedTeachers) {
                after += Functions::teacherFreeTime(teacher);
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

        if (type == 2) {
            int shift = randint(0, NUMBER_OF_SHIFTS - 1);

            if (data.classesByShift[shift].empty()) {
                continue;
            }

            auto& shiftClasses = data.classesByShift[shift];
            int cls = shiftClasses[randint(0, shiftClasses.size() - 1)];

            int off = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;
            int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

            int slotA = off + randint(0, week - 1);

            if (!occupied(cls, slotA)) {
                continue;
            }

            SubjectSet subjectsA = slotSubjects(cls, slotA);
            int subjectID = subjectsA.values[randint(0, subjectsA.size - 1)];

            vector<int> involvedTeachers;

            for (edge& e : graph[cls][slotA]) {
                if (e.value == subjectID) {
                    involvedTeachers.push_back(e.id);
                }
            }

            vector<int> groupCandidates, emptyCandidates;

            for (int slot = off; slot < off + week; slot++) {
                if (slot == slotA) {
                    continue;
                }

                if (!canPlaceLesson(cls, slot, subjectID)) {
                    continue;
                }

                bool teachersOk = true;

                for (int t : involvedTeachers) {
                    if (!teacherAllowed[t][slot] || occupied(t, slot)) {
                        teachersOk = false;
                        break;
                    }
                }

                if (!teachersOk) {
                    continue;
                }

                if (occupied(cls, slot)) {
                    groupCandidates.push_back(slot);

                } else {
                    emptyCandidates.push_back(slot);
                }
            }

            int slotB;

            if (!groupCandidates.empty()) {
                slotB = groupCandidates[randint(0, groupCandidates.size() - 1)];

            } else if (!emptyCandidates.empty()) {
                slotB = emptyCandidates[randint(0, emptyCandidates.size() - 1)];

            } else {
                continue;
            }

            double before = getClassTotal(cls);

            for (int t : involvedTeachers) {
                before += Functions::teacherFreeTime(t);
            }

            vector<edge> moving;

            for (auto it = graph[cls][slotA].begin(); it != graph[cls][slotA].end(); ) {
                if (it->value == subjectID) {
                    moving.push_back(*it);

                    it = graph[cls][slotA].erase(it);

                } else {
                    it += 1;
                }
            }

            auto applyMove = [&]() {
                for (edge& e : moving) {
                    graph[cls][slotB].push_back(edge(e.id, subjectID));
                    graph[e.id][slotB] = {edge(cls, subjectID)};
                    graph[e.id][slotA].clear();
                }
            };

            auto revertMove = [&]() {
                for (edge& e : moving) {
                    vector<edge>& vb = graph[cls][slotB];

                    for (auto it = vb.begin(); it != vb.end(); ++it) {
                        if (it->id == e.id && it->value == subjectID) {
                            vb.erase(it);
                            break;
                        }
                    }

                    graph[e.id][slotB].clear();
                    graph[e.id][slotA] = {edge(cls, subjectID)};
                }

                for (edge& e : moving) {
                    graph[cls][slotA].push_back(e);
                }
            };

            count += 1;

            applyMove();

            double after = getClassTotal(cls);

            for (int t : involvedTeachers) {
                after += Functions::teacherFreeTime(t);
            }

            double delta = after - before;

            if (delta < 0 || double(randint(1, 1e7)) / 1e7 < exp(-delta / temperature)) {
                total = total - before + after;

                equal = 0;

            } else {
                revertMove();

                equal += 1;
            }
        }
    }

    std::ofstream file(output);

    file << std::setw(4) << save() << std::endl;
    file.close();

    cout << count << " " << total << endl;

    return 0;
}
