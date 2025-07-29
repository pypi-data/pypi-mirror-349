#pragma once

#include <vector>
#include "load_inst.hpp"
#include "build_mdd.hpp"

namespace btminer {

void Freq_miner();

class Pattern {
public:
    std::vector<int> seq;
    std::vector<int> str_pnt;
    std::vector<int> slist;
    std::vector<int> ilist;
    int freq;

    Pattern(std::vector<int>& _seq, int item) {
        seq.swap(_seq);
        seq.push_back(item);
        freq = 0;
    }

    Pattern(int item) {
        seq.push_back(item);
        freq = 0;
    }

    Pattern() {
        freq = 0;
    }
};

extern int num_patt;
extern int num_max_patt;
extern std::vector<Pattern> DFS;

} // namespace btminer
