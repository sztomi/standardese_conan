from conans import ConanFile, CMake
from conans.tools import download, untargz

from glob import glob
import os
import shutil


class Standardese(ConanFile):
    settings = 'os', 'compiler', 'build_type', 'arch'
    name = 'standardese'
    url = 'https://github.com/sztomi/standardese_conan'
    repo_url = 'https://github.com/foonathan/standardese.git'
    license = 'MIT'
    version = '0.3-1'
    requires = 'Boost/1.60.0@lasote/stable'
    generators = 'cmake'

    @property
    def sourcedir(self):
        return os.path.join(os.getcwd(), self.name)

    def source(self):
        self.run('git clone --branch v{} {} --depth 1'
                     .format(self.version, self.repo_url))

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake {}'.format(self.sourcedir))
        self.run('cmake {} {} -DSTANDARDESE_BUILD_TEST=OFF -DCMAKE_INSTALL_PREFIX={}'
                    .format(self.conanfile_directory,
                            cmake.command_line,
                            self.package_folder))
        self.run('make -j4')
        self.run('cmake --build . --target install')

    def package(self):
        # the install target is a bit imperfect in this version
        # so we fix it here and there
        self.copy('*.hpp', dst='include/standardese', src='comp.generated', keep_path=False)
        shutil.rmtree(os.path.join(self.package_folder, 'lib', 'standardese'))
        self.copy('*.a', dst='lib', keep_path=False)
        self.copy('*.so', dst='lib', keep_path=False)
        self.copy('*.lib', dst='lib', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [
                self.name, 'cmark', 'clang',
                'boost_system', 'boost_filesystem'
        ]

        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('pthread')
