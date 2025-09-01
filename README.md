# instrument-similarity-analysis
Performance analysis of similarity methods applied to financial instrument time series (CMP223 project).

## 📖 Project Description
This project was developed as part of the **Computer Systems Performance Analysis (CMP223)** discipline at UFRGS.  
The main goal is to study **financial instrument price time series** and evaluate how different methods of similarity/correlation behave in terms of both **statistical quality** and **computational performance**.  

The project bridges financial data analysis with classical system performance metrics, measuring the trade-offs between accuracy and resource consumption.

## ⚙️ Experiment Setup
1. **Instruments**  
   - Example: *PETR3 vs VALE3*  
   - Other pairs or indices may also be tested.  

2. **Parameters**  
   - **Time series period**: 1 day, 7 days, 1 month, 6 months.  
   - **Data granularity**: 1 second, 1 minute, daily prices.  
   - **Correlation / similarity methods**:  
     - Pearson correlation  
     - Spearman correlation  
     - Kendall 
     - Dynamic Time Warping (DTW)  
     - Euclidean distance

3. **Performance Metrics**  
   For each parameter combination, the following are collected:  
   - Execution time  
   - CPU usage  
   - Memory usage  

## 🎯 Objectives
- Compare multiple methods for detecting similarity between financial instruments.  
- Analyze the **trade-offs** between algorithmic accuracy and computational efficiency.  
- Provide insights on how data frequency and observation window affect performance.  


## 📊 Example Results Table

This is a mock example of the type of results expected from the experiments.  
Each row represents a different configuration (Period × Frequency × Method × Instruments),  
and the columns show the collected performance metrics.

| Instruments      | Period   | Frequency | Correlation Method | Execution Time | Memory Usage | CPU Usage |
| ---------------- | -------- | --------- | ------------------ | -------------- | ------------ | --------- |
| INSTRUMENT_X × INSTRUMENT_Y | 1 day    | 1 min     | Pearson            | 0.01s          | 5 MB         | 2%        |
| INSTRUMENT_X × INSTRUMENT_Y | 1 day    | 1 min     | Spearman           | 0.03s          | 6 MB         | 3%        |
| INSTRUMENT_X × INSTRUMENT_Y | 7 days   | Daily     | Kendall Tau        | 0.02s          | 5 MB         | 2%        |
| INSTRUMENT_X × INSTRUMENT_Z | 6 months | 1 sec     | DTW                | 3.50s          | 200 MB       | 45%       |




## 📂 Repository Structure
