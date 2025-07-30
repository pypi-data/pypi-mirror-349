# Copyright (C) 2024-2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import Optional

from swh.graphql.server import get_config
from swh.objstorage.interface import objid_from_dict

from .base_node import BaseNode
from .content import BaseContentNode


class ContentDataNode(BaseNode):
    obj: BaseContentNode

    @property
    def url(self) -> str:
        content_sha1 = self.obj.hashes["sha1"]
        archive_url = "https://archive.softwareheritage.org/api/1/"
        return f"{archive_url}content/sha1:{content_sha1}/raw/"

    @property
    def raw(self) -> Optional[bytes]:
        # Return content data as a binary string
        if self.obj.length <= get_config().get("max_raw_content_size", 10000):
            assert self.obj._node is not None
            return self.archive.get_content_data(
                objid_from_dict(self.obj._node.to_dict())
            )
        return None

    def _get_node_data(self):
        # No new data to fetch: everything is either available
        # or can be computed from the parent (self.obj)
        # raw data is fetched from a property to avoid pre-loading
        return {}
