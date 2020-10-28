#!/usr/bin/python3

import argparse
import os
import time
from edgetpu.detection.engine import DetectionEngine
import cv2

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Face detection")
    parser.add_argument("--video", type=str, default="",
                        help="Path to video file")

    args = parser.parse_args()

    source = args.video    # OpenCV DNN supports 2 networks.
    # 1. FP16 version of the original Caffe implementation ( 5.4 MB )
    # 2. 8 bit Quantized version using TensorFlow ( 2.7 MB )

    modelFile = "./model/face_detection.tflite"
    engine = DetectionEngine(args.model)

    print('Initialized network')
    outputFolder = "output-dnn-videos"
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    cap = cv2.VideoCapture(0)
    outputFile = "capture" + ".avi"

    vid_writer = None
    hasFrame, frame = cap.read()
    print('hasFrame: ', hasFrame)
    if frame is not None:
        vid_writer = cv2.VideoWriter(
            os.path.join(outputFolder, outputFile),
            cv2.VideoWriter_fourcc("M", "J", "P", "G"),
            15,
            (frame.shape[1], frame.shape[0]),
        )

    frame_count = 0
    tt_opencvDnn = 0

    while True:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break

        frame_count += 1
        t = time.time()
        objs = engine.detect_with_image(
            img, threshold=0.05, keep_aspect_ratio=True, relative_coord=False, top_k=10)
        # Print and draw detected objects.
        for obj in objs:
            print('-----------------------------------------')
            print(obj.label_id)
            print('score =', obj.score)
            box = obj.bounding_box.flatten().tolist()
        tt_opencvDnn += time.time() - t
        fpsOpencvDnn = frame_count / tt_opencvDnn
        print('FPS: ', fpsOpencvDnn)
        # label = "OpenCV DNN {} FPS : {:.2f}".format(
        #     device.upper(), fpsOpencvDnn)
        # cv2.putText(
        #     outOpencvDnn,
        #     label,
        #     (10, 50),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     1.3,
        #     (0, 0, 255),
        #     3,
        #     cv2.LINE_AA,
        # )

        # cv2.imshow("Face Detection Comparison", outOpencvDnn)
        if vid_writer is not None:
            vid_writer.write(outOpencvDnn)

        if frame_count == 1:
            tt_opencvDnn = 0

        # k = cv2.waitKey(5)
        # if k == 27:
        #     break

    cv2.destroyAllWindows()
    if vid_writer is not None:
        vid_writer.release()
