#pragma once
#include <string>

class _3DTIMobile {
public:
    static char * getTemplateInfo();
    _3DTIMobile();
    ~_3DTIMobile();

    std::string message();
};


std::string message_simple();