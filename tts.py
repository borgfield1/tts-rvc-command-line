F="en-US-EmmaMultilingualNeural"
M="en-US-BrianMultilingualNeural"
RATE=5
import argparse
import subprocess
import sys

parser = argparse.ArgumentParser(description="TTS RVC") 
parser.add_argument("--text", "-t", help="text to read", required=True)
parser.add_argument("--gender", "-g", help="gender of the tts if using a girl use --gender f", default="f")
parser.add_argument("--rvc-model", "-rm", help="defualt path is /etc/rvc/models")
parser.add_argument("--edge-save-loc", "-esl", help="edge-tts save location", default="/etc/rvc/tts/output/edge.mp3")
parser.add_argument("--rvc-save-loc", "-rsl", help="rvc save location", default="/etc/rvc/tts/output/rvc.wav")
parser.add_argument("--shift", "-s", help="pitch shift", default=0)
parser.add_argument("--index", "-i", help="index file", default=None)
parser.add_argument("--cuda", "-c", help="use cuda example --cuda cuda:0" default="cpu")

def rvc(model, in_loc, out_loc, shift, index, cuda):
    from rvc_python.infer import RVCInference

    rvc = RVCInference(device=cuda, version="v2")
    rvc.set_params(f0up_key=shift, protect=0.5)
    if not index:
        try: rvc.load_model("/etc/rvc/models/"+model, index_file="/etc/rvc/models/"+index)
        except: rvc.load_model(model, index_path=index)
    else:
        try: rvc.load_model("/etc/rvc/models/"+model)
        except: rvc.load_model(model)
    rvc.infer_file(in_loc, out_loc)

def main():
    args = parser.parse_args()
    text = args.text
    if args.gender.lower() == "f": gender = F
    else: gender = M
    model = args.rvc_model
    edge_loc = args.edge_save_loc
    rvc_loc = args.rvc_save_loc
    shift = int(args.shift)
    index = args.index
    cuda = args.cuda
    subprocess.call(['edge-tts', '-t', f'"{text}"', '-v', gender, '--write-media', edge_loc])
    rvc(model, edge_loc, rvc_loc, shift, index, cuda)





if __name__=="__main__":main()
