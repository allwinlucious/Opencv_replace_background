# Opencv_replace_background
Replace background of diagrams |

1) Run configure.py to create all necessary folders and generate config file if necessary.  
2) edit config.txt if needed   

a) white_threshold : vary this to remove white background better  
b) dialate_kernel : decrease the padding (use odd number) (preferably do not change)  
c) erode_kernel : increase the padding (use odd number) (preferably do not change)  
d) dilate_iterations : decrease the padding  
e) erode_iterations : increase the padding  
f) anti_alias_kernel : makes the padding smooth (use odd number) (preferably do not change)  
g) anti_alias_sigma : makes the padding smooth  
h) background_blur : adjust the blur of background  

3)run batch_process.py   
if only one background image is inside backgrounds folder then it is used, if more images are present then random one is chosen  
![diagram3](https://user-images.githubusercontent.com/15308488/184498147-461fb0c1-d73c-4c29-b0e2-1dd24d2b821b.png)
![diagram3](https://user-images.githubusercontent.com/15308488/184498153-737f6f5f-d682-47fd-a417-627a55ca937f.png)
