"""A NT based system specialized environment class."""

from base_environment import BaseEnvironment

import os
import platform

import tools

class NtEnvironment(BaseEnvironment):
    """An environment class."""

    def __init__(
        self,
        _platform=None,
        _tools=None,
        toolpath=None,
        variables=None,
        parse_flags=None,
        **kw
    ):
        """Create a new NtEnvironment instance."""

        BaseEnvironment.__init__(
            self,
            _platform,
            _tools,
            toolpath,
            variables,
            parse_flags,
            **kw
        )

        if self.toolset == 'mingw':
            self['CXXFLAGS'].append('-Wall')
            self['CXXFLAGS'].append('-Wextra')
            self['CXXFLAGS'].append('-Werror')
            self['CXXFLAGS'].append('-pedantic')
            self['CXXFLAGS'].append('-Wshadow')
            self['CXXFLAGS'].append('-Wno-long-long')
            self['CXXFLAGS'].append('-Wno-uninitialized')

            if self.arch != platform.machine():
                if tools.is_32_bits_architecture(self.arch):
                    self['CXXFLAGS'].append('-m32')
                    self['LINKFLAGS'].append('-m32')
                elif tools.is_64_bits_architecture(self.arch):
                    self['CXXFLAGS'].append('-m64')
                    self['LINKFLAGS'].append('-m64')
        else:
            self['CXXFLAGS'].append('/O2')
            self['CXXFLAGS'].append('/EHsc')

        self['ARGUMENTS'].setdefault('prefix', r'C:\mingw')

    def FreelanLibrary(self, target_dir, name, major, minor, source_files, **env):
        """Build a library."""

        for key, value in env.items():
            if isinstance(value, list):
                if key in self:
                    env[key] += self[key]

        objects = self.Object(source = source_files, **env)
        shared_library = self.SharedLibrary(os.path.join(target_dir, name), objects, **env)
        static_library = self.StaticLibrary(os.path.join(target_dir, name + '_static'), objects, **env)

        return static_library + shared_library
