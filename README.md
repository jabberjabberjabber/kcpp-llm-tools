# Basic functions

## KoboldCpp API Interface

Allows easy use of basic KoboldCpp API endpoints, including streaming generations, images, samplers.

## Instruct Template Wrapping

Finds the appropriate instruct template for the running model and wraps it around content to create a prompt.
 
## Chunking

Will read most types of document and chunk them any size up to max context. Stops at natural break points. Returns the chunks as a list.

## Image Processing

Takes images and resizes them and sends them to the API. Can take almost any image type including most camera RAW files. If there is an embedded JPEG in th RAW it will send that to the LLM, otherwise it will process the RAW into a JPEG and send that. Image files themselves are not changed.

## Video Processing

Will extract frames from videos before and after transitions such as scenes or actions and save them as JPEGs.

# Built-in Features

## Document Processing

Can translate, summarize, distill, or correct most types of documents.

## Adversarial Style Change

Checks input text for unique style and alters it to be less unique, then returns it. Can return multiple different rewrites with uniqueness score for choosing.

## OCR / Handwriting Recognition

Given an image will attempt to read the writing in the image and return it.

## Image Tagging

Takes a directory of images and processes them to get descriptions and keywords and saves them into the image metadata.


  