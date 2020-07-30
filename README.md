# PyKinectCollect

Uses Kinectv2 (Kinect for Xbox One).

Setup, dependencies, and starter code [here](https://github.com/Kinect/PyKinect2).  
[This article](https://pterneas.com/2014/05/06/understanding-kinect-coordinate-mapping/) is also a good resource on mapping the body coordinates from the camera with Microsoft's Kinect SDK, which the above repo uses.

### TODO
- Stretch goal: Ball sprite collision with one another
    - And just improving the physics overall
- Map Kinect camera to projector for distance and scaling when the PyGame surface gets projected to use shadows for interaction
    - Consider possibly using the Kinect's depth data to accomplish this



#### Other resources
- Making sprites and detecting collision: http://programarcadegames.com/index.php?chapter=introduction_to_sprites
- More info on Kinect v2 joints and their coordinates: https://medium.com/@lisajamhoury/understanding-kinect-v2-joints-and-coordinate-system-4f4b90b9df16
- Kinect coordinate conversions compatible with OpenCV: https://docs.microsoft.com/en-us/azure/kinect-dk/use-calibration-functions
- Mapping infrared camera to projection plane: https://eclecti.cc/computergraphics/easy-interactive-camera-projector-homography-in-python
