import os
import json
from fastmcp.server import create_proxy

with open('src/remote/config.json', 'r', encoding='utf-8') as f:
    content = f.read()
    with_envs = os.path.expandvars(content)
    data = json.loads(with_envs)

remote_mcps_provider = create_proxy(data)