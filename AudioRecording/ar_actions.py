# Functions
#currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
import os

def start_recording( action, value):

    if action:
        print("doing")
    else:
        print("not doing")

    return("done")

def stop_recording(action, value):

    if action:
        print("doing" )
    else:
        print( "not doing" )

    return("done")


def action_process_files(i: int):
    """process files"""
    print(currentFuncName(), ":", i)

    files = os.listdir(audio_directory)
    files = os.listdir(audio_directory)

    suffix = "_raw.wav"

    result = list(filter(lambda x: str.endswith(x, suffix), files))

    print("result=", result)
    print("length=", len(result))
    print("-----------")

    for item in result:
        print("item=", item)
        basename = audio_directory + item[:-len(suffix)]

        raw_fn = audio_directory + item
        norm_fn = basename + "_norm.wav"
        mp3_fn = basename + "_final.mp3"

        # ffmpeg -i my_video.mp4 output_audio.wav
        os.system("sox " + raw_fn + " " + norm_fn + " --norm=-3")
        os.system("lame   --abr 64 " + norm_fn + " " + mp3_fn)

    return True


def osc_process_files(address, typetags, arguments):
    print(currentFuncName(), "\taddr:\t", address )
    val = arguments[0]
    print(currentFuncName(), "\tvalue:\t", val )

    if val > 0.99:
        print(currentFuncName(), "\taction:\tyes" )
    elif val < 0.99:
        print(currentFuncName(), "\taction:\tno" )
    else:
        print("Unexpected type:", type(val))