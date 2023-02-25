# import distutils.cmd
import os
import shutil
import distutils.log
import setuptools
import subprocess
from .build_extension import BuildExtension
from .extension import CMakeExtension

class CMakeCommand(BuildExtension):
  """A custom command to run CMake on all Python source files."""

  # description = 'run CMake on Python source files'
  # user_options = [
  #     # The format is (long option, short option, description).
  #     ('pylint-rcfile=', None, 'path to CMake config file'),
  # ]

  # def initialize_options(self):
  #   """Set default values for options."""
  #   # Each user option must be listed here with their default value.
  #   self.pylint_rcfile = ''

  # def finalize_options(self):
  #   """Post-process options."""
  #   if self.pylint_rcfile:
  #     assert os.path.exists(self.pylint_rcfile), (
  #         'CMake config file %s does not exist.' % self.pylint_rcfile)

  def run(self):
    """
    Process all the registered extensions executing only the CMakeExtension objects.
    """

    # Filter the CMakeExtension objects
    cmake_extensions = [e for e in self.extensions if isinstance(e, CMakeExtension)]

    if len(cmake_extensions) == 0:
        raise ValueError("No CMakeExtension objects found")

    # Check that CMake is installed
    if shutil.which("cmake") is None:
        raise RuntimeError("Required command 'cmake' not found")

    for ext in cmake_extensions:

        # Disable the extension if specified in the command line
        if (
            ext.name in self.no_cmake_extensions
            or "all" in self.no_cmake_extensions
        ):
            continue

        # Disable all extensions if this env variable is present
        disabled_set = {"0", "false", "off", "no"}
        env_var_name = "CMAKE_BUILD_EXTENSION_ENABLED"
        if (
            env_var_name in os.environ
            and os.environ[env_var_name].lower() in disabled_set
        ):
            continue

        self.configure_extension(ext)

        print("")
        print("==> Configuring:")
        print(f"$ {' '.join(ext.configure_command)}")
        print("")

        subprocess.check_call(ext.configure_command)
        # subprocess.check_call(ext.build_command)
        # subprocess.check_call(ext.install_command)



