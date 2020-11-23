from packageManager import *
from modelBuilder import  *
from  boundBox import *


# with trained/pretrained yolo3 weights, save the compiled model to a path on local
def init_model(weights_path, new_model_path):
    # instantiate the model and save to variable
    model = make_yolov3_model()
    # load the model weights
    weight_reader = WeightReader(weights_path)
    # set the model weights into the model
    weight_reader.load_weights(model)
    # save the model to file, filename should look like model.h5
    model.save(new_model_path)


# for an image given, predict existence of trained category and draw box out of if.
def predict_cat(model_h5, image_file):
    # load yolov3 model
    model = load_model(model_h5, compile=False)
    # define the expected input shape for the model
    input_w, input_h = 416, 416
    # define our new photo
    photo_filename = image_file
    # load and prepare image
    image, image_w, image_h = load_image_pixels(photo_filename, (input_w, input_h))
    # make prediction
    yhat = model.predict(image)
    # summarize the shape of the list of arrays
    print([a.shape for a in yhat])

    # define the anchors
    anchors = [[116, 90, 156, 198, 373, 326], [30, 61, 62, 45, 59, 119], [10, 13, 16, 30, 33, 23]]
    # define the probability threshold for detected objects
    class_threshold = 0.8
    boxes = list()

    for i in range(len(yhat)):
        # decode the output of the network
        boxes += decode_netout(yhat[i][0], anchors[i], class_threshold, input_h, input_w)

    # correct the sizes of the bounding boxes for the shape of the image
    correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w)
    # suppress non-maximal boxes
    do_nms(boxes, 0.5)
    # define the labels
    labels = ["Dress"]
    # get the details of the detected objects
    v_boxes, v_labels, v_scores = get_boxes(boxes, labels, class_threshold)

    # summarize what we found and save the labels to a list
    labelList:list = []
    for i in range(len(v_boxes)):
        # each element in the list is : a list of the label and its probability
        labelList.append([v_labels[i], v_scores[i]])
        # print(v_labels[i], v_scores[i])
    # draw what we found
    #draw_boxes(photo_filename, v_boxes, v_labels, v_scores)
    return labelList