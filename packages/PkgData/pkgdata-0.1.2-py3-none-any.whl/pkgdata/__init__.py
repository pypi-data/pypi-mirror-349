"""PkgData"""

from __future__ import annotations

from typing import TYPE_CHECKING

import inspect as _inspect
import importlib.util as _importlib_util
import importlib.resources as _importlib_resources
import importlib.metadata as _importlib_metadata
import sys as _sys
from pathlib import Path as _Path

from pkgdata import exception

if TYPE_CHECKING:
    from types import FrameType, ModuleType


def is_standard_library(module_name: str) -> bool:
    """Check whether a module is part of the current Python version's standard library."""
    return module_name in _sys.stdlib_module_names


def get_all_distribution_names() -> tuple[str, ...]:
    """Get the names of all installed distribution packages.

    Returns
    -------
    distribution_names : tuple[str, ...]
        Installed distribution names, sorted alphabetically (case-insensitive).
    """
    distribution_names = (distribution.name for distribution in _importlib_metadata.distributions())
    unique_distribution_names_sorted = tuple(sorted(set(distribution_names), key=lambda name: name.lower()))
    return unique_distribution_names_sorted


def get_all_package_name_to_distribution_names_mapping() -> dict[str, tuple[str, ...]]:
    """Get a mapping of all installed top-level import package names
    to their corresponding distribution package names.

    Returns
    -------
    mapping : dict[str, tuple[str, ...]]
        Mapping of top-level import package names to distribution package names.
        Each top-level import package may correspond to multiple distribution packages.
        Therefore, the values are tuples of distribution package names.
    """
    mapping = _importlib_metadata.packages_distributions()
    # Sometimes the list of distribution names for a package contains duplicates (seen in editable installs).
    mapping_unique_dist_names = {
        package_name: tuple(sorted(distribution_names, key=lambda name: name.lower()))
        for package_name, distribution_names in mapping.items()
    }
    return mapping_unique_dist_names


def get_all_package_names() -> tuple[str, ...]:
    """Get the names of all installed top-level import packages.

    Returns
    -------
    package_names : tuple[str, ...]
        Installed package names, sorted alphabetically (case-insensitive).
    """
    return tuple(sorted(_importlib_metadata.packages_distributions().keys(), key=lambda name: name.lower()))


def get_caller_frame(stack_up: int = 0) -> _inspect.FrameInfo:
    """Get the frame information of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    stack_up : int, default: 0
        Number of frames to go up in the call stack to determine the caller's frame.
        The default value of 0 returns the frame of this function's direct caller.

    Returns
    -------
    frame_info : inspect.FrameInfo
        Frame information of the caller.

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.

    References
    ----------
    - [Python Documentation: inspect — Inspect live objects: The interpreter stack: inspect.FrameInfo](https://docs.python.org/3/library/inspect.html#inspect.FrameInfo)
    - [Python Documentation: inspect — Inspect live objects: The interpreter stack: inspect.stack](https://docs.python.org/3/library/inspect.html#inspect.stack)
    """
    stack = _inspect.stack()
    # Determine the first external frame in the call stack to exclude internal function calls
    # when this function is called from another function in this package.
    for frame_idx, frame_info in enumerate(stack):
        if frame_info.frame.f_globals["__package__"] != "pkgdata":
            first_external_frame_idx = frame_idx
            break
    else:
        # This case should never happen, as the call stack should always have at least one external frame.
        raise RuntimeError("Could not find an external frame in the call stack.")
    external_stack = stack[first_external_frame_idx:]
    try:
        caller_frame = external_stack[stack_up]
    except IndexError:
        raise exception.PkgDataStackTooShallowError(stack=external_stack, stack_up=stack_up)
    return caller_frame


def get_caller_module(stack_up: int = 0) -> ModuleType | None:
    """Get the module of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    stack_up
        Number of frames to go up in the call stack to determine the caller's module.
        The default value of 0 returns the module of this function's direct caller.

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    """
    caller_frame = get_caller_frame(stack_up=stack_up)
    return _inspect.getmodule(caller_frame.frame)


def get_caller_module_name(stack_up: int = 0) -> str:
    """Get the name of this function's caller's module,
    or a caller higher up in the call stack.

    This function first gets the module of the caller's frame
    using the `pkgdata.get_caller_module` function.
    If the module is available and its name is not "__main__",
    the module name is returned.
    Otherwise, the function gets the file path of the caller's frame
    and converts it to a fully qualified module name,
    by traversing the parent directories until a non-package (no `__init__.py`) is found.
    If the file path does not exist (e.g., it is "<string>" for when eval() or exec() is used),
    the function returns the file path as is.

    Parameters
    ----------
    stack_up
        Number of frames to go up in the call stack to determine the caller's module name.
        The default value of 0 returns the module name of this function's direct caller.

    Returns
    -------
    Name of the caller's module.

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    """
    def filepath_to_module_name(filepath: _Path) -> str:
        """Get the fully qualified module name for a Python file.

        Traverse parent directories until a non-package (no `__init__.py`) is found.
        Assumes the input path is absolute and points to a `.py` file.
        """
        parts = [filepath.stem]
        current_dir = filepath.parent
        while (current_dir / "__init__.py").exists() and (current_dirname := current_dir.name):
            parts.insert(0, current_dirname)
            current_dir = current_dir.parent
        return ".".join(parts)

    caller_module = get_caller_module(stack_up=stack_up)
    if caller_module and (module_name := caller_module.__name__) != "__main__":
        return module_name
    caller_frame = get_caller_frame(stack_up=stack_up)
    caller_filepath = _Path(caller_frame.filename)
    if not caller_filepath.exists():
        # e.g., "<string>" for when eval() or exec() is used to run the code
        return caller_frame.filename
    return filepath_to_module_name(caller_filepath)


def get_caller_name(stack_up: int = 0, lineno: bool = False) -> str:
    """Get the fully qualified name of this function's caller,
    or a caller higher up in the call stack.

    This function first gets the module name of the caller's frame
    using the `pkgdata.get_caller_module_name` function.
    If the caller is in the module's global scope,
    the module name is returned.
    Otherwise, the fully qualified function name of the caller's frame
    within the module is added to the module name,
    and the result is returned.

    Parameters
    ----------
    stack_up
        Number of frames to go up in the call stack to determine the caller's name.
        The default value of 0 returns the name of this function's direct caller.
    lineno
        Add the line number of the caller to the end of the name
        after a colon (":").

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    """
    module_name = get_caller_module_name(stack_up=stack_up)
    frameinfo = get_caller_frame(stack_up=stack_up)
    frame: FrameType = frameinfo.frame
    code = frame.f_code
    parts = [module_name]
    if hasattr(code, "co_qualname"):
        # Python 3.11+
        # https://docs.python.org/3/reference/datamodel.html#codeobject.co_qualname
        # fully qualified function name as a string
        # e.g., "my_function", "MyClass.my_method", "MyClass.InnerClass.my_method"
        qualname = code.co_qualname
        if qualname != "<module>":
            # The caller is not in the module's global scope
            parts.append(qualname)
    # For Python 3.10 and earlier, we need to get the fully qualified name manually
    elif qualname := frame.f_locals.get("__qualname__"):
        # If the function is not in the module's global scope,
        # it has a __qualname__ attribute equivalent to `code.co_qualname`.
        # Here, it cannot be "<module>", since then `f_locals` would be empty.
        parts.append(qualname)
    # The caller is either directly in the module's global scope or in a module-level function.
    elif (func_name := frameinfo.function) != "<module>":
        # The caller is in a module-level function
        parts.append(func_name)
    fullname = ".".join(parts)
    if lineno:
        return f"{fullname}:{frameinfo.lineno}"
    return fullname


def get_distribution_name_from_package_name(package_name: str) -> str:
    """Get the name of an installed distribution package from the name of its top-level import package.

    Parameters
    ----------
    package_name : str
        Name of the top-level import package.

    Returns
    -------
    distribution_name : str
        Name of the distribution package.

    Raises
    ------
    pkgdata.exception.PkgDataPackageNotFoundError
        If the top-level import package cannot be found.
    pkgdata.exception.PkgDataMultipleDistributionsError
        If the top-level import package corresponds to multiple distribution packages.
    """
    mapping = get_all_package_name_to_distribution_names_mapping()
    dist_names = mapping.get(package_name)
    if dist_names is None:
        raise exception.PkgDataPackageNotFoundError(
            package_name=package_name, available_package_names=get_all_package_names()
        )
    if len(dist_names) > 1:
        raise exception.PkgDataMultipleDistributionsError(
            package_name=package_name, distribution_names=dist_names
        )
    return dist_names[0]


def get_package_names_from_distribution_name(distribution_name: str) -> tuple[str, ...]:
    """Get the names of installed top-level import packages from the name of a distribution package.

    Parameters
    ----------
    distribution_name : str
        Name of the distribution package.

    Returns
    -------
    package_names : tuple[str, ...]
        Names of the top-level import packages corresponding to the distribution package.

    Raises
    ------
    pkgdata.exception.PkgDataDistributionNotFoundError
        If the distribution package cannot be found.

    References
    ----------
    - [importlib_metadata GitHub Repository: Pull Request #287: package_distributions implementation](https://github.com/python/importlib_metadata/pull/287/files#diff-bf79a43449f7a7e1e76063e303fbdd35bec7eb50f2e9ddba26e3048def32ed06)
    """
    try:
        distribution = _importlib_metadata.distribution(distribution_name)
    except Exception as e:
        raise exception.PkgDataDistributionNotFoundError(
            distribution_name=distribution_name,
            available_distribution_names=get_all_distribution_names(),
        ) from e
    package_names = (distribution.read_text("top_level.txt") or "").splitlines()
    return tuple(sorted(set(package_names), key=lambda name: name.lower()))


def get_package_name_from_caller(top_level: bool = False, stack_up: int = 0) -> str:
    """Get the package name of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    top_level : bool, default: False
        - If `True`, only the top-level package name is returned,
          i.e., the first part of the package name, e.g., "some_package".
        - If `False`, the fully qualified name of the package is returned,
          e.g., "some_package.some_subpackage".
    stack_up : int, default: 0
        Number of frames to go up in the call stack to determine the caller's package name.
        The default value of 0 returns the package name of this function's direct caller.

    Returns
    -------
    package_name : str
        Name of the caller's package.

    Raises
    ------
    pkgdata.exception.PkgDataCallerPackageNameError
        If the name of the caller's package cannot be determined.
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    """
    caller_frame = get_caller_frame(stack_up=stack_up)
    package_fullname = caller_frame.frame.f_globals["__package__"]
    if package_fullname is None:
        raise exception.PkgDataCallerPackageNameError(frame_info=caller_frame)
    return package_fullname.split(".")[0] if top_level else package_fullname


def get_distribution_name_from_caller(stack_up: int = 0) -> str:
    """Get the name of the distribution package of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    stack_up : int, default: 0
        Number of frames to go up in the call stack to determine the caller's distribution package name.
        The default value of 0 returns the distribution package name of this function's direct caller.

    Returns
    -------
    distribution_name : str
        Name of the caller's distribution package.

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    pkgdata.exception.PkgDataCallerPackageNameError
        If the name of the caller's import package cannot be determined.
    pkgdata.exception.PkgDataMultipleDistributionsError
        If the caller's top-level import package corresponds to multiple distribution packages.
    """
    package_name = get_package_name_from_caller(top_level=True, stack_up=stack_up)
    dist_name = get_distribution_name_from_package_name(package_name)
    return dist_name


def get_package_path_from_caller(top_level: bool = False, stack_up: int = 0) -> _Path:
    """Get the local path to the package of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    top_level : bool, default: False
        - If `True`, the path to the top-level package of the caller is returned,
          even if the caller is a subpackage.
        - If `False`, the path to the caller's direct package is returned,
          whether it is a top-level package or a subpackage.
    stack_up : int, default: 0
        Number of frames to go up in the call stack to determine the caller's package path.
        The default value of 0 returns the package path of this function's direct caller.

    Returns
    -------
    path : pathlib.Path
        Path to the package.

    Raises
    ------
    pkgdata.exception.PkgDataCallerPackageNameError
        If the name of the caller's package cannot be determined.
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    pkgdata.exception.PkgDataPackagePathError
        If the local path to the package cannot be determined.
    """
    name = get_package_name_from_caller(top_level=top_level, stack_up=stack_up)
    path = get_package_path_from_name(name)
    return path


def get_package_path_from_name(package_name: str) -> _Path:
    """Get the local path to an installed package from its name.

    Parameters
    ----------
    package_name : str
        Fully qualified name of the package, e.g., "some_package" or "some_package.some_subpackage".

    Returns
    -------
    path : pathlib.Path
        Path to the package.

    Raises
    ------
    pkgdata.exception.PkgDataPackagePathError
        If the local path to the package cannot be determined.
    """
    try:
        path = _Path(_importlib_resources.files(package_name))
    except Exception as e:
        raise exception.PkgDataPackagePathError(name=package_name) from e
    return path


def get_version_from_distribution_name(distribution_name: str) -> str:
    """Get the version of an installed distribution package from its name.

    Parameters
    ----------
    distribution_name : str
        Name of the distribution package.
        Notice that this is not always the same as the name of the top-level import package.

    Returns
    -------
    version : str
        Version string of the package.

    Raises
    ------
    pkgdata.exception.PkgDataDistributionNotFoundError
        If the distribution package cannot be found.
    """
    try:
        version = _importlib_metadata.version(distribution_name)
    except Exception as e:
        raise exception.PkgDataDistributionNotFoundError(
            distribution_name=distribution_name,
            available_distribution_names=get_all_distribution_names(),
        ) from e
    return version


def get_version_from_package_name(package_name: str) -> str:
    """Get the version of an installed distribution package from the name of its top-level import package.

    Parameters
    ----------
    package_name : str
        Name of the top-level import package.

    Returns
    -------
    version : str
        Version string of the package.

    Raises
    ------
    pkgdata.exception.PkgDataPackageNotFoundError
        If the top-level import package cannot be found.
    pkgdata.exception.PkgDataMultipleDistributionsError
        If the top-level import package corresponds to multiple distribution packages.
    """
    dist_name = get_distribution_name_from_package_name(package_name)
    version = get_version_from_distribution_name(dist_name)
    return version


def get_version_from_caller(stack_up: int = 0) -> str:
    """Get the version of the distribution package of this function's caller,
    or a caller higher up in the call stack.

    Parameters
    ----------
    stack_up : int, default: 0
        Number of frames to go up in the call stack to determine the caller's distribution package version.
        The default value of 0 returns the distribution package version of this function's direct caller.

    Returns
    -------
    version : str
        Version string of the caller's distribution package.

    Raises
    ------
    pkgdata.exception.PkgDataStackTooShallowError
        If the call stack is too shallow for the input `stack_up` argument.
    pkgdata.exception.PkgDataCallerPackageNameError
        If the name of the caller's import package cannot be determined.
    pkgdata.exception.PkgDataMultipleDistributionsError
        If the caller's top-level import package corresponds to multiple distribution packages.
    """
    dist_name = get_distribution_name_from_caller(stack_up=stack_up)
    version = get_version_from_distribution_name(dist_name)
    return version


def import_module_from_path(path: str | _Path, name: str | None = None) -> ModuleType:
    """Import a Python module from a local path.

    Parameters
    ----------
    path : str | pathlib.Path
        Local path to the module.
        If the path corresponds to a directory,
        the `__init__.py` file in the directory is imported.
    name : str | None, default: None
        Name to assign to the imported module.
        If not provided (i.e., None), the name is determined from the path as follows:
        - If the path corresponds to a directory, the directory name is used.
        - If the path corresponds to a `__init__.py` file, the parent directory name is used.
        - Otherwise, the filename is used.

    Returns
    -------
    module : types.ModuleType
        The imported module.

    Raises
    ------
    pkgdata.exception.PkgDataModuleNotFoundError
        If no module file can be found at the given path.
    pkgdata.exception.PkgDataModuleImportError
        If the module cannot be imported.

    References
    ----------
    - [Python Documentation: importlib — The implementation of import: Importing a source file directly](https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly)
    """
    path = _Path(path).resolve()
    if path.is_dir():
        path = path / "__init__.py"
    if not path.exists():
        raise exception.PkgDataModuleNotFoundError(path=path)
    if name is None:
        name = path.parent.stem if path.name == "__init__.py" else path.stem
    try:
        spec = _importlib_util.spec_from_file_location(name=name, location=path)
        module = _importlib_util.module_from_spec(spec)
        _sys.modules[name] = module
        spec.loader.exec_module(module)
    except Exception as e:
        raise exception.PkgDataModuleImportError(name=name, path=path) from e
    return module
