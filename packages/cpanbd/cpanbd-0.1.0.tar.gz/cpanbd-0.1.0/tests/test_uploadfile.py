from cpanbd.uploadfile import UploadFile
from cpanbd.utils.const import APPNAME

pan = UploadFile()


def test_upload():
    local_filename = "tdata/独秀机器人/Robot0309.zip"
    upload_path = f"/apps/{APPNAME}/tdata/独秀机器人/Robot0309.zip"

    pan.upload_file(
        local_filename=local_filename,
        upload_path=upload_path,
        isdir=0,
        rtype=1,
        bs=32,
        show_progress=True,
    )
