# xparse
An email parser that extracts out real estate leads into JSON.

### Prerequisites
git  
Python>=3  
pip3

## Installation
1. Clone this repo 
```bash
git clone https://github.com/jskrnbindra/xparse.git
```
2. `cd` into xparse. `cd xparse`
3. Create a virtualenv and activate it.  
```bash
python3.8 -m venv xparse-env
```  
```bash
cd xparse-env
```
```bash
. bin/activate
```
4. install dependencies
```bash
cd ..
pip3 install -r requirements.txt
```

## Usage
```bash
python3.8 main.py <relative_file_path>
```
Where `<relative_file_path>` is path of an input email (HTML) file.  
And see the output: `less output.json`

### Example
```bash
python3.8 main.py tests/files/input1.html
```
<br></br>
##### Important assumptions
- This module will only be fed a single lead email. Not a list of emails or concatenated HTMLs of multiple emails.
- Input file is not too large in size.
- The structure of the email remains constant.
- The email will have 'X days searching' if it is a buyer lead else will have 'X days Listed' like below:


### Questions? Suggestions? Feedback?
Reach out jskrnbindra@gmail.com
