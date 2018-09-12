# # Psychometric tools benchmark

## 1. Cloning
```bash
$ git clone https://github.com/Marco299/Psychometric-tools-benchmark.git
```
## 2. Configuration
Edit the following configuration file:
* `src/python/db/cfg/setup.yml` - MySQL database configuration
```yaml
mysql:
    host: 127.0.0.1
    user: root
    passwd: *******
    db: apache
```
## 3. Export contents in text files per month from emails
* *Setup*:
    1. Install NLoN package as described [here](https://github.com/M3SOulu/NLoN);
    2. Use a Python 3 environment and install the required packages from `src/python/requirements.txt`.
* *Execution*:
From directory `src/python/export_content` run:
```bash
$ sh run.sh
```
Contents are stored in folder `content`.
## 4. Compute LIWC scores for exported contents
* *Execution*:
    1. Open LIWC software;
    2. From `File` select dictionary to use (2007 or 2015);
    3. From `File` click  `Analyze text in folder..` and select `content` folder described in step 3;
    4. From `File` click  `Save results..`.
## 5. Save LIWC scores into database
* *Setup*:
    Use a Python 3 environment as described in Step 3.
* *Execution*:
From directory `src/python/save_liwc_scores` run:
```bash
$ sh run.sh <liwc_file> <liwc_dictionary>
```
where:
* liwc_file: csv file saved in Step 4 (iv)
* liwc_dictionary: LIWC dictionary selected in Step 4, either `2007` or `2015`
## 6. Compute developers' Big Five traits scores
* *Setup*:
    Use a Python 3 environment as described in Step 3.
* *Execution*:
From directory `src/python/big5` run:
```bash
$ sh run.sh <liwc_dictionary>
```
where:
* liwc_dictionary: LIWC dictionary selected in Step 4 (ii), either `2007` or `2015`