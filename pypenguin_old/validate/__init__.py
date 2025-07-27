################################################################################################
# This package is supposed to check if given data is valid according to  my "optimzed format"  #
# (https://github.com/Fritzforcode/PyPenguin/blob/main/Optimized%20Format%20Documentation.md). #
# I do NOT guarantee, that this package is able to detect every possible szenario,             #
# where the data is invalid but it does detect many.                                           #
# If you find an error szenario, which this package does not detect please tell me on Github.  #
# (https://github.com/Fritzforcode/PyPenguin/issues/).                                         #
################################################################################################

from .main import validateProject
from .errors import PP_ValidationError
