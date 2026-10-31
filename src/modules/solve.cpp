#include <bits/stdc++.h>
#include <ext/random>
#include <windows.h>

#pragma GCC optimize("unroll-loops")

#include "libs/CLI11.hpp"
#include "libs/json.hpp"

using namespace std;

using json = nlohmann::json;

int JOB_WEEK_LENGHT     = 5;
int MAX_LESSON_IN_DAY   = 8;
int NUMBER_OF_SHIFTS    = 1;
int SHIFT_CROSSING      = 0;
int TEACHER_MAX_LESSONS = 9;

int SLOTS = 0;

const int MAX_GROUP_SUBJECTS = 10;
const int TEACHER_SMALL_DAY = 4;

int SUBJECT_MULTI_DAY_THRESHOLD = 4;

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

map<int, string> classroomGroupNameByID;
map<string, int> IDByClassroomGroupName;

map<int, string> classroomNameByID;
map<string, int> IDByClassroomName;

struct Constant {
    int cls, slot, subjectID;
};

class Data {
public:
    json lessons;

    vector<vector<int>> subjectHoursByClass;

    vector<vector<int>> free;
    vector<vector<int>> reserve;

    map<string, int> hards;
    vector<string> teachers, classes;

    vector<int> classShifts;

    vector<float> hardsById;
    vector<float> capacityDaysByHard{1, 1.4, 1.4, 1, 1.4, 1, 1};

    vector<int> classShiftOffset;
    vector<vector<int>> classesByShift;

    vector<vector<vector<int>>> groups;
    vector<vector<int>> groupMaskBySubject;

    vector<Constant> constants;

    bool classroomsEnable = false;

    vector<vector<int>> classroomsGroups;
    vector<vector<int>> classroomsTeacher;

    vector<vector<vector<int>>> roomGroupsByTeacherSubject;

    vector<vector<char>> crossing;

    bool anyCrossingForbidden = false;

    Data() {
        ifstream file(input);

        json settings;

        if (file.is_open()) {
            settings = json::parse(file);

        } else {
            throw runtime_error("Can not open input file: " + input);
        }

        JOB_WEEK_LENGHT     = settings["working_days_per_week"];
        MAX_LESSON_IN_DAY   = settings["max_lesson_count_per_day"];
        NUMBER_OF_SHIFTS    = settings["number_of_shifts"];
        SHIFT_CROSSING      = settings["shift_crossing"];
        TEACHER_MAX_LESSONS = settings["max_lesson_for_teacher"];

        SLOTS = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * NUMBER_OF_SHIFTS;

        for (auto entry : settings["subjects"]) {
            hards[entry[0]] = entry[1];
        }

        for (int number = 1; number <= settings["classes"]["count"].size(); number++) {
            for (int letter = 1; letter <= settings["classes"]["count"][number - 1]; letter++) {
                classes.push_back(to_string(number) + " " + CLASSES_LETTERS[letter]);

                int shift = 0;

                if (settings["classes"].contains("shift") && number - 1 < (int) settings["classes"]["shift"].size()) {
                    auto& entry = settings["classes"]["shift"][number - 1];

                    if (entry.is_array()) {
                        if (letter - 1 < entry.size() && entry[letter - 1].is_number()) {
                            shift = entry[letter - 1];
                        }

                    } else if (entry.is_number()) {
                        shift = entry;
                    }
                }

                classShifts.push_back(max(0, min(shift, NUMBER_OF_SHIFTS - 1)));
            }
        }

        classroomsEnable = settings["classrooms"]["enable"] != 0;

        int groupID = 1;

        set<string> rooms;

        classroomsGroups.push_back(vector<int>());

        for (auto& [name, var] : settings["classrooms"]["rooms"].items()) {
            classroomGroupNameByID[groupID] = name;
            IDByClassroomGroupName[name] = groupID;

            groupID += 1;

            classroomsGroups.push_back(vector<int>());

            for (auto room : var) {
                int index = 0;

                if (rooms.count(room) == 0) {
                    rooms.insert(room);

                    classroomNameByID[rooms.size()] = room;
                    IDByClassroomName[room] = rooms.size();

                    index = rooms.size();

                } else {
                    index = IDByClassroomName[room];
                }

                classroomsGroups.back().push_back(index);
            }
        }

        for (auto& [name, teacher] : settings["teachers"].items()) {
            teachers.push_back(name);

            vector<int> exclude;

            for (int shift = 0; shift < NUMBER_OF_SHIFTS; shift++) {
                for (vector<int> freeSlot : teacher["free"][shift]) {
                    exclude.push_back(JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * shift + MAX_LESSON_IN_DAY * freeSlot[0] + freeSlot[1]);
                }
            }

            vector<int> reserving;

            if (teacher.contains("reserve") && teacher["reserve"].is_array()) {
                for (int shift = 0; shift < NUMBER_OF_SHIFTS && shift < (int) teacher["reserve"].size(); shift++) {
                    for (vector<int> reserveSlot : teacher["reserve"][shift]) {
                        int value = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY * shift + MAX_LESSON_IN_DAY * reserveSlot[0] + reserveSlot[1];

                        if (value < 0 || value >= SLOTS) {
                            continue;
                        }

                        exclude.push_back(value);
                        reserving.push_back(value);
                    }
                }
            }

            reserve.push_back(reserving);

            free.push_back(vector<int>());

            for (int slot = 0; slot < SLOTS; slot++) {
                bool found = false;

                for (int index = 0; index < exclude.size(); index++) {
                    if (slot == exclude[index]) {
                        found = true;
                        break;
                    }
                }

                if (found) {
                    continue;
                }

                free.back().push_back(slot);
            }
        }

        for (string& cls : classes) {
            lessons[cls] = json::array();

            for (auto& [subject, hours] : settings["classes"]["lessons"][cls].items()) {
                if (hours == 0) {
                    continue;
                }

                vector<string> teacherCandidates;

                for (string& teacher : teachers) {
                    for (auto& subjectEntry : settings["teachers"][teacher]["subjects"]) {
                        if (subjectEntry["subject"] == subject) {
                            bool found = false;

                            for (auto used : subjectEntry["classes"]) {
                                if (used == cls) {
                                    found = true;
                                }
                            }

                            if (found) {
                                teacherCandidates.push_back(teacher);
                            }
                        }
                    }
                }

                if (teacherCandidates.size()) {
                    lessons[cls].push_back({{"subject", subject}, {"teachers", teacherCandidates}, {"hours", hours}});

                } else {
                    cout << "[WARNING] " << cls << " not found teacher for " << subject << "\n";
                }
            }
        }

        for (int index = 0; index < settings["subjects"].size(); index++) {
            subjectNameByID[index + 1] = settings["subjects"][index][0];
            IDBySubjectName[settings["subjects"][index][0]] = index + 1;
        }

        {
            int subjectCount = settings["subjects"].size();

            vector<vector<int>> explicitValue(subjectCount + 1, vector<int>(subjectCount + 1, -1));

            if (settings.contains("crossing") && settings["crossing"].is_object()) {
                for (auto& [si, row] : settings["crossing"].items()) {
                    if (!IDBySubjectName.count(si) || !row.is_object()) {
                        continue;
                    }

                    for (auto& [sj, value] : row.items()) {
                        if (!IDBySubjectName.count(sj)) {
                            continue;
                        }

                        int parsed;

                        if (value.is_boolean()) {
                            parsed = value.get<bool>() ? 1 : 0;

                        } else if (value.is_number()) {
                            parsed = value.get<double>() != 0 ? 1 : 0;

                        } else {
                            continue;
                        }

                        explicitValue[IDBySubjectName[si]][IDBySubjectName[sj]] = parsed;
                    }
                }
            }

            crossing.assign(subjectCount + 1, vector<char>(subjectCount + 1, 1));

            for (int a = 1; a <= subjectCount; a++) {
                for (int b = 1; b <= subjectCount; b++) {
                    if (a == b) {
                        crossing[a][a] = (explicitValue[a][a] == 1) ? 1 : 0;

                    } else {
                        crossing[a][b] = (explicitValue[a][b] == 0 || explicitValue[b][a] == 0) ? 0 : 1;
                    }
                }
            }

            for (int a = 1; a <= subjectCount; a++) {
                for (int b = a + 1; b <= subjectCount; b++) {
                    if (!crossing[a][b]) {
                        anyCrossingForbidden = true;
                    }
                }
            }
        }

        for (int index = 0; index < teachers.size(); index++) {
            teacherNameByID[index + 1] = teachers[index];
            IDByTeacherName[teachers[index]] = index + 1;
        }

        roomGroupsByTeacherSubject.assign(teachers.size() + 1, vector<vector<int>>(settings["subjects"].size() + 1));

        for (auto& [name, teacher] : settings["teachers"].items()) {
            int teacherID = IDByTeacherName[name];

            for (auto& element : teacher["subjects"]) {
                string subject = element["subject"];

                if (!IDBySubjectName.count(subject)) {
                    continue;
                }

                int subjectID = IDBySubjectName[subject];

                vector<int> ids;

                if (element.contains("classrooms")) {
                    for (string group : element["classrooms"]) {
                        if (IDByClassroomGroupName.count(group)) {
                            ids.push_back(IDByClassroomGroupName[group]);

                        } else {
                            cout << "[WARNING] teacher " << name << ": unknown classroom group \"" << group << "\"\n";
                        }
                    }
                }

                roomGroupsByTeacherSubject[teacherID][subjectID] = ids;
            }
        }

        for (int index = 0; index < classes.size(); index++) {
            classNameByID[teachers.size() + index + 1] = classes[index];
            IDByClassName[classes[index]] = teachers.size() + index + 1;
        }

        hardsById.assign(settings["subjects"].size() + 1, 0);

        for (int index = 0; index < settings["subjects"].size(); index++) {
            hardsById[index + 1] = hards[settings["subjects"][index][0]];
        }

        if (settings.contains("capacityDaysByHard")) {
            auto values = settings["capacityDaysByHard"];

            for (int day = 0; day < min(int(values.size()), JOB_WEEK_LENGHT); day++) {
                capacityDaysByHard[day] = values[day];
            }
        }

        classShiftOffset.assign(teachers.size() + classes.size() + 1, 0);

        for (int index = 0; index < classes.size(); index++) {
            classShiftOffset[teachers.size() + index + 1] = classShifts[index] * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;
        }

        classesByShift.assign(NUMBER_OF_SHIFTS, vector<int>());

        for (int index = 0; index < classes.size(); index++) {
            int clsID = teachers.size() + index + 1;

            classesByShift[classShifts[index]].push_back(clsID);
        }

        subjectHoursByClass.assign(teachers.size() + classes.size() + 1, vector<int>(settings["subjects"].size() + 1, 0));

        for (int index = 0; index < classes.size(); index++) {
            int clsID = teachers.size() + index + 1;

            for (auto& lessonEntry : lessons[classes[index]]) {
                string subject = lessonEntry["subject"].get<string>();

                int hours = lessonEntry["hours"].get<int>();

                if (IDBySubjectName.count(subject)) {
                    subjectHoursByClass[clsID][IDBySubjectName[subject]] = hours;
                }
            }
        }

        for (auto& [cls, items] : settings["constants"].items()) {
            if (!IDByClassName.count(cls)) {
                continue;
            }

            if (!items.is_object()) {
                continue;
            }

            for (auto& [key, value] : items.items()) {
                int day = -1, lesson = -1;

                if (sscanf(key.c_str(), "%d-%d", &day, &lesson) != 2) {
                    cout << "[WARNING] constants: bad key \"" << key << "\" for " << cls << "\n";

                    continue;
                }

                if (day < 0 || day >= JOB_WEEK_LENGHT || lesson < 0 || lesson >= MAX_LESSON_IN_DAY) {
                    cout << "[WARNING] constants: key \"" << key << "\" out of range for " << cls << "\n";

                    continue;
                }

                if (!value.is_string()) {
                    continue;
                }

                string subject = value;

                if (subject.empty() || subject == "-") {
                    continue;
                }

                if (!IDBySubjectName.count(subject)) {
                    cout << "[WARNING] constants: unknown subject \"" << subject << "\" for " << cls << "\n";

                    continue;
                }

                int slot = classShiftOffset[IDByClassName[cls]] + day * MAX_LESSON_IN_DAY + lesson;

                constants.push_back(Constant{IDByClassName[cls], slot, IDBySubjectName[subject]});
            }
        }

        groups.assign(teachers.size() + classes.size() + 1, vector<vector<int>>());

        for (auto& [cls, group] : settings["groups"].items()) {
            if (!IDByClassName.count(cls)) {
                continue;
            }

            groups[IDByClassName[cls]] = vector<vector<int>>();

            if (group.size() == 0) {
                vector<int> temp;

                for (auto entry : settings["subjects"]) {
                    temp.push_back(IDBySubjectName[entry[0]]);
                }

                groups[IDByClassName[cls]].push_back(temp);

            } else {
                for (auto& [_, subjects] : group.items()) {
                    vector<int> temp;

                    for (auto subject : subjects) {
                        temp.push_back(IDBySubjectName[subject]);
                    }

                    groups[IDByClassName[cls]].push_back(temp);
                }
            }
        }

        for (auto cls : classes) {
            if (settings["groups"].count(cls)) {
                continue;
            }

            groups[IDByClassName[cls]] = vector<vector<int>>();

            vector<int> temp;

            for (auto entry : settings["subjects"]) {
                temp.push_back(IDBySubjectName[entry[0]]);
            }

            groups[IDByClassName[cls]].push_back(temp);
        }

        groupMaskBySubject.assign(teachers.size() + classes.size() + 1, vector<int>());

        for (auto& cls : classes) {
            groupMaskBySubject[IDByClassName[cls]].assign(settings["subjects"].size() + 1, 0);

            int groupCount = groups[IDByClassName[cls]].size();

            for (int group = 0; group < groupCount; group++) {
                for (int subjectID : groups[IDByClassName[cls]][group]) {
                    if (subjectID >= 0 && subjectID <= settings["subjects"].size()) {
                        groupMaskBySubject[IDByClassName[cls]][subjectID] |= (1 << group);
                    }
                }
            }
        }
    }
};

Data& getData() {
    static Data instance;

    return instance;
}

Data* DATA = nullptr;

struct edge {
    int id = 0, value = 0;

    edge() {}

    edge(int id_, int value_) {
        id = id_;
        value = value_;
    }
};

vector<vector<vector<edge>>> graph;

vector<vector<char>> teacherIsAllowed;
vector<vector<char>> teacherReserve;

vector<uint64_t> teacherReserveMask;

vector<vector<int>> teacherRoom;
vector<vector<int>> roomOccupant;
vector<vector<int>> teacherRoomRank;

bool roomWarnings = true;

inline bool occupied(int row, int slot) {
    return !graph[row][slot].empty();
}

struct SubjectSet {
    int values[MAX_GROUP_SUBJECTS];
    int size = 0;

    inline bool contains(int value) const {
        for (int index = 0; index < size; index++) {
            if (values[index] == value) {
                return true;
            }
        }

        return false;
    }

    inline void insert(int value) {
        if (size < MAX_GROUP_SUBJECTS && !contains(value)) {
            values[size++] = value;
        }
    }
};

vector<vector<SubjectSet>> locked;

vector<SubjectSet> bufferSubjects;

vector<int> bufferCovered;
vector<int> bufferCounter;
vector<int> bufferEnds;

vector<float> bufferHards;

vector<int> bufferTeacherLengths;

inline bool slotLocked(int cls, int slot) {
    return locked[cls][slot].size > 0;
}

inline bool subjectLocked(int cls, int slot, int subjectID) {
    return locked[cls][slot].contains(subjectID);
}

inline SubjectSet slotSubjects(int row, int slot) {
    SubjectSet result;

    for (edge& connection : graph[row][slot]) {
        result.insert(connection.value);
    }

    return result;
}

inline bool subjectRepeatAllowed(int cls, int subjectID) {
    const Data& data = *DATA;

    if (subjectID <= 0 || subjectID >= (int) data.crossing.size()) {
        return true;
    }

    if (data.crossing[subjectID][subjectID]) {
        return true;
    }

    if (cls > 0 && cls < (int) data.subjectHoursByClass.size() && subjectID < (int) data.subjectHoursByClass[cls].size()) {
        return data.subjectHoursByClass[cls][subjectID] >= SUBJECT_MULTI_DAY_THRESHOLD;
    }

    return false;
}

inline bool subjectPairAllowed(int subjectA, int subjectB) {
    const Data& data = *DATA;

    if (subjectA <= 0 || subjectB <= 0 || subjectA >= (int) data.crossing.size() || subjectB >= (int) data.crossing.size()) {
        return true;
    }

    return data.crossing[subjectA][subjectB] != 0;
}

inline bool classDayConflict(int cls, int subjectID, int slot, int excludeSlot = -1) {
    if (subjectID <= 0) {
        return false;
    }

    const Data& data = *DATA;

    if (cls <= 0 || cls >= data.subjectHoursByClass.size()) {
        return false;
    }

    if (subjectID >= data.subjectHoursByClass[cls].size()) {
        return false;
    }

    const bool repeatAllowed = subjectRepeatAllowed(cls, subjectID);

    if (repeatAllowed && !data.anyCrossingForbidden) {
        return false;
    }

    int offset = data.classShiftOffset[cls];
    int base = offset + ((slot - offset) / MAX_LESSON_IN_DAY) * MAX_LESSON_IN_DAY;

    for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
        int check = base + lesson;

        for (const edge& connection : graph[cls][check]) {
            int other = connection.value;

            if (check == excludeSlot && other == subjectID) {
                continue;
            }

            if (other == subjectID) {
                if (check != slot && !repeatAllowed) {
                    return true;
                }

                continue;
            }

            if (!subjectPairAllowed(subjectID, other)) {
                return true;
            }
        }
    }

    return false;
}

inline bool classDayHasDuplicates(int cls, int slot) {
    const Data& data = *DATA;

    if (cls <= 0 || cls >= (int) data.subjectHoursByClass.size()) {
        return false;
    }

    static vector<int> distinct;

    distinct.clear();

    int offset = data.classShiftOffset[cls];
    int base = offset + ((slot - offset) / MAX_LESSON_IN_DAY) * MAX_LESSON_IN_DAY;

    bool bad = false;

    for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
        SubjectSet subjects = slotSubjects(cls, base + lesson);

        for (int index = 0; index < subjects.size; index++) {
            int subjectID = subjects.values[index];

            if (subjectID <= 0 || subjectID >= (int) bufferCounter.size()) {
                continue;
            }

            if (bufferCounter[subjectID]++ == 0) {
                distinct.push_back(subjectID);

            } else if (!subjectRepeatAllowed(cls, subjectID)) {
                bad = true;
            }
        }
    }

    if (!bad && data.anyCrossingForbidden) {
        for (int first = 0; first < (int) distinct.size() && !bad; first++) {
            for (int second = first + 1; second < (int) distinct.size(); second++) {
                if (!subjectPairAllowed(distinct[first], distinct[second])) {
                    bad = true;

                    break;
                }
            }
        }
    }

    for (int subjectID : distinct) {
        bufferCounter[subjectID] = 0;
    }

    return bad;
}

bool canPlaceLesson(int cls, int slot, int subjectID, int excludeSlot = -1) {
    if (classDayConflict(cls, subjectID, slot, excludeSlot)) {
        return false;
    }

    const vector<edge>& edges = graph[cls][slot];

    if (edges.empty()) {
        return true;
    }

    const vector<int>& mask = DATA->groupMaskBySubject[cls];

    int nw = subjectID >= 0 && subjectID < mask.size() ? mask[subjectID] : 0;

    if (nw == 0) {
        return false;
    }

    int seen[MAX_GROUP_SUBJECTS];

    int count = 0;
    int covered = 0;

    for (const edge& connection : edges) {
        int subject = connection.value;

        if (subject == subjectID) {
            return false;
        }

        bool duplicate = false;

        for (int index = 0; index < count; index++) {
            if (seen[index] == subject) {
                duplicate = true;

                break;
            }
        }

        if (duplicate) {
            continue;
        }

        if (count >= MAX_GROUP_SUBJECTS) {
            return false;
        }

        seen[count++] = subject;

        int subjectMask = subject >= 0 && subject < mask.size() ? mask[subject] : 0;

        if (subjectMask == 0) {
            return false;
        }

        covered |= subjectMask;
    }

    if (covered & nw) {
        return false;
    }

    return true;
}

pair<int, int> findRoomForTeacherRanked(int teacherID, int subjectID, int slot) {
    const Data& data = *DATA;

    if (!data.classroomsEnable) {
        return {0, 0};
    }

    if (teacherID <= 0 || teacherID >= data.roomGroupsByTeacherSubject.size()) {
        return {0, 0};
    }

    if (subjectID <= 0 || subjectID >= data.roomGroupsByTeacherSubject[teacherID].size()) {
        return {0, 0};
    }

    const vector<int>& groups = data.roomGroupsByTeacherSubject[teacherID][subjectID];

    if (groups.empty()) {
        return {0, 0};
    }

    for (int rank = 0; rank < groups.size(); rank++) {
        int groupID = groups[rank];

        if (groupID < 0 || groupID >= data.classroomsGroups.size()) {
            continue;
        }

        for (int roomID : data.classroomsGroups[groupID]) {
            if (roomOccupant[roomID][slot] == 0) {
                return {roomID, rank};
            }
        }
    }

    return {-1, -1};
}

int findRoomForTeacher(int teacherID, int subjectID, int slot) {
    return findRoomForTeacherRanked(teacherID, subjectID, slot).first;
}

void assignRoom(int teacherID, int subjectID, int slot) {
    pair<int, int> found = findRoomForTeacherRanked(teacherID, subjectID, slot);

    int room = found.first;
    int rank = found.second;

    if (room > 0) {
        roomOccupant[room][slot] = teacherID;

        teacherRoom[teacherID][slot] = room;
        teacherRoomRank[teacherID][slot] = rank;

    } else if (room == -1 && roomWarnings) {
        cout << "[WARNING] no available classroom for " << teacherNameByID[teacherID] << " / " << subjectNameByID[subjectID] << " at slot " << slot << "\n";
    }
}

void releaseRoom(int teacherID, int slot) {
    int room = teacherRoom[teacherID][slot];

    if (room > 0) {
        roomOccupant[room][slot] = 0;

        teacherRoom[teacherID][slot] = 0;
        teacherRoomRank[teacherID][slot] = 0;
    }
}

inline bool roomAvailableExcluding(int room, int slot, const vector<int>& excluding) {
    if (room == 0) {
        return true;
    }

    int occupant = roomOccupant[room][slot];

    if (occupant == 0) {
        return true;
    }

    for (int teacherID : excluding) {
        if (teacherID == occupant) {
            return true;
        }
    }

    return false;
}

bool roomsSwappable(const vector<int>& teachersList, int slotA, int slotB) {
    for (int teacherID : teachersList) {
        int roomA = teacherRoom[teacherID][slotA];
        int roomB = teacherRoom[teacherID][slotB];

        if (!roomAvailableExcluding(roomA, slotB, teachersList)) {
            return false;
        }

        if (!roomAvailableExcluding(roomB, slotA, teachersList)) {
            return false;
        }
    }

    return true;
}

void swapRoomsGroup(const vector<int>& teachersList, int slotA, int slotB) {
    for (int teacherID : teachersList) {
        int roomA = teacherRoom[teacherID][slotA];
        int roomB = teacherRoom[teacherID][slotB];

        if (roomA) {
            roomOccupant[roomA][slotA] = 0;
        }

        if (roomB) {
            roomOccupant[roomB][slotB] = 0;
        }
    }

    for (int teacherID : teachersList) {
        swap(teacherRoom[teacherID][slotA], teacherRoom[teacherID][slotB]);
        swap(teacherRoomRank[teacherID][slotA], teacherRoomRank[teacherID][slotB]);
    }

    for (int teacherID : teachersList) {
        if (teacherRoom[teacherID][slotA]) {
            roomOccupant[teacherRoom[teacherID][slotA]][slotA] = teacherID;
        }

        if (teacherRoom[teacherID][slotB]) {
            roomOccupant[teacherRoom[teacherID][slotB]][slotB] = teacherID;
        }
    }
}

bool verifyRooms() {
    Data& data = getData();

    bool ok = true;

    for (int teacherID = 1; teacherID <= (int)data.teachers.size(); teacherID++) {
        for (int slot = 0; slot < SLOTS; slot++) {
            int room = teacherRoom[teacherID][slot];

            if (room > 0 && roomOccupant[room][slot] != teacherID) {
                cout << "[ERROR] room mismatch: teacher " << teacherNameByID[teacherID] << ", room " << classroomNameByID[room]
                     << ", slot " << slot << ", roomOccupant says " << roomOccupant[room][slot] << "\n";

                ok = false;
            }
        }
    }

    for (int room = 1; room < roomOccupant.size(); room++) {
        for (int slot = 0; slot < SLOTS; slot++) {
            int teacherID = roomOccupant[room][slot];

            if (teacherID > 0 && teacherRoom[teacherID][slot] != room) {
                cout << "[ERROR] room mismatch: room " << classroomNameByID[room] << ", slot " << slot
                     << " claims teacher " << teacherNameByID[teacherID] << " who has room " << teacherRoom[teacherID][slot] << "\n";

                ok = false;
            }
        }
    }

    return ok;
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

void placeLesson(const Lesson& item, int slot) {
    vector<edge> group;

    for (int teacherID : item.ids) {
        graph[teacherID][slot] = {edge(item.cls, item.subjectID)};
        group.push_back(edge(teacherID, item.subjectID));

        assignRoom(teacherID, item.subjectID, slot);
    }

    for (edge& connection : group) {
        graph[item.cls][slot].push_back(connection);
    }
}

struct Weights {
    inline static float equalLessons = 5;
    inline static float notEqualsLessonsCountOnDay = 25;
    inline static float lessonsEmptySlots = 200;
    inline static float daysByHard = 2;
    inline static float teacherFreeTime = 5;
    inline static float teacherSmallDay = 5;
    inline static float groupBonus = 10;
    inline static float lessonShiftCrossing = 250;
    inline static float profileGaps = 200;
    inline static float classroomPriority = 50;
    inline static float teacherLessonLimit = 25;

    static void init(const json& data) {
        equalLessons = data.value("equalLessons", equalLessons);
        notEqualsLessonsCountOnDay = data.value("notEqualsLessonsCountOnDay", notEqualsLessonsCountOnDay);
        lessonsEmptySlots = data.value("lessonsEmptySlots", lessonsEmptySlots);
        daysByHard = data.value("daysByHard", daysByHard);
        teacherFreeTime = data.value("teacherFreeTime", teacherFreeTime);
        teacherSmallDay = data.value("teacherSmallDay", teacherSmallDay);
        groupBonus = data.value("groupBonus", groupBonus);
        lessonShiftCrossing = data.value("lessonShiftCrossing", lessonShiftCrossing);
        profileGaps = data.value("profileGaps", profileGaps);
        classroomPriority = data.value("classroomPriority", classroomPriority);
        teacherLessonLimit = data.value("teacherLessonLimit", teacherLessonLimit);
    }
};

inline int teacherDayGap(int teacherID, int day, int* out = nullptr) {
    const vector<vector<edge>>& row = graph[teacherID];

    const int step = MAX_LESSON_IN_DAY - max(0, SHIFT_CROSSING);
    const int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

    uint64_t used = 0;

    for (int shift = 0; shift < NUMBER_OF_SHIFTS; shift++) {
        const vector<edge>* cell = &row[shift * week + day * MAX_LESSON_IN_DAY];

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (!cell[lesson].empty()) {
                used |= 1ULL << (shift * step + lesson);
            }
        }
    }

    used |= teacherReserveMask[(size_t) teacherID * JOB_WEEK_LENGHT + day];

    if (out) {
        *out = __builtin_popcountll(used);
    }

    if (used == 0) {
        return 0;
    }

    const int first = __builtin_ctzll(used);
    const int last = 63 - __builtin_clzll(used);

    const uint64_t range = (2ULL << last) - (1ULL << first);

    return __builtin_popcountll(range & ~used);
}

inline int teacherDayLessons(const vector<vector<edge>>& row, int day) {
    int count = 0;

    for (int shift = 0; shift < NUMBER_OF_SHIFTS; shift++) {
        int base = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (!row[base + lesson].empty()) {
                count += 1;
            }
        }
    }

    return count;
}

inline int teacherDayLoad(int teacherID, int day) {
    const vector<vector<edge>>& row = graph[teacherID];

    int count = 0;

    for (int shift = 0; shift < NUMBER_OF_SHIFTS; shift++) {
        int base = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (!row[base + lesson].empty() || teacherReserve[teacherID][base + lesson]) {
                count += 1;
            }
        }
    }

    return count;
}

float lastTeacherGapCost = 0;

class Functions {
public:
    static float equalLessons(int cls, int day) {
        const Data& data = *DATA;

        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        float value = 0;

        for (int slotA = base; slotA < base + MAX_LESSON_IN_DAY; slotA++) {
            for (int slotB = slotA + 1; slotB < base + MAX_LESSON_IN_DAY; slotB++) {
                SubjectSet subjectsA = slotSubjects(cls, slotA);
                SubjectSet subjectsB = slotSubjects(cls, slotB);

                for (int index = 0; index < subjectsA.size; index++) {
                    if (subjectsB.contains(subjectsA.values[index])) {
                        value += 1;
                    }
                }
            }
        }

        return Weights::equalLessons * value;
    }

    static float notEqualsLessonsCountOnDay(int cls) {
        const Data& data = *DATA;

        int offset = data.classShiftOffset[cls];

        vector<int> lengths(JOB_WEEK_LENGHT, 0);

        float sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int base = offset + day * MAX_LESSON_IN_DAY;
            int last = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                if (occupied(cls, base + lesson)) {
                    last = lesson;
                }
            }

            lengths[day] = last;
            sum += last;
        }

        float avr = sum / JOB_WEEK_LENGHT;

        float value = 0;

        for (auto length : lengths) {
            value += pow(length - avr, 2.0);
        }

        return Weights::notEqualsLessonsCountOnDay * value;
    }

    static float lessonsEmptySlots(int cls, int day) {
        const Data& data = *DATA;

        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        float value = 0;

        int empty = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (occupied(cls, base + lesson)) {
                value += empty;

                empty = 0;

            } else {
                empty += 1;
            }
        }

        return Weights::lessonsEmptySlots * value;
    }

    static float profileGaps(int cls, int day) {
        const Data& data = *DATA;

        int count = data.groups[cls].size();

        if (count <= 1) {
            return 0;
        }

        const vector<int>& mask = data.groupMaskBySubject[cls];

        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        float value = 0;

        for (int group = 0; group < count; group++) {
            int bit = 1 << group;

            int gap = 0;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                SubjectSet subjects = slotSubjects(cls, base + lesson);

                int covered = 0;

                for (int index = 0; index < subjects.size; index++) {
                    int subjectID = subjects.values[index];

                    if (subjectID >= 0 && subjectID < mask.size()) {
                        covered |= mask[subjectID];
                    }
                }

                if (covered & bit) {
                    value += gap;

                    gap = 0;

                } else {
                    gap += 1;
                }
            }
        }

        return Weights::profileGaps * value;
    }

    static float daysByHard(int cls) {
        const Data& data = *DATA;

        int offset = data.classShiftOffset[cls];

        vector<float> hardByDay(JOB_WEEK_LENGHT, 0);

        float sum = 0;

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int base = offset + day * MAX_LESSON_IN_DAY;

            for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                SubjectSet subjects = slotSubjects(cls, base + lesson);

                float current = 0;

                for (int index = 0; index < subjects.size; index++) {
                    current += data.hardsById[subjects.values[index]];
                }

                hardByDay[day] += current / max(1, subjects.size) * (static_cast<float>(lesson + 1) / MAX_LESSON_IN_DAY + 1);
            }

            hardByDay[day] /= data.capacityDaysByHard[day % data.capacityDaysByHard.size()];

            sum += hardByDay[day];
        }

        float avr = sum / JOB_WEEK_LENGHT;

        float value = 0;

        for (auto hard : hardByDay) {
            value += abs(avr - hard);
        }

        return Weights::daysByHard * value;
    }

    static float groupBonus(int cls, int day) {
        const Data& data = *DATA;

        int base = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

        float value = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            SubjectSet subjects = slotSubjects(cls, base + lesson);

            if (subjects.size >= 2) {
                value += subjects.size * (subjects.size - 1) / 2.0;
            }
        }

        return -Weights::groupBonus * value;
    }

    static float teacherFreeTime(int teacherID) {
        float value = 0;

        const vector<vector<edge>>& row = graph[teacherID];

        fill(bufferTeacherLengths.begin(), bufferTeacherLengths.end(), 0);

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int gap = teacherDayGap(teacherID, day);

            bufferTeacherLengths[day] = teacherDayLoad(teacherID, day);

            value += Weights::teacherFreeTime * static_cast<float>(gap * gap);
        }

        lastTeacherGapCost = value;

        if (SHIFT_CROSSING > 0) {
            for (int shift = 0; shift < NUMBER_OF_SHIFTS - 1; shift++) {
                for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
                    int base = shift * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;
                    int next = (shift + 1) * JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY + day * MAX_LESSON_IN_DAY;

                    for (int step = 0; step < SHIFT_CROSSING; step++) {
                        int left = base + MAX_LESSON_IN_DAY - SHIFT_CROSSING + step;
                        int right = next + step;

                        bool leftBusy = !row[left].empty() || teacherReserve[teacherID][left];
                        bool rightBusy = !row[right].empty() || teacherReserve[teacherID][right];

                        if (leftBusy && rightBusy) {
                            value += Weights::lessonShiftCrossing;
                        }
                    }
                }
            }
        }

        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            value += Weights::teacherLessonLimit * max(0, bufferTeacherLengths[day] - TEACHER_MAX_LESSONS);

            if (bufferTeacherLengths[day] > 0) {
                int difference = max(0, TEACHER_SMALL_DAY - bufferTeacherLengths[day]);

                value += Weights::teacherSmallDay * static_cast<float>(difference * difference);
            }
        }

        return value;
    }

    static float classroomPriority(int teacherID) {
        float value = 0;

        for (int slot = 0; slot < SLOTS; slot++) {
            if (teacherRoom[teacherID][slot] > 0) {
                value += teacherRoomRank[teacherID][slot];
            }
        }

        return Weights::classroomPriority * value;
    }
};

const int FUNCTIONS_ARGUMENTS_COUNT = 6;

vector<float> getClassPoint(int cls) {
    vector<float> answer(FUNCTIONS_ARGUMENTS_COUNT, 0);

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        answer[0] += Functions::equalLessons(cls, day);
        answer[2] += Functions::lessonsEmptySlots(cls, day);
        answer[4] += Functions::groupBonus(cls, day);
        answer[5] += Functions::profileGaps(cls, day);
    }

    answer[1] += Functions::notEqualsLessonsCountOnDay(cls);
    answer[3] += Functions::daysByHard(cls);

    return answer;
}

vector<float> getClassPoint() {
    const Data& data = *DATA;

    vector<float> answer(FUNCTIONS_ARGUMENTS_COUNT, 0);

    for (int cls = data.teachers.size() + 1; cls < data.teachers.size() + data.classes.size() + 1; cls++) {
        vector<float> temp = getClassPoint(cls);

        for (int index = 0; index < FUNCTIONS_ARGUMENTS_COUNT; index++) {
            answer[index] += temp[index];
        }
    }

    return answer;
}

float getClassTotal(int cls) {
    const Data& data = *DATA;

    const int offset = data.classShiftOffset[cls];

    const vector<int>& mask = data.groupMaskBySubject[cls];

    const vector<vector<edge>>& row = graph[cls];

    float answer = 0;

    float sumEnd = 0;
    float sumHard = 0;

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        const int base = offset + day * MAX_LESSON_IN_DAY;

        float equal = 0;
        float empty = 0;
        float bonus = 0;
        float hard = 0;

        int emptyRun = 0;
        int last = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            SubjectSet& subjects = bufferSubjects[lesson];

            subjects.size = 0;

            for (const edge& connection : row[base + lesson]) {
                subjects.insert(connection.value);
            }

            if (subjects.size == 0) {
                emptyRun += 1;

                bufferCovered[lesson] = 0;

                continue;
            }

            last = lesson;

            empty += emptyRun;
            emptyRun = 0;

            float current = 0;
            int covered = 0;

            for (int index = 0; index < subjects.size; index++) {
                int subjectID = subjects.values[index];

                current += data.hardsById[subjectID];

                equal += bufferCounter[subjectID]++;

                if (subjectID >= 0 && subjectID < mask.size()) {
                    covered |= mask[subjectID];
                }
            }

            bufferCovered[lesson] = covered;

            hard += current / subjects.size * (static_cast<float>(lesson + 1) / MAX_LESSON_IN_DAY + 1);

            if (subjects.size >= 2) {
                bonus += subjects.size * (subjects.size - 1) / 2.0;
            }
        }

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            for (int index = 0; index < bufferSubjects[lesson].size; index++) {
                bufferCounter[bufferSubjects[lesson].values[index]] = 0;
            }
        }

        float gaps = 0;

        if (data.groups[cls].size() > 1) {
            for (int group = 0; group < data.groups[cls].size(); group++) {
                int bit = 1 << group;

                int gap = 0;

                for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
                    if (bufferCovered[lesson] & bit) {
                        gaps += gap;

                        gap = 0;

                    } else {
                        gap += 1;
                    }
                }
            }
        }

        answer += Weights::equalLessons * equal;
        answer += Weights::lessonsEmptySlots * empty;
        answer -= Weights::groupBonus * bonus;
        answer += Weights::profileGaps * gaps;

        hard /= data.capacityDaysByHard[day % (data.capacityDaysByHard.size())];

        bufferHards[day] = hard;
        bufferEnds[day] = last;

        sumHard += hard;
        sumEnd += last;
    }

    float avr = sumEnd / JOB_WEEK_LENGHT;

    float value = 0;

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        float diff = bufferEnds[day] - avr;

        value += diff * diff;
    }

    answer += Weights::notEqualsLessonsCountOnDay * value;

    float averageHard = sumHard / JOB_WEEK_LENGHT;

    value = 0;

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        value += abs(averageHard - bufferHards[day]);
    }

    answer += Weights::daysByHard * value;

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

inline bool accept(float delta, float temperature) {
    if (delta < 0) {
        return true;
    }

    float ratio = delta / temperature;

    if (ratio > 16.2f) {
        return false;
    }

    return static_cast<float>(randint(1, 10000000)) / 1e7 < exp(-ratio);
}

float TEACHER_FAIR = 100;

float teacherGaps(int teacherID) {
    float value = 0;

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        int gap = teacherDayGap(teacherID, day);

        value += Weights::teacherFreeTime * static_cast<float>(gap * gap);
    }

    return value;
}

inline float fair(float gap) {
    return TEACHER_FAIR > 0 ? gap * gap / TEACHER_FAIR : 0.0f;
}

float teacherCost(int teacherID) {
    float cost = Functions::teacherFreeTime(teacherID);

    if (TEACHER_FAIR > 0) {
        cost += fair(lastTeacherGapCost);
    }

    return cost;
}

int verifyNoDuplicates() {
    Data& data = getData();

    int bad = 0;

    for (int cls = data.teachers.size() + 1; cls < data.teachers.size() + data.classes.size() + 1; cls++) {
        for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
            int slot = data.classShiftOffset[cls] + day * MAX_LESSON_IN_DAY;

            if (classDayHasDuplicates(cls, slot)) {
                cout << "[ERROR] day rule violated (repeat or forbidden subject pair): " << classNameByID[cls] << ", day " << day << "\n";

                bad++;
            }
        }
    }

    return bad;
}

struct KempeUnit {
    int cls = 0, from = 0, subject = 0;
    vector<int> ids;
};

struct KempeStart {
    int A = -1, B = -1, cls = 0, subject = 0;
};

struct KempeStats {
    long long tried[3] = {0, 0, 0}, built[3] = {0, 0, 0}, valid[3] = {0, 0, 0}, accepted[3] = {0, 0, 0}, improved[3] = {0, 0, 0};
};

KempeStats kempeStats;

int KEMPE_MAX_UNITS = 24;

inline bool pairCompatible(int cls, int subjectA, int subjectB) {
    if (subjectA == subjectB) {
        return false;
    }

    const vector<int>& mask = DATA->groupMaskBySubject[cls];

    int maskA = (subjectA >= 0 && subjectA < mask.size()) ? mask[subjectA] : 0;
    int maskB = (subjectB >= 0 && subjectB < mask.size()) ? mask[subjectB] : 0;

    return maskA != 0 && maskB != 0 && (maskA & maskB) == 0;
}

bool kempeBuild(int A, int B, int startCls, int startSubject, vector<KempeUnit>& chain) {
    chain.clear();

    auto add = [&](int cls, int slot, int subject) -> bool {
        for (const KempeUnit& existing : chain) {
            if (existing.cls == cls && existing.from == slot && existing.subject == subject) {
                return true;
            }
        }

        KempeUnit unit;

        unit.cls = cls;
        unit.from = slot;
        unit.subject = subject;

        for (const edge& connection : graph[cls][slot]) {
            if (connection.value == subject) {
                unit.ids.push_back(connection.id);
            }
        }

        if (unit.ids.empty()) {
            return false;
        }

        chain.push_back(unit);

        return true;
    };

    if (!add(startCls, A, startSubject)) {
        return false;
    }

    for (size_t index = 0; index < chain.size(); index++) {
        if (chain.size() > KEMPE_MAX_UNITS) {
            return false;
        }

        KempeUnit chainUnit = chain[index];

        int oppositeSlot = (chainUnit.from == A) ? B : A;

        if (subjectLocked(chainUnit.cls, chainUnit.from, chainUnit.subject)) {
            return false;
        }

        for (int id : chainUnit.ids) {
            if (!teacherIsAllowed[id][oppositeSlot]) {
                return false;
            }

            if (!graph[id][oppositeSlot].empty()) {
                int otherCls = graph[id][oppositeSlot][0].id;
                int otherSubject = graph[id][oppositeSlot][0].value;

                if (!add(otherCls, oppositeSlot, otherSubject)) {
                    return false;
                }
            }
        }

        SubjectSet subjects = slotSubjects(chainUnit.cls, oppositeSlot);

        for (int subjectIndex = 0; subjectIndex < subjects.size; subjectIndex++) {
            if (!pairCompatible(chainUnit.cls, chainUnit.subject, subjects.values[subjectIndex])) {
                if (!add(chainUnit.cls, oppositeSlot, subjects.values[subjectIndex])) {
                    return false;
                }
            }
        }
    }

    return chain.size() <= KEMPE_MAX_UNITS;
}

inline int kempeShiftForDay(int teacherID, int shift, int day) {
    int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

    int bestShift = -1, bestCount = INT_MAX;

    for (int candidateShift = 0; candidateShift < NUMBER_OF_SHIFTS; candidateShift++) {
        int currentShift = (candidateShift == 0) ? shift : (candidateShift <= shift ? candidateShift - 1 : candidateShift);

        int count = 0;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (!graph[teacherID][currentShift * week + day * MAX_LESSON_IN_DAY + lesson].empty()) {
                count++;
            }
        }

        if (candidateShift == 0 && count > 0) {
            return shift;
        }

        if (count > 0 && count < bestCount) {
            bestCount = count;

            bestShift = currentShift;
        }
    }

    return bestShift;
}

bool kempePickSmallDay(int teacherID, int shift, int& slotA, int& slotB) {
    int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

    vector<int> dailyLessons(JOB_WEEK_LENGHT, 0);
    vector<int> smallDays;

    for (int day = 0; day < JOB_WEEK_LENGHT; day++) {
        dailyLessons[day] = teacherDayLessons(graph[teacherID], day);

        if (dailyLessons[day] == 0) {
            continue;
        }

        if (teacherDayLoad(teacherID, day) < TEACHER_SMALL_DAY || teacherDayGap(teacherID, day) > 0) {
            smallDays.push_back(day);
        }
    }

    if (smallDays.empty()) {
        return false;
    }

    int firstDay = smallDays[randint(0, smallDays.size() - 1)];

    int chosenShift = kempeShiftForDay(teacherID, shift, firstDay);

    if (chosenShift < 0) {
        return false;
    }

    vector<int> lessonSlots;

    for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
        int slot = chosenShift * week + firstDay * MAX_LESSON_IN_DAY + lesson;

        if (!graph[teacherID][slot].empty()) {
            lessonSlots.push_back(slot);
        }
    }

    if (lessonSlots.empty()) {
        return false;
    }

    slotA = lessonSlots[randint(0, lessonSlots.size() - 1)];

    vector<int> candidates;

    for (int secondDay = 0; secondDay < JOB_WEEK_LENGHT; secondDay++) {
        if (secondDay == firstDay || dailyLessons[secondDay] == 0) {
            continue;
        }

        int base = chosenShift * week + secondDay * MAX_LESSON_IN_DAY;

        int first = -1, last = -1;

        for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
            if (!graph[teacherID][base + lesson].empty() || teacherReserve[teacherID][base + lesson]) {
                if (first == -1) {
                    first = lesson;
                }

                last = lesson;
            }
        }

        if (first == -1) {
            continue;
        }

        for (int lesson = first; lesson <= last; lesson++) {
            if (graph[teacherID][base + lesson].empty() && !teacherReserve[teacherID][base + lesson]) {
                candidates.push_back(base + lesson);
            }
        }

        if (first > 0) {
            candidates.push_back(base + first - 1);
        }

        if (last < MAX_LESSON_IN_DAY - 1) {
            candidates.push_back(base + last + 1);
        }
    }

    if (candidates.empty()) {
        return false;
    }

    slotB = candidates[randint(0, candidates.size() - 1)];

    return slotA != slotB;
}

bool kempePickWindow(int teacherID, int shift, int& slotA, int& slotB) {
    int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

    int day = randint(0, JOB_WEEK_LENGHT - 1);
    int base = shift * week + day * MAX_LESSON_IN_DAY;

    int first = -1, last = -1, count = 0;

    for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
        bool real = !graph[teacherID][base + lesson].empty();

        if (real || teacherReserve[teacherID][base + lesson]) {
            if (first == -1) {
                first = lesson;
            }

            last = lesson;
        }

        if (real) {
            count++;
        }
    }

    if (count == 0) {
        return false;
    }

    static vector<int> gapSlots;

    gapSlots.clear();

    for (int lesson = first; lesson <= last; lesson++) {
        if (graph[teacherID][base + lesson].empty() && !teacherReserve[teacherID][base + lesson]) {
            gapSlots.push_back(base + lesson);
        }
    }

    if (gapSlots.empty()) {
        return false;
    }

    slotB = gapSlots[randint(0, gapSlots.size() - 1)];

    static vector<int> realSlots, endSlots;

    realSlots.clear();
    endSlots.clear();

    for (int lesson = 0; lesson < MAX_LESSON_IN_DAY; lesson++) {
        if (!graph[teacherID][base + lesson].empty()) {
            realSlots.push_back(base + lesson);
        }
    }

    if (!graph[teacherID][base + first].empty()) {
        endSlots.push_back(base + first);
    }

    if (last != first && !graph[teacherID][base + last].empty()) {
        endSlots.push_back(base + last);
    }

    if (!endSlots.empty() && randint(1, 10) <= 7) {
        slotA = endSlots[randint(0, endSlots.size() - 1)];

    } else {
        slotA = realSlots[randint(0, realSlots.size() - 1)];
    }

    return true;
}

inline bool kempePickTeacher(int kind, int t, int sh, KempeStart& k) {
    bool found = (kind == 1) ? kempePickWindow(t, sh, k.A, k.B) : kempePickSmallDay(t, sh, k.A, k.B);

    if (!found) {
        return false;
    }

    k.cls = graph[t][k.A][0].id;
    k.subject = graph[t][k.A][0].value;

    return true;
}

inline bool kempePickRandom(int sh, KempeStart& k) {
    const vector<int>& shiftClasses = DATA->classesByShift[sh];

    if (shiftClasses.empty()) {
        return false;
    }

    int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;
    int offset = sh * week;

    int cls = shiftClasses[randint(0, shiftClasses.size() - 1)];

    k.A = offset + randint(0, week - 1);

    if (!occupied(cls, k.A)) {
        return false;
    }

    SubjectSet subjects = slotSubjects(cls, k.A);

    k.cls = cls;
    k.subject = subjects.values[randint(0, subjects.size - 1)];

    if (randint(0, 1)) {
        k.B = k.A - k.A % MAX_LESSON_IN_DAY + randint(0, MAX_LESSON_IN_DAY - 1);

    } else {
        k.B = offset + randint(0, week - 1);
    }

    return k.A != k.B;
}

int kempeMove(int A, int B, int startCls, int startSubject, int kind, float temperature, double& total, int& equal, int& count) {
    static vector<KempeUnit> chain;
    static vector<int> involved, classes;

    kempeStats.tried[kind]++;

    if (!kempeBuild(A, B, startCls, startSubject, chain)) {
        return 0;
    }

    kempeStats.built[kind]++;

    involved.clear();
    classes.clear();

    for (const KempeUnit& chainUnit : chain) {
        classes.push_back(chainUnit.cls);

        for (int id : chainUnit.ids) {
            involved.push_back(id);
        }
    }

    sort(classes.begin(), classes.end());
    classes.erase(unique(classes.begin(), classes.end()), classes.end());

    sort(involved.begin(), involved.end());
    involved.erase(unique(involved.begin(), involved.end()), involved.end());

    if (!roomsSwappable(involved, A, B)) {
        return 0;
    }

    kempeStats.valid[kind]++;

    float before = 0;

    for (int cls : classes) {
        before += getClassTotal(cls);
    }

    for (int teacherID : involved) {
        before += teacherCost(teacherID);
    }

    auto flip = [&](bool back) {
        for (const KempeUnit& chainUnit : chain) {
            int toSlot = (chainUnit.from == A) ? B : A;
            int sourceSlot = back ? toSlot : chainUnit.from;

            vector<edge>& edges = graph[chainUnit.cls][sourceSlot];

            edges.erase(remove_if(edges.begin(), edges.end(), [&](const edge& connection) { return connection.value == chainUnit.subject; }), edges.end());
        }

        for (const KempeUnit& chainUnit : chain) {
            int toSlot = (chainUnit.from == A) ? B : A;
            int destSlot = back ? chainUnit.from : toSlot;

            for (int id : chainUnit.ids) {
                graph[chainUnit.cls][destSlot].push_back(edge(id, chainUnit.subject));
            }
        }

        for (int teacherID : involved) {
            swap(graph[teacherID][A], graph[teacherID][B]);
        }

        swapRoomsGroup(involved, A, B);
    };

    count++;

    flip(false);

    if (A / MAX_LESSON_IN_DAY != B / MAX_LESSON_IN_DAY) {
        bool hard = false;

        for (int cls : classes) {
            if (classDayHasDuplicates(cls, A) || classDayHasDuplicates(cls, B)) {
                hard = true;

                break;
            }
        }

        if (hard) {
            flip(true);

            equal += 1;

            return 2;
        }
    }

    float after = 0;

    for (int cls : classes) {
        after += getClassTotal(cls);
    }

    for (int teacherID : involved) {
        after += teacherCost(teacherID);
    }

    float delta = after - before;

    if (accept(delta, temperature)) {
        total = total - before + after;

        equal = 0;

        kempeStats.accepted[kind]++;

        if (delta < -0.01f) {
            kempeStats.improved[kind]++;
        }

        return 1;
    }

    flip(true);

    equal += 1;

    return 2;
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
                    answer[name][day].push_back(json{{"subject", "#"}, {"teachers", json::array()}, {"classrooms", json::array()}, {"extra", json::array()}});

                    continue;
                }

                vector<int> subjectOrder;
                map<int, vector<string>> teachersBySubject;

                for (edge& connection : graph[cls][slot]) {
                    if (!teachersBySubject.count(connection.value)) {
                        subjectOrder.push_back(connection.value);
                    }

                    teachersBySubject[connection.value].push_back(teacherNameByID[connection.id]);
                }

                auto roomsForSubject = [&](int subjectID) {
                    set<string> names;

                    for (edge& connection : graph[cls][slot]) {
                        if (connection.value != subjectID) {
                            continue;
                        }

                        int room = data.classroomsEnable ? teacherRoom[connection.id][slot] : 0;

                        if (room > 0) {
                            names.insert(classroomNameByID[room]);
                        }
                    }

                    return vector<string>(names.begin(), names.end());
                };

                json entry;

                entry["subject"] = subjectNameByID[subjectOrder[0]];
                entry["teachers"] = teachersBySubject[subjectOrder[0]];
                entry["classrooms"] = roomsForSubject(subjectOrder[0]);
                entry["extra"] = json::array();

                for (int index = 1; index < subjectOrder.size(); index++) {
                    entry["extra"].push_back(json{
                        {"subject", subjectNameByID[subjectOrder[index]]},
                        {"teachers", teachersBySubject[subjectOrder[index]]},
                        {"classrooms", roomsForSubject(subjectOrder[index])}
                    });
                }

                answer[name][day].push_back(entry);
            }
        }
    }

    return answer;
}

int main(int argc, char** argv) {
    setvbuf(stdout, NULL, _IONBF, 0);

    bool warnings = false;

    CLI::App app;

    int iterations = 5e7;
    app.add_option("--iterations", iterations);

    string weights = "null";
    app.add_option("--weights", weights);

    app.add_option("--input", input);
    app.add_option("--output", output);

    app.add_option("--warnings", warnings);

    app.add_option("--fair", TEACHER_FAIR, "convex teacher gap cost: + gaps^2/fair, for annealing, Kempe and LNS (0 = off)");

    int kempePercent = 20;
    int kempeWindowPercent = 50;
    int kempeSmallPercent = 20;

    app.add_option("--kempe", kempePercent, "percent of annealing moves that are Kempe-chain moves (0 = off)");
    app.add_option("--kempe-window", kempeWindowPercent, "percent of Kempe moves aimed at closing a teacher gap");
    app.add_option("--kempe-small", kempeSmallPercent, "percent of Kempe moves aimed at emptying a teacher short day (0 = off)");
    app.add_option("--kempe-size", KEMPE_MAX_UNITS, "max lessons in one Kempe chain");

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

    DATA = &data;

    SUBJECT_MULTI_DAY_THRESHOLD = JOB_WEEK_LENGHT + 1;

    for (const string& name : data.classes) {
        map<string, int> hoursPerSubject;

        for (auto& lesson : data.lessons[name]) {
            hoursPerSubject[lesson["subject"].get<string>()] += lesson["hours"].get<int>();
        }
    }

    int size = data.teachers.size() + data.classes.size() + 3;

    graph.assign(size, vector<vector<edge>>(SLOTS));

    teacherIsAllowed.assign(size, vector<char>(SLOTS, 0));
    teacherReserve.assign(size, vector<char>(SLOTS, 0));

    const int positionStep = MAX_LESSON_IN_DAY - max(0, SHIFT_CROSSING);

    if ((NUMBER_OF_SHIFTS - 1) * positionStep + MAX_LESSON_IN_DAY > 64) {
        throw runtime_error("too many shift positions for 64-bit mask");
    }

    teacherReserveMask.assign((size_t) size * JOB_WEEK_LENGHT, 0);

    locked.assign(size, vector<SubjectSet>(SLOTS));

    teacherRoom.assign(size, vector<int>(SLOTS, 0));
    teacherRoomRank.assign(size, vector<int>(SLOTS, 0));

    roomOccupant.assign(classroomNameByID.size() + 1, vector<int>(SLOTS, 0));

    bufferSubjects.assign(MAX_LESSON_IN_DAY, SubjectSet());
    bufferCovered.assign(MAX_LESSON_IN_DAY, 0);

    bufferCounter.assign(subjectNameByID.size() + 2, 0);

    bufferTeacherLengths.assign(JOB_WEEK_LENGHT, 0);
    bufferEnds.assign(JOB_WEEK_LENGHT, 0);
    bufferHards.assign(JOB_WEEK_LENGHT, 0);

    for (int index = 0; index < data.teachers.size(); index++) {
        for (int slot : data.free[index]) {
            teacherIsAllowed[index + 1][slot] = true;
        }

        for (int slot : data.reserve[index]) {
            teacherReserve[index + 1][slot] = 1;

            const int week = JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY;

            int shift = slot / week;
            int day = (slot % week) / MAX_LESSON_IN_DAY;
            int lesson = slot % MAX_LESSON_IN_DAY;

            teacherReserveMask[(size_t) (index + 1) * JOB_WEEK_LENGHT + day] |= 1ULL << (shift * positionStep + lesson);
        }
    }

    vector<Lesson> pending;

    for (auto& name : data.classes) {
        json& value = data.lessons[name];

        int cls = IDByClassName[name];

        int base = data.classShiftOffset[cls];

        for (auto lessonEntry : value) {
            vector<int> ids;

            for (auto& teacher : lessonEntry["teachers"]) {
                ids.push_back(IDByTeacherName[teacher]);
            }

            int subjectID = IDBySubjectName[lessonEntry["subject"]];

            for (int hour = 0; hour < lessonEntry["hours"]; hour++) {
                pending.push_back(Lesson{cls, base, ids, subjectID, name, (string)lessonEntry["subject"]});
            }
        }
    }

    int unplaced = 0;

    for (const Constant& constant : data.constants) {
        const string& name = classNameByID[constant.cls];
        const string& subject = subjectNameByID[constant.subjectID];

        int index = -1;

        for (int pos = 0; pos < pending.size(); pos++) {
            if (pending[pos].cls == constant.cls && pending[pos].subjectID == constant.subjectID) {
                index = pos;

                break;
            }
        }

        if (index == -1) {
            cout << "[WARNING] constant " << name << " / " << subject << " skipped, no lesson hours (or no teacher) left for this subject" << "\n";

            continue;
        }

        Lesson item = pending[index];

        if (!canPlaceLesson(constant.cls, constant.slot, constant.subjectID)) {
            cout << "[WARNING] constant " << name << " / " << subject << " skipped, slot conflicts with another constant or with the subject crossing rules" << "\n";

            continue;
        }

        bool ok = true;

        for (int teacherID : item.ids) {
            if (!teacherIsAllowed[teacherID][constant.slot] || occupied(teacherID, constant.slot)) {
                ok = false;

                break;
            }
        }

        if (!ok) {
            cout << "[WARNING] constant " << name << " / " << subject << " skipped: teacher is busy or unavailable at this slot" << "\n";

            continue;
        }

        for (int teacherID : item.ids) {
            if (findRoomForTeacher(teacherID, item.subjectID, constant.slot) == -1) {
                ok = false;

                break;
            }
        }

        if (!ok) {
            cout << "[WARNING] constant " << name << " / " << subject << " skipped: no available classroom at this slot" << "\n";

            continue;
        }

        pending.erase(pending.begin() + index);

        placeLesson(item, constant.slot);
        locked[constant.cls][constant.slot].insert(constant.subjectID);
    }

    while (!pending.empty()) {
        int best = -1;

        vector<int> bestCandidates;

        for (int index = 0; index < pending.size(); index++) {
            Lesson& item = pending[index];

            vector<int> candidates;

            for (int slot = item.base; slot < item.base + JOB_WEEK_LENGHT * MAX_LESSON_IN_DAY; slot++) {
                if (!canPlaceLesson(item.cls, slot, item.subjectID)) {
                    continue;
                }

                bool ok = true;

                for (int teacherID : item.ids) {
                    if (!teacherIsAllowed[teacherID][slot] || occupied(teacherID, slot)) {
                        ok = false;
                        break;
                    }
                }

                if (ok) {
                    for (int teacherID : item.ids) {
                        if (findRoomForTeacher(teacherID, item.subjectID, slot) == -1) {
                            ok = false;
                            break;
                        }
                    }
                }

                if (ok) {
                    candidates.push_back(slot);
                }
            }

            if (best == -1 || candidates.size() < bestCandidates.size()) {
                best = index;

                bestCandidates = candidates;
            }

            if (bestCandidates.empty()) {
                break;
            }
        }

        Lesson item = pending[best];

        pending.erase(pending.begin() + best);

        if (bestCandidates.empty()) {
            cout << "[WARNING] no common free slot for " << item.className << " / " << item.subjectName << "\n";

            unplaced++;

            continue;
        }

        int slot = bestCandidates[randint(0, bestCandidates.size() - 1)];

        placeLesson(item, slot);
    }

    if (unplaced > 0) {
        cout << "[WARNING] " << unplaced << " lesson(s) could not be placed during initial construction" << "\n";
    }

    if (warnings) {
        return 0;
    }

    double total = getClassTotal();

    for (int teacherID = 1; teacherID <= data.teachers.size(); teacherID++) {
        total += teacherCost(teacherID);
        total += Functions::classroomPriority(teacherID);
    }

    float temperature = 100;

    int equal = 0;
    int count = 0;

    roomWarnings = false;

    vector<int> involved, teachers1, teachers2, groupCandidates, emptyCandidates, savedRooms, savedRanks;
    vector<edge> moving;

    auto has = [](const vector<int>& values, int target) {
        return find(values.begin(), values.end(), target) != values.end();
    };

    for (int iteration = 0; iteration < iterations; iteration++) {
        temperature *= 0.9999999;

        if (equal == 10000 || (iteration + 1) % 1000000 == 0) {
            ostringstream stream;

            stream << (equal == 10000 ? "[EQUAL]" : "[PRINT]") << " ";
            stream << iteration + 1 << " " << temperature << " " << total << " " << equal;

            string prefix = stream.str();

            cout << prefix;

            int len = prefix.size();

            if (len < 40) {
                cout << string(40 - len, ' ');
            }

            cout << "| ";

            for (auto point : getClassPoint()) {
                cout << point << " ";
            }

            cout << "\n";
        }

        if (equal == 10000) {
            temperature = 20;

            equal = 0;
        }

        int type;

        if (kempePercent > 0 && randint(1, 100) <= kempePercent) {
            if (randint(1, 100) <= kempeSmallPercent) {
                type = 6;

            } else {
                type = randint(1, 100) <= kempeWindowPercent ? 5 : 4;
            }

        } else {
            type = randint(0, 3);
        }

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

            if (slotLocked(cls, slotA) || slotLocked(cls, slotB)) {
                continue;
            }

            vector<edge>& groupA = graph[cls][slotA];
            vector<edge>& groupB = graph[cls][slotB];

            if (groupA.empty() && groupB.empty()) {
                continue;
            }

            bool ok = true;

            for (auto& connection : groupA) {
                if (!teacherIsAllowed[connection.id][slotB]) {
                    ok = false;

                    break;
                }

                if (occupied(connection.id, slotB)) {
                    bool flag = false;

                    for (auto& other : groupB) {
                        if (other.id == connection.id) {
                            flag = true;

                            break;
                        }
                    }

                    if (!flag) {
                        ok = false;

                        break;
                    }
                }
            }

            if (!ok) {
                continue;
            }

            for (auto& connection : groupB) {
                if (!teacherIsAllowed[connection.id][slotA]) {
                    ok = false;

                    break;
                }

                if (occupied(connection.id, slotA)) {
                    bool flag = false;

                    for (auto& other : groupA) {
                        if (other.id == connection.id) {
                            flag = true;

                            break;
                        }
                    }

                    if (!flag) {
                        ok = false;

                        break;
                    }
                }
            }

            if (!ok) {
                continue;
            }

            involved.clear();

            for (auto& connection : groupA) {
                involved.push_back(connection.id);
            }

            for (auto& connection : groupB) {
                bool flag = false;

                for (auto& other : groupA) {
                    if (other.id == connection.id) {
                        flag = true;
                    }
                }

                if (flag) {
                    continue;
                }

                involved.push_back(connection.id);
            }

            if (!roomsSwappable(involved, slotA, slotB)) {
                continue;
            }

            float before = getClassTotal(cls);

            for (int teacherID : involved) {
                before += teacherCost(teacherID);
            }

            auto intraSwapper = [&]() {
                for (int teacherID : involved) {
                    swap(graph[teacherID][slotA], graph[teacherID][slotB]);
                }

                swapRoomsGroup(involved, slotA, slotB);

                swap(graph[cls][slotA], graph[cls][slotB]);
            };

            count++;

            intraSwapper();

            bool hard = false;

            if ((slotA - off) / MAX_LESSON_IN_DAY != (slotB - off) / MAX_LESSON_IN_DAY) {
                hard = classDayHasDuplicates(cls, slotA) || classDayHasDuplicates(cls, slotB);
            }

            float after = getClassTotal(cls);

            for (int teacherID : involved) {
                after += teacherCost(teacherID);
            }

            float delta = after - before;

            if (!hard && accept(delta, temperature)) {
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

            if (slotLocked(cls1, color1) || slotLocked(cls2, color2) ||
                slotLocked(cls1, color2) || slotLocked(cls2, color1)) {
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

            teachers1.clear();
            teachers2.clear();

            for (auto& connection : group1) {
                if (!has(teachers1, connection.id)) {
                    teachers1.push_back(connection.id);
                }
            }

            for (auto& connection : group2) {
                if (!has(teachers2, connection.id)) {
                    teachers2.push_back(connection.id);
                }
            }

            bool ok = true;

            for (int teacherID : teachers1) {
                if (!teacherIsAllowed[teacherID][color2]) {
                    ok = false;

                    break;
                }

                if (occupied(teacherID, color2) && !has(teachers2, teacherID)) {
                    ok = false;

                    break;
                }
            }

            if (ok == false) {
                continue;
            }

            for (int teacherID : teachers2) {
                if (!teacherIsAllowed[teacherID][color1]) {
                    ok = false;

                    break;
                }

                if (occupied(teacherID, color1) && !has(teachers1, teacherID)) {
                    ok = false;

                    break;
                }
            }

            if (ok == false) {
                continue;
            }

            involved = teachers1;

            for (int teacherID : teachers2) {
                if (!has(teachers1, teacherID)) {
                    involved.push_back(teacherID);
                }
            }

            if (!roomsSwappable(involved, color1, color2)) {
                continue;
            }

            float before = getClassTotal(cls1) + getClassTotal(cls2);

            for (int teacherID : involved) {
                before += teacherCost(teacherID);
            }

            auto swapper = [&]() {
                for (int teacherID : involved) {
                    swap(graph[teacherID][color1], graph[teacherID][color2]);
                }

                swapRoomsGroup(involved, color1, color2);

                swap(graph[cls1][color1], graph[cls1][color2]);
                swap(graph[cls2][color1], graph[cls2][color2]);
            };

            count++;

            swapper();

            bool hard = false;

            if ((color1 - off) / MAX_LESSON_IN_DAY != (color2 - off) / MAX_LESSON_IN_DAY) {
                hard = classDayHasDuplicates(cls1, color1) || classDayHasDuplicates(cls1, color2) ||  classDayHasDuplicates(cls2, color1) || classDayHasDuplicates(cls2, color2);
            }

            float after = getClassTotal(cls1) + getClassTotal(cls2);

            for (int teacherID : involved) {
                after += teacherCost(teacherID);
            }

            float delta = after - before;

            if (!hard && accept(delta, temperature)) {
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

            if (subjectLocked(cls, slotA, subjectID)) {
                continue;
            }

            involved.clear();

            for (edge& connection : graph[cls][slotA]) {
                if (connection.value == subjectID) {
                    involved.push_back(connection.id);
                }
            }

            groupCandidates.clear();
            emptyCandidates.clear();

            for (int slot = off; slot < off + week; slot++) {
                if (slot == slotA) {
                    continue;
                }

                bool slotOk = true;

                for (int teacherID : involved) {
                    if (!teacherIsAllowed[teacherID][slot] || occupied(teacherID, slot)) {
                        slotOk = false;

                        break;
                    }
                }

                if (!slotOk) {
                    continue;
                }

                if (!canPlaceLesson(cls, slot, subjectID, slotA)) {
                    continue;
                }

                if (data.classroomsEnable) {
                    for (int teacherID : involved) {
                        if (findRoomForTeacher(teacherID, subjectID, slot) == -1) {
                            slotOk = false;

                            break;
                        }
                    }
                }

                if (!slotOk) {
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

            float before = getClassTotal(cls);

            for (int teacherID : involved) {
                before += teacherCost(teacherID) + Weights::classroomPriority * teacherRoomRank[teacherID][slotA];
            }

            moving.clear();

            for (auto iterator = graph[cls][slotA].begin(); iterator != graph[cls][slotA].end(); ) {
                if (iterator->value == subjectID) {
                    moving.push_back(*iterator);

                    iterator = graph[cls][slotA].erase(iterator);

                } else {
                    iterator += 1;
                }
            }

            savedRooms.clear();
            savedRanks.clear();

            for (edge& connection : moving) {
                savedRooms.push_back(teacherRoom[connection.id][slotA]);
                savedRanks.push_back(teacherRoomRank[connection.id][slotA]);
            }

            auto applyMove = [&]() {
                for (edge& connection : moving) {
                    graph[cls][slotB].push_back(edge(connection.id, subjectID));
                    graph[connection.id][slotB] = {edge(cls, subjectID)};

                    graph[connection.id][slotA].clear();

                    releaseRoom(connection.id, slotA);
                    assignRoom(connection.id, subjectID, slotB);
                }
            };

            auto revertMove = [&]() {
                for (int index = 0; index < moving.size(); index++) {
                    edge& connection = moving[index];

                    vector<edge>& slotBEdges = graph[cls][slotB];

                    for (auto iterator = slotBEdges.begin(); iterator != slotBEdges.end(); ++iterator) {
                        if (iterator->id == connection.id && iterator->value == subjectID) {
                            slotBEdges.erase(iterator);

                            break;
                        }
                    }

                    graph[connection.id][slotB].clear();
                    graph[connection.id][slotA] = {edge(cls, subjectID)};

                    releaseRoom(connection.id, slotB);

                    int room = savedRooms[index];

                    if (room > 0) {
                        roomOccupant[room][slotA] = connection.id;

                        teacherRoom[connection.id][slotA] = room;
                        teacherRoomRank[connection.id][slotA] = savedRanks[index];
                    }
                }

                for (edge& connection : moving) {
                    graph[cls][slotA].push_back(connection);
                }
            };

            count += 1;

            applyMove();

            bool hard = false;

            if ((slotA - off) / MAX_LESSON_IN_DAY != (slotB - off) / MAX_LESSON_IN_DAY) {
                hard = classDayHasDuplicates(cls, slotA) || classDayHasDuplicates(cls, slotB);
            }

            float after = getClassTotal(cls);

            for (int teacherID : involved) {
                after += teacherCost(teacherID) + Weights::classroomPriority * teacherRoomRank[teacherID][slotB];
            }

            float delta = after - before;

            if (!hard && accept(delta, temperature)) {
                total = total - before + after;

                equal = 0;

            } else {
                revertMove();

                equal += 1;
            }
        }

        if (type == 3) {
            if (!data.classroomsEnable || data.teachers.empty()) {
                continue;
            }

            int teacherID = randint(1, data.teachers.size());
            int slot = randint(0, SLOTS - 1);

            int room = teacherRoom[teacherID][slot];

            if (room == 0 || graph[teacherID][slot].empty()) {
                continue;
            }

            int subjectID = graph[teacherID][slot][0].value;
            int rank = teacherRoomRank[teacherID][slot];

            float before = Weights::classroomPriority * rank;

            releaseRoom(teacherID, slot);
            assignRoom(teacherID, subjectID, slot);

            count++;

            if (teacherRoom[teacherID][slot] == 0) {
                roomOccupant[room][slot] = teacherID;

                teacherRoom[teacherID][slot] = room;
                teacherRoomRank[teacherID][slot] = rank;

                equal += 1;

                continue;
            }

            float after = Weights::classroomPriority * teacherRoomRank[teacherID][slot];

            float delta = after - before;

            if (delta <= 0) {
                total = total - before + after;

                equal = (delta < 0) ? 0 : equal + 1;

            } else {
                releaseRoom(teacherID, slot);

                roomOccupant[room][slot] = teacherID;

                teacherRoom[teacherID][slot] = room;
                teacherRoomRank[teacherID][slot] = rank;

                equal += 1;
            }
        }

        if (type >= 4) {
            int shift = randint(0, NUMBER_OF_SHIFTS - 1);

            if (data.classesByShift[shift].empty()) {
                continue;
            }

            KempeStart kempeStart;

            bool found = false;

            if (type == 4) {
                found = kempePickRandom(shift, kempeStart);

            } else {
                int attempts = (type == 6) ? 40 : 30;

                for (int attempt = 0; attempt < attempts && !found; attempt++) {
                    found = kempePickTeacher(type - 4, randint(1, data.teachers.size()), shift, kempeStart);
                }
            }

            if (!found) {
                continue;
            }

            kempeMove(kempeStart.A, kempeStart.B, kempeStart.cls, kempeStart.subject, type - 4, temperature, total, equal, count);
        }
    }

    std::ofstream file(output);

    file << std::setw(4) << save() << std::endl;
    file.close();

    cout << count << " " << total << endl;

    return 0;
}
