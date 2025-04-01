<div align= "center">
    <h1>Asclepius</h1>
</div>

<p align="center">
   <a href="https://arxiv.org/abs/2402.11217" target="_blank">Full Paper</a>
</p>

## 📖 Overview

This repositry contains:
- Code implementation for running experiments for LLM on Asclepius.
- Asclepius dataset in `./bench_data`. Images in Asclepius are available on [GitHub Releases](https://github.com/StevenSU4/Asclepius/releases/download/v1.0.0/images.zip).

## 💻️ Code

### Installation
1. Clone the repository
```bash
git clone https://github.com/StevenSU4/Asclepius.git
cd Asclepius
```

2. Download benchmark images
- Automated script (recommended, need **wget** and **unzip** installed on local system):
    ```bash
    bash download_images.sh
    ```
- Manual download:  
 Download the ZIP file from [GitHub Releases](https://github.com/your-username/your-repo/releases) and unzip it into the `./bench_data` folder.

3. Make directory for storing results
```bash
mkdir ./eval_results
```

4. Create virtual environment and download libraries
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

#### Project structure
```
.
├── README.md                   # Repository's README
├── bench_data                  # Asclepius dataset
│   ├── Asclepius_bench.json    # Main benchmark data in json
│   ├── Asclepius_bench.xlsx    # Main benchmark data in Excel
│   ├── __MACOSX                # May be contained, neglectable
│   │   └── ...          
│   └── images                  # Benchmark images
│       └── ...                
├── download_images.sh          # For downloading images
├── eval_results                # Empty folder for storing results
├── evaluation.py               # For evaluating model predictions
├── requirements.txt            # For creating virtual environment
├── test.py                     # For generating model predictions
└── venv                        # Created virtual environment folder
```

#### Set up models
1. Set up the model to be benchmarked

- If the tested model is compatible with OpenAI's payload format, just modify the `client` in line 8 in `test.py` and specify which model you use in line 40.
    ```python
    client = OpenAI(
        api_key="your api key here"
        # base_url="your base url here"
    )
    ```
- Otherwise, modify the `ask_image()` function in `test.py` according to comments to call your tested model to make predictions.

2. Set up the evaluator model

To evaluate the benchmarked model's performance, Asclepius utilizes an evaluator model for prediction evaluation, the default model is gpt-4o-mini. (See [full paper](https://arxiv.org/abs/2402.11217) for more detail)

The set up of the evaluator model is the same as setting up the benchmarked model except that modifications should be made in `evaluation.py` instead of `test.py`.

#### Generate predictions
To generate model predictions, simply run:
```bash
python test.py
```
This will result in a `model_predictions.xlsx` file under the `./eval_results` folder containing the predictions made by the benchmarked model.


#### Evaluation and scores
To evaluate the model's predictions, simply run:
```bash
python evaluation.py
```
This will result in a `model_scores.xlsx` file under the `./eval_results` folder containing the scores for each question. Combining this result file with the main benchmark data file `./bench_data/Asclepius_bench.xlsx`, one can easily calculate the average scores for different specialties and capacities of the benchmarked model using Excel.

