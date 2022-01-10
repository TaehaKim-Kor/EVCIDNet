# Copyright (c) OpenMMLab. All rights reserved.
import asyncio
from argparse import ArgumentParser

from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector, show_result_pyplot)
from val import *
import numpy as np

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.3, help='bbox score threshold')
    parser.add_argument(
        '--async-test',
        action='store_true',
        help='whether to set async options for async inference.')
    args = parser.parse_args()
    return args


def main(args):
    # build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint, device=args.device)
    # test a single image
    result = inference_detector(model, args.img)
    # show the results
    f = open(result_add, 'w', encoding='utf-8')
    if len(result[0]) is not 3:
        print("The number of objects are detected is under the 3.")
    for i in range(len(result[0])):
        tgt_list = [0 for i in range(5)]
        if len(result[0][i]) is not 1:
            for j in range(len(result[0][i])):
                if tgt_list[4] < result[0][i][j][4]:
                    tgt_list = result[0][i][j]
        else:
            tgt_list = result[0][i][0]
        f.write(str(tgt_list))
        f.write("\n")
    f.close()
        #if i == 0:
        #    for j in range(len(result[i])):
                #np.savetxt(nd_result_add,result[i][j])
        #        f.write(str(result[i][j]))
                #with open(nd_result_add,'r') as n:
                #    mytxt=n.readline()
                #    f.write(mytxt)
                #    f.write("\n")
        #        f.write("-----------------\n")
        #    f.write("===================\n")
        #else:
            #for j in range(len(result[i])):
            #    for k in range(len(result[i][j])):
                    #np.savetxt(nd_result_add,result[i][j][k])
            #        f.write(str(result[i][j][k]))
                #with open(nd_result_add, 'r') as n:
                #    mytxt=n.readline()
                #    f.write(mytxt)
                #    f.write("\n")
            #    f.write("-----------------\n")
            #f.write("================\n")
    #f.close()
    show_result_pyplot(model, args.img, result, score_thr=args.score_thr)


async def async_main(args):
    # build the model from a config file and a checkpoint file
    model = init_detector(args.config, args.checkpoint, device=args.device)
    # test a single image
    tasks = asyncio.create_task(async_inference_detector(model, args.img))
    result = await asyncio.gather(tasks)
    # show the results
    show_result_pyplot(model, args.img, result[0], score_thr=args.score_thr)


if __name__ == '__main__':
    args = parse_args()
    if args.async_test:
        asyncio.run(async_main(args))
    else:
        main(args)
