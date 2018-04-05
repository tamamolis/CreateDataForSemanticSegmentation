# CreateDataForSemanticSegmentation
This project create data for semantic segmentation:
1) crop images 
2) convert masks from color with three channel to one-channel label. For exampel my legend list:
   [0, 0, 255] -->     0
   [0, 255, 0] -->     1 
   [255, 255, 0] -->   2
   [255, 255, 255] --> 3
   [0, 255, 255] -->   4
   [255, 0, 255] -->   5
   [255, 0, 0] -->     6
3) create npy-arrays for fast reading from disk

Original image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/original.png)

Crop image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/crop.png)

Label image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/label.png)
