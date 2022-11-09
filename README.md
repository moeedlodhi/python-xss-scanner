# python-xss-scanner

A simple XSS vulnerability tool in Python. Article is avialable [here]()


Installation
-----------
1. Clone the repository.

    ```
    git clone https://github.com/iam-mhaseeb/python-xss-scanner.git
    ```
    
2. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

3. You are good to go!

Quick start
-----------

1. Define your own class, inherit it from `BaseXSSScanner`.
2. Implement `get_form_details` as per your needs. 
3. Run the script to run scans with the command below. Replace `{url}` with your website on which you want to run scan.

    ```
    python xss-scanner.py {url} 
    ```


## Authors

* **Muhammad Haseeb** - *Initial work* - [Muhammad Haseeb](https://github.com/iam-mhaseeb)

## Licensing
The project is [MIT Licenced](LICENSE).
