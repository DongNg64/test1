# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
import torch
import os
import tempfile
import time
import imghdr

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        # self.model = torch.load("./weights.pth")

    def predict(
        self,
        source_path: Path = Input(description="Select an source image"),
        target_path: Path = Input(description="Select an target image or video")
       # keep_fps: bool = Input(description="Keep target fps"),
       # keep_frames: bool = Input(description="Keep temporary frames")
    ) -> Path:
        """Run a single prediction on the model"""
        # processed_input = preprocess(image)
        # output = self.model(processed_image, scale)
        # return postprocess(output)
        command = "python run.py "
        #if keep_fps is True:
        #    command += "--keep-fps "
        #if keep_frames is True:
        #    command += "--keep-frames "
        
        # create temp folder save output
        if imghdr.what(target_path) in ["jpeg", "png"]:
            extension = "png"
        else:
            extension = "mp4"
        out_path = Path(tempfile.mkdtemp()) / f"output.{extension}"
        
        command += "-s {source_path} -t {target_path} -o {out_path} --keep-frames --keep-fps --frame-processor face_swapper, face_enhancer". \
        format(source_path=source_path, target_path=target_path, out_path=out_path)
        
        # execute
        os.system(command)
        
        return Path(out_path)
