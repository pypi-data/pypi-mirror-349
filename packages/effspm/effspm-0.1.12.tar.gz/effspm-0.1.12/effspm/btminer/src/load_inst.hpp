#pragma once

#include <vector>
#include <string>
#include <fstream>
#include <map>
#include <unordered_set>
#include <unordered_map>
#include <ctime>

namespace btminer {

bool Load_instance(std::string& items_file, double thresh);

extern std::string out_file, folder;

extern bool b_disp, b_write, use_dic, just_build, pre_pro;

extern int N, M, L, theta, num_nodes, M_mult, N_mult, time_limit, cur_node;

extern clock_t start_time;

} // namespace btminer
