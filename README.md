# aws-python-picture-to-text
 A Python program that employs AWS Textract to pick up text from images

If you push this program as a AWS Lambda function, it will pick up images from the selected S3 bucket and create a txt file with the text it picked up from the images in that S3 bucket.

In my specific need, I wanted to pick up serial numbers from emails converted to images. If you need a certain need, feel free to change serial_finder function or just get rid of it altogether to get all the text from the image.

The function should not have any dependencies on AWS environment, send me a message if you need any help.