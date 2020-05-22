#include "_3DTIMobile.h"

#define PLATFORM_ANDROID 0
#define PLATFORM_IOS 1

char * _3DTIMobile::getTemplateInfo()
{
#if PLATFORM == PLATFORM_IOS
	static char info[] = "Platform for iOS";
#elif PLATFORM == PLATFORM_ANDROID
	static char info[] = "Platform for Android";
#else
	static char info[] = "Undefined platform";
#endif

	return info;
}

_3DTIMobile::_3DTIMobile()
{
}

_3DTIMobile::~_3DTIMobile()
{
}

std::string _3DTIMobile::message()
{
	return "This message was created by a C++ library";
}

std::string message_simple()
{
	return "This message was created by a C++ library";
}
