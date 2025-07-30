import argparse
import collections
import importlib.machinery
import json
import os
import sys
import sysconfig
import traceback
import warnings


if False:  # TYPE_CHECKING
    pass


def version_info_to_dict(obj):  # (object) -> dict[str, Any]
    field_names = ('major', 'minor', 'micro', 'releaselevel', 'serial')
    return {field: getattr(obj, field) for field in field_names}


def get_dict_key(container, key):  # (dict[str, Any], str) -> dict[str, Any]
    for part in key.split('.'):
        container = container[part]
    return container


def generate_data(schema_version):  # () -> None  # noqa: C901
    """Generate the build-details.json data (PEP 739).

    :param schema_version: The schema version of the data we want to generate.
    """

    if schema_version != '1.0':
        raise ValueError('Unsupported schema_version: ' + schema_version)

    data = collections.defaultdict(lambda: collections.defaultdict(dict))

    data['schema_version'] = schema_version

    data['base_prefix'] = sysconfig.get_config_var('installed_base')

    base_interpreter = sysconfig.get_config_var('EXENAME') or getattr(sys, '_base_executable', None)
    if base_interpreter:
        data['base_interpreter'] = base_interpreter

    data['platform'] = sysconfig.get_platform()

    data['language']['version'] = sysconfig.get_python_version()
    data['language']['version_info'] = version_info_to_dict(sys.version_info)

    data['implementation'] = vars(sys.implementation)
    data['implementation']['version'] = version_info_to_dict(sys.implementation.version)

    data['abi']['flags'] = list(sys.abiflags)

    data['suffixes']['source'] = importlib.machinery.SOURCE_SUFFIXES
    data['suffixes']['bytecode'] = importlib.machinery.BYTECODE_SUFFIXES
    data['suffixes']['optimized_bytecode'] = importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES
    data['suffixes']['debug_bytecode'] = importlib.machinery.DEBUG_BYTECODE_SUFFIXES
    data['suffixes']['extensions'] = importlib.machinery.EXTENSION_SUFFIXES

    LIBDIR = sysconfig.get_config_var('LIBDIR')
    LDLIBRARY = sysconfig.get_config_var('LDLIBRARY')
    LIBRARY = sysconfig.get_config_var('LIBRARY')
    PY3LIBRARY = sysconfig.get_config_var('PY3LIBRARY')
    LIBPYTHON = sysconfig.get_config_var('LIBPYTHON')
    LIBPC = sysconfig.get_config_var('LIBPC')
    LIBPL = sysconfig.get_config_var('LIBPL')

    if os.name == 'posix':
        # On POSIX, LIBRARY is always the static library, while LDLIBRARY is the
        # dynamic library if enabled, otherwise it's the static library.
        # If LIBRARY != LDLIBRARY, support for the dynamic library is enabled.
        has_dynamic_library = LDLIBRARY != LIBRARY
        has_static_library = sysconfig.get_config_var('STATIC_LIBPYTHON')
    elif os.name == 'nt':
        # Windows can only use a dynamic library or a static library.
        # If it's using a dynamic library, sys.dllhandle will be set.
        # Static builds on Windows are not really well supported, though.
        # More context: https://github.com/python/cpython/issues/110234
        has_dynamic_library = hasattr(sys, 'dllhandle')
        has_static_library = not has_dynamic_library
    else:
        raise NotADirectoryError('Unknown platform: ' + os.name)

    # On POSIX, EXT_SUFFIX is set regardless if extension modules are supported
    # or not, and on Windows older versions of CPython only set EXT_SUFFIX when
    # extension modules are supported, but newer versions of CPython set it
    # regardless.
    #
    # We only want to set abi.extension_suffix and stable_abi_suffix if
    # extension modules are supported.
    if has_dynamic_library:
        data['abi']['extension_suffix'] = sysconfig.get_config_var('EXT_SUFFIX')

        # EXTENSION_SUFFIXES has been constant for a long time, and currently we
        # don't have a better information source to find the  stable ABI suffix.
        for suffix in importlib.machinery.EXTENSION_SUFFIXES:
            if suffix.startswith('.abi'):
                data['abi']['stable_abi_suffix'] = suffix
                break

        PYTHONFRAMEWORKPREFIX = sysconfig.get_config_var('PYTHONFRAMEWORKPREFIX')
        if PYTHONFRAMEWORKPREFIX:
            # macOS framework builds have a custom location
            data['libpython']['dynamic'] = os.path.join(PYTHONFRAMEWORKPREFIX, LDLIBRARY)
        else:
            data['libpython']['dynamic'] = os.path.join(LIBDIR, LDLIBRARY)

        # FIXME: Not sure if windows has a different dll for the stable ABI, and
        #        even if it does, currently we don't have a way to get its name.
        if PY3LIBRARY:
            data['libpython']['dynamic_stableabi'] = os.path.join(LIBDIR, PY3LIBRARY)

        # Os POSIX, this is defined by the LIBPYTHON Makefile variable not being
        # empty. On Windows, don't link extensions — LIBPYTHON won't be defined,
        data['libpython']['link_extensions'] = bool(LIBPYTHON)

    if has_static_library:
        # Static library can be in a variety of places
        static_libpython_candidates = [
            os.path.join(LIBDIR, LIBRARY),
            os.path.join(LIBPL, LIBRARY),
        ]
        try:
            data['libpython']['static'] = next(filter(os.path.exists, static_libpython_candidates))
        except StopIteration:
            message = (
                "sysconfig.get_config_var('LIBRARY') is set, but none of the following paths "
                'were found on the system: ' + ', '.join(static_libpython_candidates)
            )
            warnings.warn(message, RuntimeWarning, stacklevel=1)

    data['c_api']['headers'] = sysconfig.get_path('include')
    if LIBPC:
        data['c_api']['pkgconfig_path'] = LIBPC

    return data


def make_paths_relative(data, config_path=None):  # (dict[str, Any], str | None) -> None
    # Make base_prefix relative to the config_path directory
    if config_path:
        data['base_prefix'] = os.path.relpath(data['base_prefix'], os.path.dirname(config_path))
    # Update path values to make them relative to base_prefix
    PATH_KEYS = [
        'base_interpreter',
        'libpython.dynamic',
        'libpython.dynamic_stableabi',
        'libpython.static',
        'c_api.headers',
        'c_api.pkgconfig_path',
    ]
    for entry in PATH_KEYS:
        parent, _, child = entry.rpartition('.')
        # Get the key container object
        try:
            container = data
            for part in parent.split('.'):
                container = container[part]

            # KeyError not raised in DefaultDict
            if child not in container:
                continue

            current_path = container[child]
        except KeyError:
            continue
        # Get the relative path
        new_path = os.path.relpath(current_path, data['base_prefix'])
        # Join '.' so that the path is formated as './path' instead of 'path'
        new_path = os.path.join('.', new_path)
        container[child] = new_path


def main():  # () -> None
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument(
        '--schema-version',
        default='1.0',
        help='Schema version of the build-details.json file to generate.',
    )
    parser.add_argument(
        '--relative-paths',
        action='store_true',
        help='Whether to specify paths as absolute, or as relative paths to ``base_prefix``.',
    )
    parser.add_argument(
        '--config-file-path',
        default=None,
        help='If specified, ``base_prefix`` will be set as a relative path to the given config file path.',
    )

    args = parser.parse_args()

    with warnings.catch_warnings(record=True) as data_generation_warnings:
        data = generate_data(args.schema_version)
        if args.relative_paths:
            make_paths_relative(data, args.config_file_path)

    output = {
        'data': data,
        'warnings': [
            {
                'message': str(warning.message),
                'category': '.'.join(warning.category.__module__, warning.category.__qualname__),
                'filename': warning.filename,
                'lineno': warning.lineno,
            }
            for warning in data_generation_warnings
        ],
    }

    json_output = json.dumps(output, indent=2)
    print(json_output)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        data = {
            'error': {
                'kind': str(e.__class__),
                'message': str(e),
            }
        }
        print(json.dumps(data, indent=2))
