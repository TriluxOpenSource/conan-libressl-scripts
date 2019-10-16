#!/usr/bin/env bash

declare ABSOLUTE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Install conan (windows)
if [[ "$GITHUB_OS_NAME" == "windows" ]]; then
    choco install python3;
    choco install conan;

# Install conan (linux)
elif [[ "$GITHUB_OS_NAME" == "linux" ]]; then
    pip install conan --user;

# Install conan (macos)
elif [[ "$GITHUB_OS_NAME" == "macos" ]]; then
    pip3 install conan;
fi

# Add conan repository and apply conan config
conan remote add ${CONAN_REPOSITORY_NAME} ${CONAN_REPOSITORY}
conan config install ${ABSOLUTE_DIR}/conan/config.zip

# login to conan
conan user -p "${BINTRAY_KEY}" -r ${CONAN_REPOSITORY_NAME} ${BINTRAY_USER}
