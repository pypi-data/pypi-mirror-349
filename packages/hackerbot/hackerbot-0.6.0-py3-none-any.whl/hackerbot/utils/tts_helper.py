################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.13
#
# This module contains the TTSHelper class that gets or downloads a Piper voice 
# model from HuggingFace
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
# Saad Elbeleidy - https://github.com/sbeleidy
#
# Credits:
# This project makes use of functionality inspired by or adapted from:
# Dimits - https://github.com/Reqeique/Dimits
################################################################################


import os
from huggingface_hub import hf_hub_url
import requests

class TTSHelper:
    """
    Downloads a Piper voice model (.onnx + .json) from HuggingFace
    and stores it in a local directory for future use.
    """

    def __init__(self, cache_dir: str = os.path.expanduser("~/piper_models")):
        """
        Args:
            cache_dir (str): Directory where downloaded models will be stored. Defaults to "~/piper_models".
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_or_download_model(self, model_src: str) -> str:
        """
        If model_src is a valid file path, returns it.
        Otherwise treats it as a HuggingFace voice model name and downloads it.

        Args:
            model_src (str): Either local .onnx path or voice name (e.g., "en_US-amy-low").

        Returns:
            str: Path to ONNX model file.
        """
        if os.path.isfile(model_src):
            return model_src
        return self._download_model_from_huggingface(model_src)

    def _download_model_from_huggingface(self, voice: str) -> str:
        """
        Downloads a Piper voice model (.onnx and .json) from HuggingFace.

        Args:
            voice (str): Voice model name, e.g., "en_US-amy-low".

        Returns:
            str: Path to downloaded .onnx model.

        Raises:
            RuntimeError: If the download fails.
        """
        try:
            locale, person, pitch = voice.split('-')
            lang, country = locale.split('_')
        except ValueError:
            raise RuntimeError(f"Invalid voice model name: {voice}")

        base_path = f"{lang}/{locale}/{person}/{pitch}"
        filename_onnx = f"{voice}.onnx"
        filename_json = f"{voice}.onnx.json"

        url_onnx = hf_hub_url(repo_id="rhasspy/piper-voices", filename=f"{base_path}/{filename_onnx}")
        url_json = hf_hub_url(repo_id="rhasspy/piper-voices", filename=f"{base_path}/{filename_json}")

        path_onnx = os.path.join(self.cache_dir, filename_onnx)
        path_json = os.path.join(self.cache_dir, filename_json)

        if not os.path.exists(path_onnx):
            self._download_file(url_onnx, path_onnx)
        if not os.path.exists(path_json):
            self._download_file(url_json, path_json)

        return path_onnx

    def _download_file(self, url: str, dest_path: str):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            raise RuntimeError(f"Failed to download {url}: {e}")
