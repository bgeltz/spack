# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geopm(AutotoolsPackage):
    """The Global Extensible Open Power Manager (GEOPM) is a framework for
    exploring power and energy optimizations targeting heterogeneous platforms.
    The GEOPM package provides many built-in features. A simple use case is
    reading hardware counters and setting hardware controls with platform
    independent syntax using a command line tool on a particular compute node.
    An advanced use case is dynamically coordinating hardware settings across
    all compute nodes used by a distributed application is response to the
    application's behavior and requests from the resource manager.

    Note: GEOPM interfaces with hardware using Model Specific Registers (MSRs).
    For proper usage make sure MSRs are made available via the msr or
    msr-safe kernel modules by your administrator."""

    homepage = "https://geopm.github.io"
    url = "https://github.com/geopm/geopm/releases/download/v2.0.2/geopm-service-2.0.2.tar.gz"
    git = "https://github.com/geopm/geopm.git"

    maintainers("bgeltz", "cmcantalupo")

    tags = ["e4s"]

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version("develop", branch="dev")
    version("2.0.2", sha256="a44ad1f152dc2cd9492a8a50fb2b0c1c813a9d826573da4a1878abdb7aa8875f")

    # Variants reflecting most ./configure --help options
    variant("debug", default=False, description="Enable debug.")
    variant("coverage", default=False,
            description="Enable test coverage support, enables debug by default.")
    variant("doc", default=True, description="Create man pages with Sphinx.")
    variant("gnu-ld", default=False, description="Assume C compiler uses gnu-ld.")

    # Added dependencies.
    depends_on("ruby-ronn", type="build", when="+doc")
    depends_on("doxygen", type="build", when="+doc")

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("doxygen", type="build", when="+doc")
    depends_on("py-sphinx@5:", type="build", when="+doc")
    depends_on("py-sphinx_rtd_theme@1:", type="build", when="+doc")
    depends_on("py-sphinxemoji@0:", type="build", when="+doc")

    depends_on("py-cycler@0.10.0:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-pandas@0.22.0:", type=("build", "run"))
    depends_on("py-tables@3.4.3:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-cffi@1.6.0:", when="@1.1.0:", type=("build", "run"))
    depends_on("py-pyyaml@5.1.0:", when="@1.1.0:", type=("build", "run"))
    depends_on("py-mock@3.0.0:", when="@1.1.0:", type=("build", "run"))
    depends_on("py-future@0.17.1:", when="@1.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.14.3:", type=("build", "run"))
    depends_on("py-setuptools@39.2.0:", when="@1.0.0:", type="build")
    depends_on("py-natsort@5.3.2:", type=("build", "run"))
    depends_on("py-psutil@5.4.8:", when="@1.0.0:", type=("build", "run"))
    depends_on("py-pylint@1.9.5:", when="@1.1.0:", type=("build", "run"))
    depends_on("py-matplotlib@2.2.3", when="@:1.0.0-rc2", type=("build", "run"))
    depends_on("py-matplotlib@2.2.3:", when="@1.1.0:", type=("build", "run"))

    parallel = False

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")

    def configure_args(self):
        args = []
        args.extend(self.enable_or_disable("debug"))
        args.extend(self.enable_or_disable("coverage"))
        args.extend(self.enable_or_disable("overhead"))
        args.extend(self.enable_or_disable("procfs"))
        args.extend(self.enable_or_disable("mpi"))
        args.extend(self.enable_or_disable("fortran"))
        args.extend(self.enable_or_disable("doc"))
        args.extend(self.enable_or_disable("openmp"))
        args.extend(self.enable_or_disable("ompt"))
        args.extend(self.with_or_without("gnu-ld"))

        return args
