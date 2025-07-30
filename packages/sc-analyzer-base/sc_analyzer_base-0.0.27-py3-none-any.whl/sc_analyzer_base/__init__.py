# The MIT License (MIT)
#
# Copyright (c) 2025 Scott
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__version__ = "0.0.27"

PROJECT_NAME = 'sc-analyzer-base'

__all__ = [
    __version__,
    PROJECT_NAME,
    "BranchUtils",
    "ManifestUtils",
    "MoneyUtils",
    "BaseSummaryDiffAnalyzer",
    "BaseAnalyzer",
]

# 引用顺序不能随意调整，会导致循环依赖的问题
from sc_analyzer_base.utils.branch_utils import BranchUtils
from sc_analyzer_base.utils.manifest_utils import ManifestUtils
from sc_analyzer_base.utils.money_utils import MoneyUtils
from sc_analyzer_base.analyzer.base_summary_diff_analyzer import BaseSummaryDiffAnalyzer
from sc_analyzer_base.analyzer.base_analyzer import BaseAnalyzer
