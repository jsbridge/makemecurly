# Make Me Curly

Trying to find the best curly girl friendly products for your hair can be time-consuming and expensive! This app helps you find the best products for your hair based on thousands of Reddit users' experiences. 

## Motivation: Why curly hair products?
The curly hair product industry has really exploded over the last 10 to 15 years. Thousands of new products have appeared on the market,  and helping people take care of their curly hair has become a multi-million dollar industry. However, for those of us with curly hair, the choosing the right products for our hair type is very time-consuming, and the costs can really add up!

## Using the app: Make Me Curly
To address this problem, I have created [Make Me Curly](http://www.makemecurly.today) to recommend the best products for your hair type. 

You upload an image of your hair, and the hair in the image is classified and a list of the most popular products that other people with your hair type recommend. Additionally, Amazon links for each product are provided.

## Behind the scenes: Two convolutional neural networks
When the user uploads an image, it is run through a binary classification convolutional neural network that I built using Keras and Tensorflow to check whether the picture is a picture of hair. This CNN is composed of three convolutional layers that use a rectified linear unit activation function. Each of these layers if followed by a max pooling layer. Two fully connected layers follow, sandwiching a dropout layer to avoid overfitting the training data. The final layer uses a sigmoid activation function, which is ideal for binary classification.

The nonhair training data come from the [Caltech 101](http://www.vision.caltech.edu/Image_Datasets/Caltech101/) dataset with the human face categories removed. The hair training data come from the [Figaro1k](http://projects.i-ctm.eu/it/progetto/figaro-1k) hair dataset. 

![ibis](https://github.com/jsbridge/random_images/blob/master/ibis_image_0051.jpg)![motorcycle](https://github.com/jsbridge/random_images/blob/master/Motorbikes_image_0022.jpg)![mandolin](https://github.com/jsbridge/random_images/blob/master/mandolin_image_0026.jpg)

If the model determines that the picture includes hair, another neural network classifies how curly the hair is in the image, whether it’s very curly, wavy and so on. A PostgreSQL database is then queried for products that are good for that hair type.

## The PostgreSQL database is populated with data from Reddit
I scraped over 9,000 images from the [curly hair subreddit](http://www.reddit.com/r/curlyhair) on Reddit using the Pushshift API. Each of these images is accompanies by a comment from the uploader describing their hair routine and listing the products and product types that they use (this is a rule of the subreddit - if you don't post you're routine, a bot complains!)

## The classfication neural network
I used a pre-trained [VGG16 model](https://neurohive.io/en/popular-networks/vgg16/) with the bottom layers frozen and added two fully connected layers at the end to train a model that classifies each image from Reddit into the hair categories. Between the two fully connected layers is a dropout layer to reduce overfitting, and final layer uses a softmax activation function. The model is trained using the labeled Figaro1k image set, and the input images are masked to block out the background and other things that may bias the results, such as skin color. The classes are straight, wavy, curly, and quite curly.
![masks](https://github.com/jsbridge/random_images/blob/master/masks.jpg)

The accuracy of the model is almost 80% on the test set of images, with good loss, precision, recall, and f1 scores as well.
![acc](https://github.com/jsbridge/random_images/blob/master/VGG_loss_acc.png)
![recall](https://github.com/jsbridge/random_images/blob/master/VGG_prec_recall_f1.png)
The output model can be accessed [here](https://www.dropbox.com/s/u4zs7f2mdv5xg9f/model_saved_VGG_4cat.h5?dl=0).

## Natural language processing with Reddit comments
With the Reddit images classified, I performed natural language processing on the Reddit comments describing the uploader’s routine and products. Here is an example of a comment:
![comment](https://github.com/jsbridge/random_images/blob/master/Screen%20Shot%202020-02-07%20at%2011.37.04%20AM.png)

To parse the comments, I used a master list of popular curly hair products, and searched for product names and types in each comment. However, this is not as simple as it sounds, as people do not alway write out full product names, and sometimes misspell them. 
![products](https://github.com/jsbridge/random_images/blob/master/Screen%20Shot%202020-02-07%20at%202.39.59%20PM.png)

To address this issue, I searched for unique parts of product names, such as “curl and shine," that people are likely to type out, as they are the identifying feature of the product. From there, I searched for product types, such as "styling milk," in the vicinity of the unique phrase. In this way, I was able to reduce each comment to it’s component products.
![better](https://github.com/jsbridge/random_images/blob/master/Screen%20Shot%202020-02-07%20at%202.40.11%20PM.png)

These products were put into the SQL database, and the most popular products are returned to the user when their hair type is identified.
 
## Summary: Better hair, faster!
The purpose of this app is to demystify the process of choosing the best products for your hair type. Check on the curly hair [subreddit](http://www.reddit.com/r/curlyhair) for more tips and moral support!
