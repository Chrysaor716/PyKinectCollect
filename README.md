# PyKinectCollect

Uses Kinectv2 (Kinect for Xbox One).

Setup, dependencies, and starter code [here](https://github.com/Kinect/PyKinect2).  
[This article](https://pterneas.com/2014/05/06/understanding-kinect-coordinate-mapping/) is also a good resource on mapping the body coordinates from the camera with Microsoft's Kinect SDK, which the above repo uses.

### TODO
- Currently working on collision detection of PyGame sprites with the bodies from the Kinect's camera feed
    - I'm not sure how to do this...I have the coordinates for all the [joints](https://docs.microsoft.com/en-us/azure/kinect-dk/body-joints) through PyKinect2. I would have to see if the positions of the sprites overlap the *lines* between these joints. Maybe I can convert each of these lines to a sprite and then use `pygame.sprite.spritecollide()`? Or do a bunch of math...(find slope of all lines, which are dynamic and constantly changing...this is too much compute time anyway).
    - What other libraries can I look at? Processing? OpenCV? [libfreenect2](https://github.com/OpenKinect/libfreenect2)?
    - Since I'm already in the PyGame rabbit hole, let's try the first suggestion (converting each skeleton line to a sprite)
    - TODO: currently draws lines in a separate class; need to map out coordinates of joints on PyGame surface to sprites' individual coordinate system (where `start` can either be "greater than" or "less than" `end` points arbitrarily, which complicates things)
- Add x bounds for ball objects
    - and gravity
- Map Kinect camera to projector for distance and scaling when the PyGame surface gets projected to use shadows for interaction



#### Other resources
- Making sprites and detecting collision: http://programarcadegames.com/index.php?chapter=introduction_to_sprites
- More info on Kinect v2 joints and their coordinates: https://medium.com/@lisajamhoury/understanding-kinect-v2-joints-and-coordinate-system-4f4b90b9df16
