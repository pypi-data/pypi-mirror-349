# Copyright (C) 2023-2025  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information


import base64

from . import utils
from ..data import get_contents, get_too_big_contents


def test_content_raw_data(client):
    content = get_contents()[0]
    query_str = """
    query getContents($swhid: SWHID!) {
      contentsBySWHID(swhid: $swhid) {
        data {
          url
          raw {
            text
            base64
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, swhid=str(content.swhid()))
    archive_url = "https://archive.softwareheritage.org/api/1/"
    assert data["contentsBySWHID"][0] == {
        "data": {
            "url": f"{archive_url}content/sha1:{content.sha1.hex()}/raw/",
            "raw": {
                "text": content.data.decode(),
                "base64": base64.b64encode(content.data).decode("ascii"),
            },
        }
    }


def test_content_raw_data_too_long_content(client):
    content = get_too_big_contents()[0]
    query_str = """
    query getContents($swhid: SWHID!) {
      contentsBySWHID(swhid: $swhid) {
        data {
          raw {
            text
            base64
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, swhid=str(content.swhid()))
    assert data["contentsBySWHID"][0] == {"data": {"raw": None}}
