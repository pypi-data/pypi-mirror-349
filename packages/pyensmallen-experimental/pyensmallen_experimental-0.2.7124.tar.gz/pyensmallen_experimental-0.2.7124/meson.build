project('pyensmallen-experimental',
        ['cpp'],
        version: '0.2.5',
        default_options: ['cpp_std=c++14'])

py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11')
ensmallen_dep = dependency('ensmallen')
armadillo_dep = dependency('Armadillo')

# Simplify to bare minimum
py.extension_module('_pyensmallen-experimental',
    'pyensmallen-experimental/module.cpp',
    dependencies: [pybind11_dep, armadillo_dep, ensmallen_dep],
    install: true,
    install_dir: py.get_install_dir() / 'pyensmallen-experimental'
)

# Install Python sources separately
py.install_sources(
    [
        'pyensmallen-experimental/__init__.py',
        'pyensmallen-experimental/losses.py',
        'pyensmallen-experimental/gmm.py',
        'pyensmallen-experimental/utils.hpp',
        'pyensmallen-experimental/first_order.hpp',
        'pyensmallen-experimental/newton_type.hpp',
        'pyensmallen-experimental/constrained.hpp'
    ],
    pure: false,
    subdir: 'pyensmallen-experimental'
)