# Conan LibreSSL

![Android status](https://github.com/rgpaul/conan-libressl-scripts/workflows/Android/badge.svg)
![iOS status](https://github.com/rgpaul/conan-libressl-scripts/workflows/iOS/badge.svg)
![Linux status](https://github.com/rgpaul/conan-libressl-scripts/workflows/Linux/badge.svg)
![macOS status](https://github.com/rgpaul/conan-libressl-scripts/workflows/macOS/badge.svg)
![Windows status](https://github.com/rgpaul/conan-libressl-scripts/workflows/Windows/badge.svg)

This repository contains a conan receipe that can be used to build LibreSSL packages.

For Infos about LibreSSL please visit [libressl.org](https://www.libressl.org/).  
The library is licensed under the [ISC License](https://tldrlegal.com/license/-isc-license).  
This repository is licensed under the [MIT License](LICENSE).

## Android

The environmental `ANDROID_NDK_PATH` must be set to the path of the android ndk.

To create a package for Android you can run the conan command like this:

```
export ANDROID_NDK_PATH='/opt/android-ndks/android-ndk-r20'
conan create . libressl/2.9.2@rgpaul/stable -s os=Android -s os.api_level=21 -s compiler=clang -s compiler.version=8.0 -s compiler.libcxx=libc++ -s arch=x86_64 -s build_type=Release -o android_ndk=r20 -o android_stl_type=c++_static
```

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Android NDK](https://developer.android.com/ndk/downloads/)

## iOS

To create a package for iOS you can run the conan command like this:

```
conan create . libressl/2.9.2@rgpaul/stable -s os=iOS -s os.version=13.0 -s arch=armv8 -s build_type=Release -o shared=False
```

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Xcode](https://developer.apple.com/xcode/)

## Linux - Debian

To create a package for Linux you can run the conan command like this:

```
conan create . libressl/2.9.2@rgpaul/stable -s os=Linux -s arch=x86_64 -s build_type=Release -o shared=False
```

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* build-essential, make, curl, git, unzip and zip (`apt-get install build-essential cmake curl git unzip zip`)

## macOS

To create a package for macOS you can run the conan command like this:

```
conan create . libressl/2.9.2@rgpaul/stable -s os=Macos -s os.version=10.15 -s arch=x86_64 -s build_type=Release -o shared=False
```

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Xcode](https://developer.apple.com/xcode/)

## Windows 10

To create a package for Windows 10 you can run the conan command like this:

```
conan create . libressl/2.9.2@rgpaul/stable -s os=Windows -s compiler="Visual Studio" -s compiler.runtime=MT -s arch=x86_64 -s build_type=Release -o shared=False
```

### Requirements

* [CMake](https://cmake.org/)
* [Conan](https://conan.io/)
* [Visual Studio 2017](https://visualstudio.microsoft.com/de/downloads/)