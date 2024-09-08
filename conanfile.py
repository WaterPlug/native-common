from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import patch, copy
from os.path import join
import re

required_conan_version = ">=2.7.0"

class NativeLibs(ConanFile):
    name = "native_libs"
    license = "Apache-2.0"
    author = "WaterPlug"
    url = "https://github.com/WaterPlug/native-common"
    vcs_url = "https://github.com/WaterPlug/native-common.git"
    description = "Common library for C++ opensource projects"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    patch_files = []
    exports_sources = patch_files

    def requirements(self):
        self.requires("boost/1.84.0", transitive_headers=True)


    def build_requirements(self):
        self.test_requires("gtest/1.15.0")

    def configure(self):
        self.options["gtest"].build_gmock = False

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        self.run(f"git init . && git remote add origin {self.vcs_url} && git fetch")
        if re.match(r'\d+\.\d+\.\d+', self.version) is not None:
            version_hash = self.conan_data["commit_hash"][self.version]["hash"]
            self.run("git checkout -f %s" % version_hash)
        else:
            self.run("git checkout -f %s" % self.version)
        for p in self.patch_files:
            patch(self, patch_file=p)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        MODULES = ["common"]
        for m in MODULES:
            copy(self, "*.h", src=join(self.source_folder, "%s/include" % m), dst=join(self.package_folder, "include"), keep_path=True)
        copy(self, "*.lib", src=self.build_folder, dst=join(self.package_folder, "lib"), keep_path=False)
        copy(self, "*.a", src=self.build_folder, dst=join(self.package_folder, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "native_libs"
        self.cpp_info.name = "native_libs"
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libs = ["wp_common"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.requires = [
            "boost::boost"
        ]
        if self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ws2_32", "wsock32"]
        self.cpp_info.defines.append("FMT_EXCEPTIONS=0")
