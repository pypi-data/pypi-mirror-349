#include "utility.hpp"
#include "build_mdd.hpp"
#include "load_inst.hpp"
#include <iostream>

namespace btminer {

// === Global Variables ===
bool use_dic = false; 
std::vector<std::vector<int>> items;
bool use_list = false;
bool just_build = false;
int E = 0, M = 0, N = 0, L = 0, theta = 0;
std::vector<Pattern> DFS;
clock_t start_time;
bool b_disp = false, b_write = false;
std::string out_file;

bool pre_pro = true;
int N_mult = 1, M_mult = 1;
int time_limit = 30 * 3600;

// === Function Definitions ===

int find_ID(std::vector<int>& vec, int itm) {
    int plc = 0;
    while (plc < vec.size() && vec[plc] != itm)
        ++plc;
    return (plc == vec.size()) ? -1 : plc;
}

bool check_parent(int cur_arc, int str_pnt, int start, std::vector<int>& strpnt_vec) {
    std::vector<int> ancestors;
    int cur_anct = Tree[cur_arc].anct;

    while (Tree[cur_anct].itmset > Tree[str_pnt].itmset) {
        if (Tree[cur_anct].item > 0)
            ancestors.push_back(cur_anct);
        cur_anct = Tree[cur_anct].anct;
    }

    if (Tree[cur_anct].itmset == Tree[str_pnt].itmset)
        return true;

    for (auto it = ancestors.rbegin(); it != ancestors.rend(); ++it) {
        for (int i = start; i < strpnt_vec.size(); ++i) {
            if (strpnt_vec[i] == *it)
                return true;
        }
    }

    return false;
}

bool find_pnt(Arc* pnt, std::vector<Arc*>& vec, int pos) {
    for (size_t i = pos; i < vec.size(); ++i) {
        if (vec[i] == pnt)
            return true;
    }
    return false;
}

float give_time(clock_t kk) {
    return static_cast<float>(kk) / CLOCKS_PER_SEC;
}

} // namespace btminer
