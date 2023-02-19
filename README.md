<div align="center">
<img src="assets/logo.png" width="40%"><p></p>
<div>

<img alt="Python" src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
<img alt="Python" src="https://img.shields.io/badge/uses-Streamlit-blue.svg">
<img alt="Python" src="https://img.shields.io/badge/supports-.SRT-blue.svg">
</div>
</div>

## Summary

A simple web application to word-wrap .SRT subtitle files.

## How to use
* Go to this link: [this link](https://vrejf-subtitle-wrapper-sub-wrapper-gp2mv5.streamlit.app/)
* Add your srt-file or a bunch of them
* Set the word-wrap limit
* Check the preview and download!

## Features

* Drag and drop SRT files
* Batch process multiple SRT files at ones
* Wraps subtitles word-by-word
* Creates a zip file with timestamp
* Real-time preview
* Only takes SRT files


## Demo
<img alt="Demo gif" width="70%" src="https://i.ibb.co/cNpxkLG/subwrap-demo.gif" alt="subwrap-demo">


## Example
#### This long caption:

```
 - My mama always said life was like a box of chocolates. You never know what you're gonna get
 ```
 #### Will become this:

```
- My mama always said life was like a box of chocolates. 
  You never know what you're gonna get.
```


## Acknowledgements
* [srt](https://pypi.org/project/srt/)
* [Streamlit](https://streamlit.io)