# CreateDataForSemanticSegmentation
This project create data for semantic segmentation:
1. crop images 
2. convert masks from color with three channel to one-channel label. For examplе my legend list:
      1. [0, 0, 255] -->     0
      2. [0, 255, 0] -->     1 
      3. [255, 255, 0] -->   2
      4. [255, 255, 255] --> 3
      5. [0, 255, 255] -->   4
      6. [255, 0, 255] -->   5
      7. [255, 0, 0] -->     6
3. create npy-arrays for fast reading from disk
4. create a txt-files with names of images for creating npy-arrays

Original image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/images/original.png)

Crop image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/images/crop.png)

Label image:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/images/label.png)

I increased the brightness so that it was clear why the label look so:

![alt text](https://github.com/tamamolis/CreateDataForSemanticSegmentation/blob/master/images/bright%20label.jpg)
