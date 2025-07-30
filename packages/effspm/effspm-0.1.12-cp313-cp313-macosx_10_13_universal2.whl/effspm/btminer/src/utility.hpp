#pragma once

#include <vector>
#include <ctime>
#include <string>
#include "build_mdd.hpp"
#include "freq_miner.hpp"
#include "load_inst.hpp"

namespace btminer {

// === Utility function declarations ===
bool find_pnt(Arc* pnt, std::vector<Arc*>& vec, int pos);
int find_ID(std::vector<int>& vec, int itm);
float give_time(clock_t kk);
bool check_parent(int cur_arc, int str_pnt, int start, std::vector<int>& strpnt_vec);

// === Global variables (DECLARATIONS ONLY) ===
extern std::vector<std::vector<int>> items;
extern bool use_list;
extern bool just_build;
extern int E, M, N, L, theta;
extern std::vector<Pattern> DFS;
extern clock_t start_time;
extern bool b_disp, b_write;
extern std::string out_file;
extern bool pre_pro;
extern int N_mult, M_mult;
extern int time_limit;

// === Python-friendly accessors ===
inline void ClearCollected() {
    DFS.clear();
}

inline std::vector<std::vector<int>> GetCollected() {
    std::vector<std::vector<int>> patterns;
    for (const auto& p : DFS) {
        patterns.push_back(p.seq);
    }
    return patterns;
}

} // namespace btminer
