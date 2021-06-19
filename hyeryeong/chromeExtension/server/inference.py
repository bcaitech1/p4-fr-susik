import torch
from torchvision import transforms
from PIL import Image
import time
from Model.flags import Flags
from Model.checkpoint import load_checkpoint
from Model.SATRN import SATRN


START = "<SOS>"
END = "<EOS>"
PAD = "<PAD>"
SPECIAL_TOKENS = [START, END, PAD]

def id_to_string(tokens, vocab ,do_eval=0):
    result = []
    if do_eval:
        eos_id = vocab["token_to_id"]["<EOS>"]
        special_ids = set([vocab["token_to_id"]["<PAD>"], vocab["token_to_id"]["<SOS>"], eos_id])

    for example in tokens:
        string = ""
        if do_eval:
            for token in example:
                token = token.item()
                if token not in special_ids:
                    if token != -1:
                        string += vocab["id_to_token"][token] + " "
                elif token == eos_id:
                    break
        else:
            for token in example:
                token = token.item()
                if token != -1:
                    string += vocab["id_to_token"][token] + " "

        result.append(string)
    return result

def inference(image):
    
    # print(image)
    
    # print(type(image))
    
    checkpoint_path = "./checkpoints/0070.pth"
    tokens_path = "./Model/tokens.txt"
    
    is_cuda = torch.cuda.is_available()
    checkpoint = load_checkpoint(checkpoint_path, cuda=is_cuda)
    options = Flags(checkpoint["configs"]).get()
    
    hardware = "cuda" if is_cuda else "cpu"
    device = torch.device(hardware)
    
    print("--------------------------------")
    print("Running {} on device {}\n".format(options.network, device))
    
    model_checkpoint = checkpoint["model"]
    if model_checkpoint:
        print(
            "[+] Checkpoint\n",
            "Resuming from epoch : {}\n".format(checkpoint["epoch"]),
        )
    print("input height :", options.input_size.height)
    print("input width :", options.input_size.width)

    transformed = transforms.Compose(
        [
            transforms.Resize((options.input_size.height, options.input_size.width)),
            transforms.ToTensor(),
        ]
    )
    
    image = image.convert("L")
    
    tensor = transformed(image)
    tensor = torch.stack([tensor,tensor], dim=0)
    
    dummy_gt = torch.zeros((2,232))+158
    
    start = time.time()
    
    model = SATRN(options, checkpoint, model_checkpoint).to(device)
    
    print('SATRN model load')
    
    model.eval()
    
    output = model(tensor.to(device), dummy_gt.to(device), False, 0.0)
    
    decoded_values = output.transpose(1, 2)
    _, sequence = torch.topk(decoded_values, 1, dim=1)
    
    sequence = sequence.squeeze(1)
    
    sequence_str = id_to_string(sequence, checkpoint, do_eval=1)[0]
    
    cnt_left = 0
    cnt_right = 0
    idx = 0
    for ch in sequence_str:
        if ch == '{':
            cnt_left += 1
        elif ch != ' ':
            cnt_left = 0
        if ch == '}':
            cnt_right += 1
        elif ch != ' ':
            cnt_right = 0
        if cnt_left >= 2 or cnt_right >=2:
            sequence_str = sequence_str[0:idx-1]
            break
        idx+=1       
            
    
    print("time elapsed {}\n".format(time.time() - start))
    print("sequence: {}\n".format(sequence_str))
    
    return sequence_str

    