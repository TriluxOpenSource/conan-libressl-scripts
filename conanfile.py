from conans import ConanFile, CMake, tools
import os

class LibreSSLConan(ConanFile):
    name = "libressl"
    author = "Ralph-Gordon Paul (gordon@rgpaul.com)"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "android_ndk": "ANY", "android_stl_type":["c++_static", "c++_shared"]}
    default_options = "shared=False", "android_ndk=None", "android_stl_type=c++_static"
    description = "LibreSSL is a version of the TLS/crypto stack forked from OpenSSL in 2014, with goals of modernizing the codebase, improving security, and applying best practice development processes."
    url = "https://github.com/RGPaul/conan-libressl-scripts"
    license = "ISC"
    exports_sources = "cmake-modules/*", "ios/*"

    # download sources
    def source(self):
        url = "https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-%s.tar.gz" % self.version
        tools.get(url)

    # compile using cmake
    def build(self):
        cmake = CMake(self)
        library_folder = "%s/libressl-%s" % (self.source_folder, self.version)
        cmake.verbose = True

        if self.settings.os == "Android":
            self.applyCmakeSettingsForAndroid(cmake)

        if self.settings.os == "iOS":
            self.applyCmakeSettingsForiOS(cmake)

        if self.settings.os == "Macos":
            self.applyCmakeSettingsFormacOS(cmake)

        if self.settings.os == "Windows":
            self.applyCmakeSettingsForWindows(cmake)

        cmake.configure(source_folder=library_folder)
        cmake.build()
        cmake.install()

    def applyCmakeSettingsForAndroid(self, cmake):
        android_toolchain = os.environ["ANDROID_NDK_PATH"] + "/build/cmake/android.toolchain.cmake"
        cmake.definitions["CMAKE_SYSTEM_NAME"] = "Android"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = android_toolchain
        cmake.definitions["ANDROID_NDK"] = os.environ["ANDROID_NDK_PATH"]
        cmake.definitions["ANDROID_ABI"] = tools.to_android_abi(self.settings.arch)
        cmake.definitions["ANDROID_STL"] = self.options.android_stl_type
        cmake.definitions["ANDROID_NATIVE_API_LEVEL"] = self.settings.os.api_level
        cmake.definitions["ANDROID_TOOLCHAIN"] = "clang"
        cmake.definitions["LIBRESSL_APPS"] = "OFF"
        cmake.definitions["LIBRESSL_TESTS"] = "OFF"

    def applyCmakeSettingsForiOS(self, cmake):
        ios_toolchain = "cmake-modules/Toolchains/ios.toolchain.cmake"
        cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = ios_toolchain
        cmake.definitions["DEPLOYMENT_TARGET"] = "10.0"
        
        tools.replace_in_file("%s/libressl-%s/CMakeLists.txt" % (self.source_folder, self.version),
                    "project (LibreSSL C ASM)",
                    """project (LibreSSL C ASM)
                    include_directories(BEFORE "../ios/include") """)

        # on iOS SDK 13+ we have to remove some checks
        if tools.Version(self.settings.os.version) >= 13.0:
            tools.replace_in_file("%s/libressl-%s/CMakeLists.txt" % (self.source_folder, self.version),
                        "check_function_exists(reallocarray", "#check_function_exists(reallocarray")

            tools.replace_in_file("%s/libressl-%s/CMakeLists.txt" % (self.source_folder, self.version),
                        "check_function_exists(explicit_bzero", "#check_function_exists(explicit_bzero")

            tools.replace_in_file("%s/libressl-%s/CMakeLists.txt" % (self.source_folder, self.version),
                        "check_function_exists(syslog_r", "#check_function_exists(syslog_r")

            tools.replace_in_file("%s/libressl-%s/CMakeLists.txt" % (self.source_folder, self.version),
                        "check_function_exists(timingsafe_memcmp", "#check_function_exists(timingsafe_memcmp")

        cmake.definitions["LIBRESSL_APPS"] = "OFF"
        cmake.definitions["LIBRESSL_TESTS"] = "OFF"

        if self.settings.arch == "x86":
            cmake.definitions["PLATFORM"] = "SIMULATOR"
            cmake.definitions["ENABLE_ASM"] = "OFF"
        elif self.settings.arch == "x86_64":
            cmake.definitions["PLATFORM"] = "SIMULATOR64"
            cmake.definitions["ENABLE_ASM"] = "OFF"
        else:
            cmake.definitions["PLATFORM"] = "OS"

        # define all architectures for ios fat library
        if "arm" in self.settings.arch:
            cmake.definitions["ARCHS"] = "armv7;armv7s;arm64;arm64e"
        else:
            cmake.definitions["ARCHS"] = tools.to_apple_arch(self.settings.arch)
    
    def applyCmakeSettingsFormacOS(self, cmake):
        cmake.definitions["CMAKE_OSX_ARCHITECTURES"] = tools.to_apple_arch(self.settings.arch)

    def applyCmakeSettingsForWindows(self, cmake):
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        if self.settings.compiler == "Visual Studio":
            # check that runtime flags and build_type correspond (consistency check)
            if "d" not in self.settings.compiler.runtime and self.settings.build_type == "Debug":
                raise Exception("Compiling for Debug mode but compiler runtime does not contain 'd' flag.")

            if self.settings.build_type == "Debug":
                cmake.definitions["CMAKE_CXX_FLAGS_DEBUG"] = "/%s" % self.settings.compiler.runtime
            elif self.settings.build_type == "Release":
                cmake.definitions["CMAKE_CXX_FLAGS_RELEASE"] = "/%s" % self.settings.compiler.runtime

    def package(self):
        self.copy("*", dst="include", src='include')
        self.copy("*.lib", dst="lib", src='lib', keep_path=False)
        self.copy("*.dll", dst="bin", src='bin', keep_path=False)
        self.copy("*.so", dst="lib", src='lib', keep_path=False)
        self.copy("*.dylib", dst="lib", src='lib', keep_path=False)
        self.copy("*.a", dst="lib", src='lib', keep_path=False)
        
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ['include']

    def package_id(self):
        if "arm" in self.settings.arch and self.settings.os == "iOS":
            self.info.settings.arch = "AnyARM"

    def config_options(self):
        # remove android specific option for all other platforms
        if self.settings.os != "Android":
            del self.options.android_ndk
            del self.options.android_stl_type
