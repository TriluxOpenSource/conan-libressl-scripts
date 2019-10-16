#!/usr/bin/env bash
set -e

export IOS_SDK_VERSION=$(xcodebuild -showsdks | grep iphoneos | awk '{print $4}' | sed 's/[^0-9,\.]*//g');
echo "iOS SDK ${IOS_SDK_VERSION}";
      
conan create . libressl/${LIBRARY_VERSION}@${CONAN_USER}/${CONAN_CHANNEL} -s os=iOS -s os.version=${IOS_SDK_VERSION} -s arch=armv8 -s build_type=Release -o shared=False;
conan create . libressl/${LIBRARY_VERSION}@${CONAN_USER}/${CONAN_CHANNEL} -s os=iOS -s os.version=${IOS_SDK_VERSION} -s arch=armv8 -s build_type=Debug -o shared=False;
conan create . libressl/${LIBRARY_VERSION}@${CONAN_USER}/${CONAN_CHANNEL} -s os=iOS -s os.version=${IOS_SDK_VERSION} -s arch=x86_64 -s build_type=Debug -o shared=False;
