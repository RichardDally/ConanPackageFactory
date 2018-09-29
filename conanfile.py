from conans import ConanFile, CMake, tools


class SFMLPackage(ConanFile):
    name = 'SFML'
    version = '2.5.0'
    license = 'zlib/png license'
    url = 'https://github.com/SFML/SFML'
    description = 'Simple and Fast Multimedia Library'
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'

    def source(self):
        self.run('git clone https://github.com/SFML/SFML')
        self.run('cd SFML && git checkout {}'.format(self.version))
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("SFML/CMakeLists.txt", "project(SFML)",
                              '''project(SFML)
                              include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
                              conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder='SFML')
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

