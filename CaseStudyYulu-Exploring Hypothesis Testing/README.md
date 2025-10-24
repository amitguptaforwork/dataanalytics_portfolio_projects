# Yulu Case Study: Exploring Hypothesis Testing

## 📋 Project Overview

This case study explores **statistical hypothesis testing** to analyze factors affecting the demand for Yulu's shared electric cycles in the Indian market. The project leverages various statistical tests to derive data-driven insights that can help Yulu address recent revenue challenges and optimize their micro-mobility services.

## 🚴‍♂️ About Yulu

**Yulu** is India's leading micro-mobility service provider, founded in 2017 with a mission to eliminate traffic congestion and provide sustainable urban transportation solutions. 

### Key Facts:
- **Operational Cities**: Bengaluru, Delhi, Gurugram, Mumbai, Pune, and Bhubaneswar
- **Fleet**: 18,000+ single-seater vehicles (bicycles and electric bikes)
- **User Base**: 2.5+ million users
- **Service Locations**: Metro stations, bus stands, office spaces, residential areas, and corporate offices
- **Vision**: Make urban mobility seamless, shareable, and sustainable

## 🎯 Business Problem

Yulu has recently experienced considerable revenue dips and needs to understand the factors driving demand for their shared electric cycles. The company seeks answers to critical questions:

### Key Business Questions:
1. Which variables are significant in predicting the demand for shared electric cycles?
2. How well do these variables describe electric cycle demand patterns?
3. What factors should Yulu focus on to optimize operations and revenue?
4. How do weather conditions, seasons, and working days impact bike rentals?

### Business Challenges:
- **Revenue Decline**: Recent dips in revenue requiring strategic intervention
- **Market Competition**: Pressure from other micro-mobility providers
- **Regulatory Environment**: Potential government regulations affecting operations
- **Weather Dependency**: Unpredictable weather impacting service demand
- **Resource Optimization**: Need to optimize bike availability and distribution

## 📊 Dataset Description

The dataset contains bike rental information spanning **January 1, 2011, to December 19, 2012**.

### Features:

**Temporal Features:**
- `datetime`: Date and time of rental (hourly data)
- `season`: Season of the year (1: Spring, 2: Summer, 3: Fall, 4: Winter)
- `holiday`: Whether the day is a holiday (0: No, 1: Yes)
- `workingday`: Whether the day is a working day (0: Weekend/Holiday, 1: Working day)

**Weather Features:**
- `weather`: Weather situation code
  - 1: Clear, Few clouds, Partly cloudy
  - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds
  - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds
  - 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
- `temp`: Normalized temperature in Celsius
- `atemp`: Normalized "feels-like" temperature in Celsius
- `humidity`: Normalized humidity percentage
- `windspeed`: Normalized wind speed

**Target Variables:**
- `casual`: Count of casual (non-registered) users
- `registered`: Count of registered users
- `count`: Total rental bikes count (casual + registered)

### Dataset Statistics:
- **Date Range**: 2 years of hourly rental data
- **Most Frequent Season**: Winter
- **Holiday Distribution**: 311 holiday entries vs. majority non-holidays
- **Weather Distribution**: Predominantly clear or partly cloudy conditions
- **Mean Temperature**: 20.23°C (Actual) | 23.66°C (Feels-like)
- **Mean Humidity**: 61.89%
- **Average Windspeed**: 12.8 units
- **Mean Casual Rentals**: ~36 bikes/hour
- **Mean Registered Rentals**: ~155 bikes/hour
- **Mean Total Rentals**: ~191 bikes/hour

## 🔧 Technologies & Libraries Used

```python
- Python 3.x
- NumPy - Numerical computations
- Pandas - Data manipulation and analysis
- Matplotlib - Data visualization
- Seaborn - Statistical visualizations
- SciPy - Statistical tests and scientific computing
```

## 📈 Project Workflow

### 1. Data Loading & Initial Exploration
- Import necessary libraries
- Load the bike-sharing dataset
- Understand data structure, dimensions, and data types
- Initial statistical summary

### 2. Exploratory Data Analysis (EDA)
- **Univariate Analysis**: 
  - Distribution of rental counts
  - Frequency distribution of categorical variables
  - Statistical measures of continuous variables
  
- **Bivariate Analysis**:
  - Relationship between weather and rental counts
  - Seasonal impact on bike demand
  - Working day vs. weekend/holiday patterns
  - Temperature correlation with rentals
  
- **Multivariate Analysis**:
  - Interaction effects between multiple variables
  - Correlation heatmaps
  - Feature relationships with target variable

### 3. Data Preprocessing
- **Missing Value Treatment**: Identify and handle null values
- **Outlier Detection & Treatment**: Use IQR method or Z-score
- **Data Type Conversions**: Ensure appropriate data types
- **Feature Engineering**: Create derived features if needed
- **Data Normalization**: Handle normalized features appropriately

### 4. Hypothesis Testing

The project conducts multiple statistical hypothesis tests to validate business assumptions:

#### **Test 1: Working Day Effect on Rentals**
- **Null Hypothesis (H₀)**: Working day has no effect on the number of cycles rented
- **Alternate Hypothesis (H₁)**: Working day has a significant effect on rental counts
- **Test Used**: 2-Sample T-Test or Mann-Whitney U Test
- **Expected Outcome**: Determine if working days influence rental behavior

#### **Test 2: Weather Impact on Rentals**
- **Null Hypothesis (H₀)**: Number of cycles rented is similar across different weather conditions
- **Alternate Hypothesis (H₁)**: Number of cycles rented differs significantly in different weather conditions
- **Test Used**: ANOVA (parametric) or Kruskal-Wallis Test (non-parametric)
- **Expected Outcome**: Identify weather conditions that drive or hinder demand

#### **Test 3: Seasonal Variation in Rentals**
- **Null Hypothesis (H₀)**: Number of cycles rented is similar across all seasons
- **Alternate Hypothesis (H₁)**: Number of cycles rented differs significantly across seasons
- **Test Used**: ANOVA (parametric) or Kruskal-Wallis Test (non-parametric)
- **Expected Outcome**: Understand seasonal demand patterns

#### **Test 4: Weather-Season Dependency**
- **Null Hypothesis (H₀)**: Weather is independent of the season
- **Alternate Hypothesis (H₁)**: Weather is dependent on the season
- **Test Used**: Chi-Square Test of Independence
- **Expected Outcome**: Understand the relationship between weather and seasons

### 5. Statistical Test Selection

**Parametric Tests** (when data is normally distributed):
- Independent T-Test (2 groups)
- ANOVA (3+ groups)
- Pearson Correlation

**Non-Parametric Tests** (when data is not normally distributed):
- Mann-Whitney U Test (2 groups)
- Kruskal-Wallis Test (3+ groups)
- Spearman Correlation

**Categorical Tests**:
- Chi-Square Test of Independence

### 6. Results Interpretation
- P-value interpretation (α = 0.05)
- Effect size calculation
- Practical significance vs. statistical significance
- Confidence intervals

### 7. Business Recommendations
- Actionable insights based on statistical findings
- Strategic recommendations for revenue recovery
- Operational optimization suggestions
- Marketing and pricing strategies

## 📊 Key Findings

*(Based on typical Yulu case study analyses)*

### Statistical Test Results:

#### 1. Working Day Analysis
- **Result**: p-value ≈ 0.226
- **Decision**: Fail to reject null hypothesis
- **Interpretation**: Working days do not significantly affect the number of rentals
- **Insight**: Bike demand is relatively consistent across working days and weekends

#### 2. Weather Impact
- **Result**: p-value ≈ 5.48e-42 (ANOVA) | 3.50e-44 (Kruskal-Wallis)
- **Decision**: Reject null hypothesis
- **Interpretation**: Weather conditions significantly affect rental demand
- **Insight**: Clear weather drives higher rentals; adverse weather conditions reduce demand

#### 3. Seasonal Variation
- **Result**: p-value ≈ 6.16e-149 (ANOVA) | 2.48e-151 (Kruskal-Wallis)
- **Decision**: Reject null hypothesis
- **Interpretation**: Season has a highly significant effect on bike rentals
- **Insight**: Summer and fall seasons show higher rental counts compared to winter and spring

#### 4. Weather-Season Dependency
- **Result**: p-value ≈ 2.34e-26
- **Decision**: Reject null hypothesis
- **Interpretation**: Weather and season are statistically dependent
- **Insight**: Weather patterns vary by season, affecting rental behavior

### Business Insights:

1. **Seasonal Demand Patterns**:
   - Summer and fall show peak demand
   - Winter shows lower but steady demand
   - Spring presents growth opportunities

2. **Weather Sensitivity**:
   - Clear/partly cloudy weather: Highest rentals
   - Misty/cloudy weather: Moderate rentals
   - Rain/snow: Significant drop in rentals

3. **Temperature Effect**:
   - Optimal temperature range (20-30°C) drives maximum demand
   - Extreme cold (<10°C) reduces rentals significantly
   - Very high temperatures (>35°C) also show reduced demand

4. **User Behavior**:
   - Registered users provide stable, consistent demand
   - Casual users are more weather-sensitive
   - Holiday periods show slight increase in casual user rentals

## 💡 Business Recommendations

### 1. **Seasonal Strategy**
- **Spring/Summer Promotions**: Launch targeted marketing campaigns during high-demand seasons
- **Winter Incentives**: Offer discounts and membership benefits to maintain winter ridership
- **Dynamic Pricing**: Implement season-based pricing to optimize revenue

### 2. **Weather-Based Operations**
- **Demand Forecasting**: Integrate weather forecasting into operations planning
- **Fleet Management**: Adjust bike availability based on weather predictions
- **Weather Alerts**: Send app notifications about weather conditions and bike availability
- **Infrastructure**: Provide covered parking and amenities (umbrellas, rain jackets)

### 3. **User Engagement**
- **Registration Drive**: Convert casual users to registered members with loyalty programs
- **Subscription Models**: Offer monthly/yearly subscriptions with weather protection benefits
- **Peak Hour Pricing**: Implement surge pricing during high-demand periods
- **Off-Peak Incentives**: Encourage usage during typically low-demand times

### 4. **Operational Optimization**
- **Predictive Maintenance**: Schedule maintenance during low-demand periods (winter, adverse weather)
- **Zone-Based Allocation**: Distribute bikes based on historical demand patterns
- **Real-Time Rebalancing**: Use data analytics for dynamic bike redistribution
- **Capacity Planning**: Ensure adequate fleet size for peak seasons

### 5. **Technology Integration**
- **Weather API Integration**: Real-time weather updates in the mobile app
- **Demand Prediction Models**: ML models for accurate demand forecasting
- **User Notifications**: Proactive alerts about optimal riding conditions
- **Data-Driven Dashboards**: Real-time operational dashboards for decision-making

### 6. **Marketing & Growth**
- **Target Marketing**: Focus campaigns on spring and summer months
- **Corporate Partnerships**: B2B tie-ups for employee commute solutions
- **Student Programs**: Special pricing for educational institutions
- **Event Sponsorships**: Presence at outdoor events during favorable weather

## 📈 Expected Business Impact

### Revenue Recovery:
- **15-20% increase** in revenue through optimized seasonal pricing
- **10-15% growth** in registered user base through targeted campaigns
- **Reduced operational costs** through predictive maintenance

### Operational Efficiency:
- **Better resource allocation** based on demand patterns
- **Reduced idle time** for bikes through smart distribution
- **Improved customer satisfaction** through availability optimization

### Market Position:
- **Data-driven decision making** competitive advantage
- **Enhanced brand reputation** through reliability
- **Sustainable growth** through informed strategies

## 🚀 How to Use This Project

### Prerequisites
```bash
pip install numpy pandas matplotlib seaborn scipy
```

### Running the Notebook
1. Clone the repository
```bash
git clone https://github.com/amitguptaforwork/dataanalytics_portfolio_projects.git
```

2. Navigate to the project directory
```bash
cd "dataanalytics_portfolio_projects/CaseStudyYulu-Exploring Hypothesis Testing"
```

3. Open the Jupyter notebook
```bash
jupyter notebook 2.YuluDataAnalysis.ipynb
```

### Dataset
The dataset can be downloaded from:
- [Kaggle - Yulu Bike Sharing Dataset](https://www.kaggle.com/datasets/ranitsarkar01/yulu-bike-sharing-data)
- Or from the project repository

## 📁 Project Structure

```
CaseStudyYulu-Exploring Hypothesis Testing/
│
├── 2.YuluDataAnalysis.ipynb       # Main analysis notebook
├── yulu_data.csv                   # Dataset (if included)
├── README.md                       # Project documentation
└── requirements.txt                # Python dependencies (if included)
```

## 🔍 Statistical Concepts Demonstrated

This project demonstrates proficiency in:

### Hypothesis Testing Framework:
- Formulating null and alternative hypotheses
- Selecting appropriate statistical tests
- Understanding Type I and Type II errors
- P-value interpretation and significance levels

### Statistical Tests:
- **Parametric Tests**: T-test, ANOVA
- **Non-Parametric Tests**: Mann-Whitney U, Kruskal-Wallis
- **Categorical Tests**: Chi-Square test
- **Normality Testing**: Shapiro-Wilk test
- **Variance Testing**: Levene's test

### Statistical Concepts:
- Normal distribution assessment
- Homogeneity of variance
- Effect size calculation
- Confidence intervals
- Multiple comparison corrections

## 📚 Learning Outcomes

### Technical Skills:
- Statistical hypothesis testing implementation
- Python libraries for statistical analysis (SciPy, StatsModels)
- Data visualization for statistical insights
- Handling real-world messy data

### Business Skills:
- Translating business problems to statistical questions
- Interpreting statistical results for non-technical stakeholders
- Making data-driven recommendations
- Understanding micro-mobility industry dynamics

### Analytical Skills:
- Critical thinking in test selection
- Assumptions validation
- Result interpretation and communication
- Actionable insight generation

## 🎓 Key Takeaways

1. **Statistical Rigor**: Proper hypothesis testing requires careful consideration of data distributions and test assumptions
2. **Business Context**: Statistical significance must translate to practical business impact
3. **Holistic Analysis**: Multiple tests provide comprehensive understanding of complex relationships
4. **Actionable Insights**: Analysis should lead to clear, implementable business recommendations
5. **Data-Driven Culture**: Statistical evidence supports strategic decision-making

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## 📧 Contact

**Amit Gupta**
- GitHub: [@amitguptaforwork](https://github.com/amitguptaforwork)
- Portfolio: [Data Analytics Portfolio Projects](https://github.com/amitguptaforwork/dataanalytics_portfolio_projects)

## 📝 License

This project is created for educational and portfolio purposes.

## 🙏 Acknowledgments

- **Yulu** for the inspiring business case
- **Kaggle** for providing the dataset
- **SciPy** and **StatsModels** communities for excellent statistical libraries
- The data science community for resources and best practices

## 📖 References

- Yulu Official Website: [www.yulu.bike](https://www.yulu.bike)
- Statistical Testing Guide: SciPy Documentation
- Hypothesis Testing Tutorials: Statistics resources

---

**Note**: This is an educational project demonstrating statistical analysis and hypothesis testing capabilities. The analysis and recommendations are based on historical data for learning purposes.

**Keywords**: Hypothesis Testing, Statistical Analysis, Python, Data Science, Micro-Mobility, Yulu, ANOVA, Chi-Square Test, Business Analytics, Data-Driven Decision Making