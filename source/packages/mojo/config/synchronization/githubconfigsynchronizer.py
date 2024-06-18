

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []

from typing import Dict, Tuple, Union

import re

import base64
import json
import io
import yaml
import requests

from http import HTTPStatus

from mojo.errors.exceptions import ConfigurationError, PublishError

from mojo.config.synchronization.configsynchronizerbase import ConfigSynchronizerBase

GITHUB_API_VERSION = "2022-11-28"

class GithubConfigSynchronizer(ConfigSynchronizerBase):
    """
        A directory configuration synchronizer.
    """

    scheme = "github"
    parse_exp = re.compile(r"github://(?P<owner>[a-zA-Z\.0-9\-]+)/(?P<repo>[a-zA-Z\.0-9\-]+)/(?P<leaf>[\S]+)")

    def __init__(self, storage_uri: str, owner: str, repo: str, leaf: str):
        super().__init__(storage_uri)

        self._owner = owner
        self._repo = repo
        self._leaf = leaf
        return

    @classmethod
    def parse(cls, uri: str) -> Union[None, "GithubConfigSynchronizer"]:

        rtnobj = None

        mobj = cls.parse_exp.match(uri)
        if mobj is not None:
            try:
                import pymongo
            except ImportError:
                errmsg = "You must install the 'pymongo' module in order to use couchdb sources."
                raise ConfigurationError(errmsg)

            matchinfo = mobj.groupdict()

            owner = matchinfo["owner"]
            repo = matchinfo["repo"]
            leaf = matchinfo["leaf"]

            rtnobj = GithubConfigSynchronizer(uri, owner, repo, leaf)

        return rtnobj

    def _publish_configuration(self, venue: str, user: str, config_class: str, config_name: str, config_format: str, config_info: str, credentials: Dict[str, Tuple[str, str]]):
        
        username, token = credentials[self._owner]
        
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": GITHUB_API_VERSION
        }

        ref = "heads/main"

        publish_path = f"/users/{user}/{venue}/{config_class}/{config_name}.{config_format}"

        # Step 1 - Get a reference to the head revision 
        ref_url = f"https://api.github.com/repos/{self._owner}/{self._repo}/git/ref/{ref}"
        resp: requests.Response = requests.get(ref_url, headers=headers)
        if resp.status_code != HTTPStatus.OK:
            errmsg = f"Failed to get a reference to branch. ref={ref}"
            raise PublishError(errmsg)

        ref_info = resp.json()

        ref_obj = ref_info["object"]
        top_commit_url = ref_obj["url"]

        # Step 2 - Get the top commit info
        resp: requests.Response = requests.get(top_commit_url, headers=headers)
        if resp.status_code != HTTPStatus.OK:
            errmsg = f"Failed to get the top commit for branch. ref={ref}"
            raise PublishError(errmsg)

        commit_info = resp.json()

        commit_sha = commit_info["sha"]
        commit_tree = commit_info["tree"]
        commit_tree_sha = commit_tree["sha"]
        commit_tree_url = commit_tree["url"]

        # Step 3 - Post a blob of the commit to github
        commit_content_buffer = io.StringIO()
        if config_format == "yaml":
            yaml.safe_dump(config_info, commit_content_buffer, indent=4)
        elif config_format == "json":
            json.dump(config_info, commit_content_buffer, indent=4)
        else:
            errmsg = f"Error publishing config '{config_name}' due to unsupported format. config_format={config_format}"
            raise PublishError(errmsg)

        commit_content = commit_content_buffer.getvalue()

        blob_info = {
            "content": base64.b64encode(commit_content),
            "encoding": "base64"
        }

        blobs_post_url = f"https://api.github.com/repos/{self._owner}/{self._repo}/git/blobs"
        resp: requests.Response = requests.post(blobs_post_url, headers=headers, json=blob_info)
        if resp.status_code != HTTPStatus.ACCEPTED:
            errmsg = f"Failed to post a blob for config. config_name={config_name}"
            raise PublishError(errmsg)
        
        blob_info = resp.json()
        blob_url = blob_info["url"]
        blob_sha = blob_info["sha"]

        # Step 4 - Get a hold of the tree of the top commit
        resp: requests.Response = requests.get(commit_tree_url, headers=headers)
        if resp.status_code != HTTPStatus.OK:
            errmsg = f"Failed to get the tree associated with the top commit for branch. ref={ref}"
            raise PublishError(errmsg)

        top_commit_tree_info = resp.json()
        top_commit_tree_sha = top_commit_tree_info["sha"]

        # Step 5 - Create a commit tree for the publish commit
        create_commit_tree_body = {
            "base_tree": top_commit_tree_sha,
            "tree": [
                {
                    "path": publish_path,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob_sha
                }
            ]
        }

        create_commit_tree_url = f"https://api.github.com/repos/{self._owner}/{self._repo}/git/trees"
        resp: requests.Response = requests.post(create_commit_tree_url, json=create_commit_tree_body, headers=headers)
        if resp.status_code != HTTPStatus.CREATED:
            errmsg = f"Failed to create a commit tree for the publish commmit. config_name={config_name}"
            raise PublishError(errmsg)

        publish_commit_tree_info = resp.json()
        publish_commit_tree_sha = publish_commit_tree_info["sha"]

        commit_message = ""

        # Step 6 - Create the new commit.
        publish_commit = {
            "message": commit_message,
            "parents": [commit_sha],
            "tree": publish_commit_tree_sha
        }

        publish_commit_url = f"https://api.github.com/repos/{self._owner}/{self._repo}/git/commits"
        resp: requests.Response = requests.post(publish_commit_url, json=publish_commit, headers=headers)
        if resp.status_code != HTTPStatus.CREATED:
            errmsg = f"Failed to create a configuration commit. config_name={config_name}"
            raise PublishError(errmsg)
        
        publish_response_info = resp.json()

        publish_commit_sha = publish_response_info["sha"]

        # Step 7 - Update head to point to our publish commit
        move_head_body = {
            "sha": publish_commit_sha,
            "force": False
        }

        resp: requests.Response = requests.patch(ref_url, json=move_head_body, headers=headers)
        if resp.status_code != HTTPStatus.ACCEPTED:
            errmsg = f"Failed to move HEAD to our commit for branch. ref={ref} config_name={config_name}"
            raise PublishError(errmsg)

        return
    
    def _retrieve_configuration(self, venue: str, user: str, config_class: str, config_name: str, credentials: Dict[str, Tuple[str, str]]) -> Union[Tuple[str, dict], Tuple[None, None]]:
        
        config_format = None
        config_info = None

        username, token = credentials[self._owner]
        
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
        }

        publish_path = f"/users/{user}/{venue}/{config_class}/{config_name}.yaml"
        retrieve_url = f"https://github.com/{self._owner}/{self._repo}/releases/latest/download/{publish_path}"
        resp: requests.Response = requests.get(retrieve_url, headers=headers)
        if resp.status_code == HTTPStatus.OK:
            config_buffer = io.StringIO(resp.content)
            config_info = yaml.safe_load(config_buffer)
            config_format = "yaml"

        if config_info is None:
            publish_path = f"/users/{user}/{venue}/{config_class}/{config_name}.json"
            retrieve_url = f"https://github.com/{self._owner}/{self._repo}/releases/latest/download/{publish_path}"
            resp: requests.Response = requests.get(retrieve_url, headers=headers)
            if resp.status_code == HTTPStatus.OK:
                config_buffer = io.StringIO(resp.content)
                config_info = json.load(config_buffer)
                config_format = "json"

        return config_format, config_info
