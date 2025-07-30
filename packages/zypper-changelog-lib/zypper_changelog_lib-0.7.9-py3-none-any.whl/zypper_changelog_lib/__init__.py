# SPDX-FileCopyrightText: 2025 The Rockstor Project <support@rockstor.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
from .zyppchangelog import get_zypper_changelog, get_zypper_repo_dict, zypp_info_codes, \
    zypp_err_codes

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

__all__ = [
    "get_zypper_changelog",
    "get_zypper_repo_dict",
    "zypp_info_codes",
    "zypp_err_codes"
]
