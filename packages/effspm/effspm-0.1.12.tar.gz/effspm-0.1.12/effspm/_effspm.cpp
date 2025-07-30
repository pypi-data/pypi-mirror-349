#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// PrefixProjection headers
#include "freq_miner.hpp"
#include "load_inst.hpp"
#include "utility.hpp"

// BTMiner (wrapped in its own namespace in source files)
#include "btminer/src/freq_miner.hpp"
#include "btminer/src/load_inst.hpp"
#include "btminer/src/utility.hpp"
#include "btminer/src/build_mdd.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_effspm, m) {
    m.doc() = "Unified SPM library: PrefixProjection, BTMiner, and more";

    // PrefixProjection
    m.def("PrefixProjection",
        [](py::object data,
           double minsup,
           unsigned int time_limit,
           bool preproc,
           bool use_dic,
           bool verbose,
           const std::string &out_file)
        {
            ::time_limit = time_limit;
            ::pre_pro    = preproc;
            ::use_dic    = use_dic;
            ::use_list   = false;
            ::b_disp     = verbose;
            ::b_write    = !out_file.empty();
            ::out_file   = out_file;

            ClearCollected();
            start_time = std::clock();

            if (py::isinstance<py::str>(data)) {
                std::string path = data.cast<std::string>();
                if (!Load_instance(path, minsup))
                    throw std::runtime_error("Failed to load file: " + path);
            } else {
                auto seqs = data.cast<std::vector<std::vector<int>>>();
                items = std::move(seqs);
                N = items.size();

                int max_id = 0;
                for (auto &seq : items)
                    for (int x : seq)
                        max_id = std::max(max_id, std::abs(x));
                L = max_id;

                theta = (minsup < 1.0) ? std::ceil(minsup * N) : minsup;

                DFS.clear();
                DFS.reserve(L);
                for (unsigned int i = 0; i < L; ++i)
                    DFS.emplace_back(-static_cast<int>(i) - 1);

                M = 0;
                E = 0;
                for (auto &seq : items) {
                    M = std::max<unsigned int>(M, seq.size());
                    E += seq.size();
                }
            }

            Freq_miner();

            py::dict out;
            out["patterns"] = GetCollected();
            out["time"]     = give_time(std::clock() - start_time);
            return out;
        },
        py::arg("data"),
        py::arg("minsup") = 0.01,
        py::arg("time_limit") = 36000,
        py::arg("preproc") = false,
        py::arg("use_dic") = false,
        py::arg("verbose") = false,
        py::arg("out_file") = ""
    );

    // BTMiner
    m.def("BTMiner",
        [](py::object data,
           double minsup,
           unsigned int time_limit,
           bool preproc,
           bool use_dic,
           bool verbose,
           const std::string &out_file)
        {
            btminer::time_limit = time_limit;
            btminer::pre_pro    = preproc;
            btminer::use_dic    = use_dic;
            btminer::use_list   = false;
            btminer::b_disp     = verbose;
            btminer::b_write    = !out_file.empty();
            btminer::out_file   = out_file;

            btminer::ClearCollected();
            btminer::start_time = std::clock();

            if (py::isinstance<py::str>(data)) {
                std::string path = data.cast<std::string>();
                if (!btminer::Load_instance(path, minsup))
                    throw std::runtime_error("Failed to load file: " + path);
            } else {
                auto seqs = data.cast<std::vector<std::vector<int>>>();
                btminer::items = std::move(seqs);
                btminer::N = btminer::items.size();

                int max_id = 0;
                for (auto &seq : btminer::items)
                    for (int x : seq)
                        max_id = std::max(max_id, std::abs(x));
                btminer::L = max_id;

                btminer::theta = (minsup < 1.0) ? std::ceil(minsup * btminer::N) : minsup;

                btminer::DFS.clear();
                btminer::DFS.reserve(btminer::L);
                for (unsigned int i = 0; i < btminer::L; ++i)
                    btminer::DFS.emplace_back(-static_cast<int>(i) - 1);

                btminer::M = 0;
                btminer::E = 0;
                for (auto &seq : btminer::items) {
                    btminer::M = std::max<unsigned int>(btminer::M, seq.size());
                    btminer::E += seq.size();
                }
            }

            btminer::Freq_miner();

            py::dict out;
            out["patterns"] = btminer::GetCollected();
            out["time"]     = btminer::give_time(std::clock() - btminer::start_time);
            return out;
        },
        py::arg("data"),
        py::arg("minsup") = 0.01,
        py::arg("time_limit") = 36000,
        py::arg("preproc") = false,
        py::arg("use_dic") = false,
        py::arg("verbose") = false,
        py::arg("out_file") = ""
    );
}
