import os
import json
import shutil
from core.utils import get_data_dir, get_images_dir

class UserProfile:
    def __init__(self, profile_path="user_profile.json"):
        self.data_dir = get_data_dir()
        self.images_dir = get_images_dir()
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        self.profile_path = os.path.join(self.data_dir, profile_path)
        self.data = {"name": "", "profile_picture": "", "default_resolution": "720p", "download_path": os.getcwd(), "history_enabled": True, "theme": "Dark", "proxy": "", "social_media_links": {"instagram": "", "twitter": "", "youtube": ""}}
        self.load_profile()

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as f:
                try:
                    self.data = json.load(f)
                    if "social_media_links" not in self.data:
                        self.data["social_media_links"] = {"instagram":"","twitter":"","youtube":""}
                        self.save_profile()
                except:
                    self.save_profile()
        else:
            self.save_profile()

    def save_profile(self):
        with open(self.profile_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def set_profile(self, name, profile_picture, download_path):
        if profile_picture:
            if not os.path.exists(self.images_dir):
                os.makedirs(self.images_dir)
            filename = f"profile_{os.path.basename(profile_picture)}"  
            new_path = os.path.join(self.images_dir, filename)
            old_pic = self.data["profile_picture"]
            if old_pic and os.path.exists(old_pic) and old_pic.startswith(self.images_dir):
                try:
                    os.remove(old_pic)
                except:
                    pass
            try:
                shutil.copy2(profile_picture, new_path)
                self.data["profile_picture"] = new_path
            except Exception as e:
                print(f"Error copying profile picture: {e}")
                self.data["profile_picture"] = ""
        else:
            # If no new picture is provided, keep the old one
            if "profile_picture" in self.data:
                pass  # Do not change the value
            else:
                self.data["profile_picture"] = ""
        self.data["name"] = name
        self.data["download_path"] = download_path
        self.save_profile()

    def set_social_media_links(self, insta, tw, yt):
        self.data["social_media_links"]["instagram"] = insta
        self.data["social_media_links"]["twitter"] = tw
        self.data["social_media_links"]["youtube"] = yt
        self.save_profile()

    def remove_profile_picture(self):
        old_pic = self.data["profile_picture"]
        if old_pic and os.path.exists(old_pic) and old_pic.startswith(self.images_dir):
            try:
                os.remove(old_pic)
            except:
                pass
        self.data["profile_picture"] = ""
        self.save_profile()

    def get_download_path(self):
        return self.data.get("download_path", os.getcwd())

    def get_proxy(self):
        return self.data.get("proxy", "")

    def set_proxy(self, proxy):
        self.data["proxy"] = proxy
        self.save_profile()

    def get_theme(self):
        return self.data.get("theme", "Dark")

    def set_theme(self, theme):
        self.data["theme"] = theme
        self.save_profile()

    def get_default_resolution(self):
        return self.data.get("default_resolution", "720p")

    def set_default_resolution(self, resolution):
        self.data["default_resolution"] = resolution
        self.save_profile()

    def is_history_enabled(self):
        return self.data.get("history_enabled", True)

    def set_history_enabled(self, enabled):
        self.data["history_enabled"] = enabled
        self.save_profile()

    def is_profile_complete(self):
        return bool(self.data["name"])
