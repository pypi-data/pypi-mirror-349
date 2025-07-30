
#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
#include <ctime>
#include <map>
#include <vector>
#include <algorithm>
#include "load_inst.hpp"
#include "utility.hpp"
#include "build_mdd.hpp"
#include "freq_miner.hpp"

namespace btminer {

using namespace std;

extern int num_nodes, cur_node;

map<string, int> item_map;
map<int, string> item_map_rev;
vector<int> freq;
vector<int> item_dic;

void Load_items_pre(string& inst_name);
bool Load_items(string& inst_name);
bool Preprocess(string& inst, double thresh);

bool Load_instance(string& items_file, double thresh) {
    clock_t kk = clock();
    Tree.emplace_back(0, 0, 0);

    if (pre_pro) {
        if (!Preprocess(items_file, thresh))
            return false;

        cout << "\nPreprocess done in " << give_time(clock() - kk) << " seconds\n\n";

        DFS.reserve(L);
        for (int i = 0; i < L; ++i)
            DFS.emplace_back(-i - 1);

        kk = clock();
        Load_items_pre(items_file);
    } else if (!Load_items(items_file))
        return false;
    else {
        theta = (thresh < 1) ? ceil(thresh * N * N_mult) : thresh;
    }

    cout << "\nMDD Database built in " << give_time(clock() - kk) << " seconds\n\n";
    cout << "Found " << N * N_mult << " sequence, with max line len " << M << ", and " << L << " items, and " << E << " enteries\n";
    cout << "Total MDD nodes: " << Tree.size() << endl;

    return true;
}

bool Preprocess(string& inst, double thresh) {
    ifstream file(inst);
    if (!file.good()) {
        cout << "!!!!!! No such file exists: " << inst << " !!!!!!\n";
        return false;
    }

    string line;
    int size_m, ditem;
    while (getline(file, line) && give_time(clock() - start_time) < time_limit) {
        ++N;
        vector<bool> counted(L, 0);
        istringstream word(line);
        string itm;
        while (word >> itm) {
            ditem = stoi(itm);
            if (L < abs(ditem)) L = abs(ditem);
            while (freq.size() < L) {
                freq.push_back(0);
                counted.push_back(0);
            }
            if (!counted[abs(ditem) - 1]) {
                ++freq[abs(ditem) - 1];
                counted[abs(ditem) - 1] = 1;
            }
        }
    }

    theta = (thresh < 1) ? ceil(thresh * N * N_mult) : thresh;

    int real_L = 0;
    item_dic = vector<int>(L, -1);
    for (int i = 0; i < L; ++i) {
        if (freq[i] >= theta)
            item_dic[i] = ++real_L;
    }

    cout << "Original number of items: " << L << " Reduced to: " << real_L << endl;
    L = real_L;
    N = 0;
    return true;
}

void Load_items_pre(string& inst_name) {
    ifstream file(inst_name);
    if (!file.good()) return;

    string line;
    int ditem;
    while (getline(file, line) && give_time(clock() - start_time) < time_limit) {
        istringstream word(line);
        string itm;
        vector<int> temp_vec;
        bool sgn = 0;
        while (word >> itm) {
            if (use_dic) {
                auto it = item_map.find(itm);
                if (it == item_map.end()) {
                    item_map[itm] = ++L;
                    item_map_rev[L] = itm;
                    ditem = L;
                } else {
                    ditem = it->second;
                }
            } else {
                ditem = stoi(itm);
            }

            if (pre_pro && freq.size() > abs(ditem) - 1 && freq[abs(ditem) - 1] < theta) {
                if (!sgn)
                    sgn = ditem < 0;
                continue;
            } else if (pre_pro) {
                ditem = (ditem > 0) ? item_dic[ditem - 1] : -item_dic[-ditem - 1];
            }

            if (sgn && ditem > 0)
                ditem = -ditem;
            sgn = 0;

            temp_vec.push_back(ditem);
        }

        if (temp_vec.empty()) continue;

        ++N;
        if (temp_vec.size() > M) M = temp_vec.size();

        E += temp_vec.size();  // <-- make sure E gets incremented
        Build_MDD(temp_vec);
    }
}

bool Load_items(string& inst_name) {
    ifstream file(inst_name);
    if (!file.good()) {
        cout << "!!!!!! No such file exists: " << inst_name << " !!!!!!\n";
        return false;
    }

    string line;
    int ditem;
    while (getline(file, line) && give_time(clock() - start_time) < time_limit) {
        ++N;
        istringstream word(line);
        string itm;
        vector<int> temp_vec;
        while (word >> itm) {
            if (use_dic) {
                auto it = item_map.find(itm);
                if (it == item_map.end()) {
                    item_map[itm] = ++L;
                    item_map_rev[L] = itm;
                    ditem = L;
                } else {
                    ditem = it->second;
                }
            } else {
                ditem = stoi(itm);
                if (L < abs(ditem)) {
                    L = abs(ditem);
                    while (DFS.size() < L && !just_build) {
                        DFS.reserve(L);
                        DFS.emplace_back(-DFS.size() - 1);
                    }
                }
            }
            temp_vec.push_back(ditem);
        }

        if (temp_vec.size() > M) M = temp_vec.size();
        E += temp_vec.size();  // <-- make sure E gets incremented
        Build_MDD(temp_vec);
    }
    return true;
}

} // namespace btminer
