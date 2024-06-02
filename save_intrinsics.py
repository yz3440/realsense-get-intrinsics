import pyrealsense2 as rs
import json

print("Starting the camera...")
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.z16, 15)
config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.z16, 15)

print("Starting the pipeline...")
cfg = pipeline.start(config)
profile = cfg.get_stream(rs.stream.infrared, 1)  # Fetch stream profile for depth stream

# get camera serial number
serial_number = cfg.get_device().get_info(rs.camera_info.serial_number)
# get the intrinsics
intr = profile.as_video_stream_profile().get_intrinsics()
print("Intrinsics for camera: ", serial_number)
print(intr)

print("Stopping the pipeline...")
pipeline.stop()


# try saving the intrinsics to a json file
print("Saving the intrinsics to a json file...")
try:
    with open(f"{serial_number}_intrinsics.json", "w") as f:
        json.dump(
            {
                "width": intr.width,
                "height": intr.height,
                "fx": intr.fx,
                "fy": intr.fy,
                "ppx": intr.ppx,
                "ppy": intr.ppy,
                "model": intr.model,
            },
            f,
        )
except Exception as e:
    print(f"Error: {e}")
