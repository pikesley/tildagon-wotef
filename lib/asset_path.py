# https://tildagon.badge.emfcamp.org/tildagon-apps/reference/ctx/#adding-images
import os

apps = os.listdir("/apps")  # noqa: PTH208
path = ""
ASSET_PATH = "apps//"

if "github_user_tildagon_wotef" in apps:
    ASSET_PATH = "/apps/github_user_tildagon_wotef/"

if "wotef" in apps:
    ASSET_PATH = "apps/wotef/"
