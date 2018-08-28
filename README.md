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
    1. Install NLoN package as described [here](https://github.com/M3SOulu/NLoN)
    2. Use a Python 3 environment and install the required packages from `src/python/requirements.txt`
* *Execution*:
From directory `src/python/export_content` run:
```bash
$ sh run.sh
```
Contents are stored in folder `content`.
## 4. Compute developers' Big Five traits scores using LIWC
* *Execution*:
    1. Open LIWC software;
    2. From `File` click  `Analyze text in folder..` and select `content` folder described at step 3;
    3. From `File` click  `Save results..`.