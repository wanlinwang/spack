# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


@IntelOneApiPackage.update_description
class IntelOneapiCompilersClassic(Package):
    """Relies on intel-oneapi-compilers to install the compilers, and
    configures modules for icc/icpc/ifort.

    """

    maintainers = ['rscohn2']

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    has_code = False

    phases = []

    # Versions before 2021 are in the `intel` package
    # intel-oneapi versions before 2022 use intel@19.0.4
    for ver, oneapi_ver in {
        '2021.6.0': '2022.2.0',
        '2021.5.0': '2022.1.0',
    }.items():
        version(ver)
        depends_on('intel-oneapi-compilers@' + oneapi_ver, when='@' + ver, type='run')

    @property
    def oneapi_compiler_prefix(self):
        oneapi_version = self.spec['intel-oneapi-compilers'].version
        return self.spec['intel-oneapi-compilers'].prefix.compiler.join(
            '%s' % oneapi_version).linux

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        env.set('CC', join_path(self.oneapi_compiler_prefix.bin, 'icc'))
        env.set('CXX', join_path(self.oneapi_compiler_prefix.bin, 'icpc'))
        env.set('F77', join_path(self.oneapi_compiler_prefix.bin, 'ifort'))
        env.set('FC', join_path(self.oneapi_compiler_prefix.bin, 'ifort'))

    def install(self, spec, prefix):
        # We create a physical directory for binaries because they are more likely
        # to be affected by being symlinked
        mkdirp(prefix.bin)
        for entry in os.listdir(self.oneapi_compiler_prefix.bin):
            src = os.path.join(self.oneapi_compiler_prefix.bin, entry)
            dst = prefix.bin.join(entry)
            os.symlink(src, dst)

        os.symlink(self.oneapi_compiler_prefix.lib, prefix.lib)
        os.symlink(self.oneapi_compiler_prefix.include, prefix.include)
        os.symlink(self.oneapi_compiler_prefix.compiler, prefix.compiler)
        os.symlink(self.oneapi_compiler_prefix.man, prefix.man)
        os.symlink(self.oneapi_compiler_prefix.share, prefix.share)
