project('pyensmallen',
        ['cpp'],
        version: '0.2.5',
        default_options: ['cpp_std=c++14'])

py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11')
ensmallen_dep = dependency('ensmallen')
armadillo_dep = dependency('Armadillo')

# Simplify to bare minimum
py.extension_module('_pyensmallen',
    'pyensmallen_experimental/module.cpp',
    dependencies: [pybind11_dep, armadillo_dep, ensmallen_dep],
    install: true,
    install_dir: py.get_install_dir() / 'pyensmallen_experimental'
)

# Install Python sources separately
py.install_sources(
    [
        'pyensmallen_experimental/__init__.py',
        'pyensmallen_experimental/losses.py',
        'pyensmallen_experimental/gmm.py',
        'pyensmallen_experimental/utils.hpp',
        'pyensmallen_experimental/first_order.hpp',
        'pyensmallen_experimental/newton_type.hpp',
        'pyensmallen_experimental/constrained.hpp'
    ],
    pure: false,
    subdir: 'pyensmallen_experimental'
)