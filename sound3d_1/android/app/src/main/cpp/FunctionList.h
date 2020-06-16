//
// Created by facun on 10/06/2020.
//

#ifndef ANDROID_FUNCTIONLIST_H
#define ANDROID_FUNCTIONLIST_H

#include <vector>
#include <functional>
#include <array>

template<class iter_type>
class FunctionList {
    std::vector<std::pair<std::function<void(iter_type, iter_type)>, bool>> functionList;
    bool muted = false;
public:
    FunctionList() = default;

    FunctionList(const FunctionList &) = delete;

    FunctionList &operator=(const FunctionList &) = delete;


    void operator()(iter_type begin, iter_type end) {
        for (auto &f : functionList) {
            if (f.second == true) std::get<0>(f)(begin, end);
        }
        if (muted) std::fill(begin, end, 0);
    }

    void addEffect(std::function<void(iter_type, iter_type)> f) {
        functionList.emplace_back(std::move(f), true);
    }

    void removeEffectAt(unsigned int index) {
        if (index < functionList.size()) {
            functionList.erase(std::next(functionList.begin(), index));
        }
    }

    void rotateEffectAt(unsigned int from, unsigned int to) {
        auto &v = functionList;
        if (from >= v.size() || to >= v.size()) return;
        if (from <= to) {
            std::rotate(v.begin() + from, v.begin() + from + 1, v.begin() + to + 1);
        } else {
            from = v.size() - 1 - from;
            to = v.size() - 1 - to;
            std::rotate(v.rbegin() + from, v.rbegin() + from + 1, v.rbegin() + to + 1);
        }
    }

    void modifyEffectAt(size_t index, std::function<void(iter_type, iter_type)> fun) {
        functionList[index] = {std::move(fun), functionList[index].second};
    }

    void enableEffectAt(size_t index, bool enable) {
        functionList[index].second = enable;
    }

    void mute(bool toMute) {
        muted = toMute;
    }

    auto getType() {
        return iter_type();
    }

};

#endif //ANDROID_FUNCTIONLIST_H
