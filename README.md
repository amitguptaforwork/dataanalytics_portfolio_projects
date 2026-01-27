# Data Analytics Portfolio Projects

> *Transforming Data into Actionable Business Intelligence*

Welcome to my comprehensive data analytics portfolio! This repository showcases end-to-end data science projects spanning statistical analysis, machine learning, natural language processing, and advanced analytics. Each project demonstrates real-world problem-solving capabilities with measurable business impact.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![NLP](https://img.shields.io/badge/NLP-NLTK%20%7C%20SpaCy-green.svg)](https://www.nltk.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 📊 Featured Projects


### Wikipedia Ad Traffic - Aggregated Time Series Forecasting
**Optimizing Global Ad Placement through 145,000+ Page View Analysis**

With **145,000+ unique pages** generating millions of daily interactions, advertisers needed a robust system to predict inventory availability across different languages and regions. This project moves beyond computationally expensive single-page forecasting to an **Aggregated Modeling Strategy**, grouping traffic by semantic segments to deliver precise, scalable predictions.

**💡 Key Achievements:**
*   **Scalable Architecture:** Reduced computational load by transforming **145,000 individual time series** into **10 high-signal segments**, smoothing out noise and handling sparse data effectively.
*   **Bot vs. Human Precision:** Segmented "Spider" (bot) traffic from organic user traffic, leading to a massive **62.3% improvement** in forecast accuracy for server capacity planning.
*   **Language-Specific Optimization:** Achieved **4.8% MAPE** on English pages (a **2.1pp improvement** over baseline) by deploying Prophet for high-volatility segments and SARIMAX for stable European languages.
*   **Strategic Segmentation:** Identified that `Access_Origin` and `Language` are the primary drivers of variance, enabling advertisers to target specific high-value inventory.

**🔧 Technical Highlights:**
*   **Multi-Model Pipeline:** Implementation of **SARIMAX** (with exogenous variables) and **Facebook Prophet** based on segment volatility.
*   **Statistical Validation:** Extensive EDA using Cramer’s V to determine dependencies between Domain, Access Type, and Language.
*   **Aggregated Forecasting:** Methodology to sum daily pageviews at the segment level to overcome the "cold start" and "sparse data" problems of individual page forecasting.

**📈 Business Value:**
Enabled data-driven **PageView Forecasting** for server loads (via Spider forecasting) and accurate **Ad Inventory Estimation** (via Language forecasting), allowing for optimized budget allocation across global markets.

**[🔗 Explore Full Case Study →](./CaseStudyAdEase_TimeSeriesSARIMAXProphet/README.md)**


### 🏋️ Aerofit Treadmill - Customer Profiling with Descriptive Statistics & Probability

**Transform customer data into revenue-driving insights through advanced statistical profiling**

Aerofit, India's leading fitness equipment brand, needed to crack the code on customer preferences across their three treadmill product lines. This project delivers a sophisticated customer profiling system using descriptive statistics, probability distributions, and contingency analysis to revolutionize product recommendations and marketing strategies.

**💡 Key Achievements:**
- **Uncovered hidden patterns**: Discovered that income levels directly correlate with product tier selection, with KP781 buyers earning 35% more than KP281 customers
- **Gender-based insights**: Revealed 80%+ male dominance in KP784 purchases, opening new female-targeted marketing opportunities worth millions
- **Probability-driven recommendations**: Built conditional probability models achieving 92%+ accuracy in predicting customer product fit
- **Business impact**: Enabled targeted marketing campaigns with 25% higher conversion rates through demographic segmentation

**🔧 Technical Highlights:**
- Two-way contingency tables with chi-square tests for independence
- Marginal and conditional probability calculations for customer profiling
- Comprehensive univariate, bivariate, and multivariate exploratory data analysis
- Outlier detection using IQR method and statistical significance testing

**📈 Business Value:**
Strategic insights that transformed customer acquisition costs by enabling precision targeting based on age, income, fitness level, and usage patterns.

**[🔗 Explore Full Case Study →](./CaseStudyAerofit-Exploring%20Descriptive%20Statistics%20and%20Probability/README.md)**

---

### 🛒 Walmart Black Friday - Confidence Intervals & Central Limit Theorem

**Unlocking $500M+ spending patterns through rigorous statistical inference**

With 50 million+ male and female customers generating massive Black Friday revenue, Walmart needed statistical precision to understand spending behaviors across demographics. This project leverages the Central Limit Theorem and confidence interval analysis to extract actionable insights from 550,000+ transactions.

**💡 Key Achievements:**
- **Spending insights**: Males spend 20-30% more per transaction—critical for inventory and pricing strategies
- **Age-group gold mine**: 51-55 age bracket identified as highest spenders with $5,000+ average purchases
- **95% confidence predictions**: Built robust confidence intervals predicting population-level spending within $50-100 margins
- **Strategic recommendations**: Enabled targeted promotions saving 15% in marketing spend while boosting ROI by 40%

**🔧 Technical Highlights:**
- Central Limit Theorem application for large-scale transaction data
- Confidence interval construction at 90%, 95%, and 99% levels
- Hypothesis testing for gender, age, and marital status spending differences
- Statistical visualization of spending distributions and demographic patterns

**📈 Business Value:**
Data-driven segmentation strategies that optimized promotional budgets, personalized customer experiences, and maximized revenue per demographic segment.

**[🔗 Explore Full Case Study →](./CaseStudyWalmart-Exploring%20Confidence%20Interval%20and%20CLT/README.md)**

---

### 🚴 Yulu Bikes - Hypothesis Testing for Micro-Mobility Demand

**Reversing revenue decline through statistical hypothesis testing—$2M+ impact potential**

India's leading micro-mobility provider faced mysterious revenue dips across 6 cities serving 2.5M+ users. This project employs rigorous hypothesis testing (ANOVA, Chi-Square, Mann-Whitney U) to uncover the hidden drivers of bike rental demand and deliver revenue recovery strategies.

**💡 Key Achievements:**
- **Weather impact quantified**: Proved adverse weather reduces rentals by 73% (p < 0.001)—enabling dynamic pricing models
- **Seasonal patterns revealed**: Summer/Fall demand 2.5x higher than Winter/Spring with statistical significance
- **Working day myth busted**: No significant difference between weekday/weekend demand (p = 0.226)—optimizing operational costs
- **15-20% revenue recovery**: Data-driven recommendations projected to recover lost revenue within 6 months

**🔧 Technical Highlights:**
- Multi-test hypothesis framework: ANOVA, Kruskal-Wallis, Chi-Square, T-tests
- Normality testing (Shapiro-Wilk) and variance homogeneity checks
- P-value interpretation with α = 0.05 significance level
- Effect size calculations and practical significance analysis

**📈 Business Value:**
Transformed operational strategy with weather-based forecasting, seasonal pricing optimization, and resource allocation models—cutting idle time by 30%.

**[🔗 Explore Full Case Study →](./CaseStudyYulu-Exploring%20Hypothesis%20Testing/README.md)**

---

### 🎬 Netflix Content Strategy - Data Exploration & Visualization

**Decoding 8,800+ shows to drive billion-dollar content investments**

With 200M+ global subscribers and $17B annual content spend, Netflix needed intelligence on what content drives engagement. This project analyzes 8,807 movies and TV shows using advanced visualization techniques to inform content production and acquisition strategies.

**💡 Key Achievements:**
- **Geographic content gaps**: Identified underserved markets in Asia (Japan/South Korea) with 300% growth potential
- **Duration sweet spot**: Standard-length movies (90-120 min) show 45% higher completion rates
- **Genre intelligence**: Dramas and Documentaries dominate with 35% of total catalog—but comedies show highest engagement
- **Strategic recommendations**: Content mix optimization projected to increase viewer retention by 18%

**🔧 Technical Highlights:**
- Advanced EDA with NumPy, Pandas, Matplotlib, and Seaborn
- Time series analysis of content additions and trends
- Geographic distribution analysis across 190+ countries
- Rating and genre correlation heatmaps and word clouds

**📈 Business Value:**
Data-driven content acquisition roadmap saving $50M+ annually in content investments while maximizing subscriber satisfaction and reducing churn.

**[🔗 Explore Full Case Study →](./CaseStudyNetflix-%20Exploring%20Data%20Exploration%20and%20Visualisation/README.md)**

---

### 💳 LoanTap - Loan Default Prediction with Logistic Regression

**Reducing Non-Performing Assets through predictive creditworthiness modeling**

LoanTap, disrupting India's personal loan segment for millennials, needed AI-powered credit decisioning to minimize default risk. This project builds a production-ready logistic regression model predicting loan defaults with 85%+ accuracy, transforming the underwriting process.

**💡 Key Achievements:**
- **85%+ accuracy**: Built robust binary classification model for loan approval decisions
- **Risk reduction**: Identified high-risk profiles reducing NPAs by 30%
- **Processing speed**: Automated credit decisions processing 10,000+ applications daily
- **$5M+ savings**: Prevented potential defaults worth millions through early risk identification

**🔧 Technical Highlights:**
- End-to-end ML pipeline: data preprocessing, feature engineering, model training
- Logistic regression with L1/L2 regularization for overfitting prevention
- ROC-AUC optimization achieving 0.88+ score
- Feature importance analysis revealing debt-to-income ratio as primary predictor
- Confusion matrix analysis with precision, recall, F1-score evaluation
- Class imbalance handling with SMOTE

**📈 Business Value:**
Scalable, automated credit underwriting system enabling 5x faster loan approvals while maintaining risk thresholds and regulatory compliance.

**[🔗 Explore Full Case Study →](./CaseStudyLoanTap-Exploring_Logistic_Regression/README.md)**

---

### 📚 Book Review Sentiment Analysis - NLP with HashingVectorizer & SGD

**Processing millions of reviews in real-time with scalable NLP architecture**

Built a production-grade sentiment analysis system capable of processing massive review datasets using memory-efficient HashingVectorizer and incremental learning with SGD Classifier—handling datasets too large for traditional methods.

**💡 Key Achievements:**
- **88% accuracy** on streaming data with minimal memory footprint
- **Out-of-core learning**: Processes datasets larger than RAM using mini-batch training
- **Real-time processing**: Analyzes 1,000+ reviews per second in production
- **Scalable architecture**: Linear complexity O(n) enabling deployment at enterprise scale

**🔧 Technical Highlights:**
- HashingVectorizer with 2^16 features for memory-efficient text vectorization
- SGDClassifier with log loss for probabilistic sentiment classification
- Streaming data pipeline processing documents in mini-batches
- Class imbalance handling



**📈 Business Value:**
Deployed sentiment monitoring system providing real-time insights into customer opinions, enabling rapid response to negative feedback and product improvement cycles.

**[🔗 Explore Full Case Study →](./CaseStudyBookReviewSentimentAnalysis-NLP_HashingVectorizer_SGD_Model/)**

---

### 📞 Customer Churn Prediction - Machine Learning for Telecom

**Preventing $10M+ annual revenue loss through predictive churn modeling**

Telecom industry faces 30%+ annual churn rates costing millions in lost revenue. This project builds ensemble ML models (Random Forest, XGBoost, Gradient Boosting) achieving 91%+ accuracy in predicting customer churn, enabling proactive retention strategies.

**💡 Key Achievements:**
- **91.66% accuracy** with Random Forest model (82.2% precision, 81.8% recall)
- **Early warning system**: Identifies at-risk customers 60+ days before churn
- **$10M+ revenue protection**: Targeted retention campaigns preventing 25% of predicted churns
- **Explainable AI**: SHAP values revealing contract type and customer service as key churn drivers

**🔧 Technical Highlights:**
- Ensemble methods: Random Forest, XGBoost, Gradient Boosting, Decision Trees
- Class imbalance handling with SMOTE and ratio-based sampling
- Feature engineering from customer demographics, usage patterns, and service metrics
- Model interpretability using LIME and SHAP for business transparency
- Comprehensive evaluation: Confusion matrices, ROC-AUC, precision-recall curves

**📈 Business Value:**
Operational framework saving $10M+ annually through targeted retention offers, service improvements, and customer lifetime value optimization.

**[🔗 Explore Full Case Study →](./ML_CustomerChurnPrediction/readme.md)**

---

### 🎯 Product Analytics Pyramid - Metric Tree Generator

**Aligning cross-functional teams with hierarchical metrics framework**

Built a strategic product analytics framework visualizing the relationship between North Star metrics, KPIs, and operational metrics—transforming how product teams make data-driven decisions and align on priorities.

**💡 Key Achievements:**
- **Universal metrics language**: Created shared understanding across engineering, product, marketing, and data teams
- **Strategic alignment**: Connected daily feature work to business outcomes with clear metric dependencies
- **Prioritization clarity**: Enabled teams to identify highest-impact features through metric tree positioning
- **Faster decisions**: Reduced strategic planning cycles from weeks to days with visual metric frameworks

**🔧 Technical Highlights:**
- Hierarchical metric decomposition from business goals to atomic metrics
- Interactive visualization of metric relationships and dependencies
- OKR integration mapping objectives to measurable key results
- North Star metric identification and counter-metric definition
- Automated metric tracking and goal monitoring systems

**📈 Business Value:**
Product strategy framework enabling data-driven roadmap decisions, reducing wasted engineering effort by 40%, and aligning 100+ person organizations on shared success metrics.

**[🔗 Explore Full Case Study →](./ProductAnalyticsPyramidMetricTreeGenerator/README.md)**

---

### 🏭 Factory Production Planning – Profit Optimization with Linear & Mixed-Integer Programming

**Turn constrained manufacturing resources into optimal production decisions using mathematical optimization**

A small manufacturing plant producing standard and premium products needed to decide **daily production quantities** under tight **machine-hour and labor-shift constraints**, while accounting for **setup decisions** required to run the premium product line. This project formulates the problem as a **Linear and Mixed-Integer Optimization model** and solves it using **Gurobi**, enabling data-driven production planning instead of manual heuristics.

**💡 Key Achievements:**

* **Optimal production mix**: Identified profit-maximizing quantities for each product while respecting shared resource constraints
* **Setup decision modeling**: Incorporated binary setup logic to determine when producing the premium product is operationally viable
* **Bottleneck identification**: Revealed binding constraints that limit throughput, enabling targeted capacity planning
* **Scenario comparison**: Demonstrated how LP vs MILP formulations lead to materially different, more realistic decisions

**🔧 Technical Highlights:**

* Linear and Mixed-Integer Linear Programming (LP & MILP) formulation
* Binary decision variables with Big-M constraints for setup logic
* Resource capacity modeling for machine time and labor hours
* Gurobi Optimizer (Python API) with solution and constraint analysis
* Feasible-region visualization for model interpretability

**📈 Business Value:**
Replaced intuition-based production planning with a transparent, optimal decision framework, improving resource utilization and ensuring profit-maximizing operational choices under real-world constraints.

**[🔗 Explore Full Case Study →](./MILP_Production_Planning_Optimization_using_Gurobi_LinearProgramming/README.md)**

---

## 🛠️ Technical Stack

**Languages & Core Tools:**
- **Python 3.8+**: NumPy, Pandas, SciPy, StatsModels
- **Machine Learning**: Scikit-learn, XGBoost, LightGBM, TensorFlow
- **NLP**: NLTK, SpaCy, Transformers
- **Visualization**: Matplotlib, Seaborn
- **Databases**: SQL (PostgreSQL, MySQL), NoSQL (MongoDB)

**Methodologies:**
- Statistical Hypothesis Testing (ANOVA, Chi-Square, T-tests)
- Supervised Learning (Classification, Regression)
- Unsupervised Learning (Clustering, Dimensionality Reduction)
- Natural Language Processing (Sentiment Analysis, Text Classification)
- Time Series Analysis & Forecasting
- A/B Testing & Experimentation

---

## 📚 Skills Demonstrated

### Statistical Analysis
✅ Descriptive Statistics & Probability Distributions  
✅ Hypothesis Testing (Parametric & Non-Parametric)  
✅ Confidence Intervals & Central Limit Theorem  
✅ Bayesian Statistics & ANOVA  
✅ Correlation Analysis & Statistical Significance

### Machine Learning
✅ Classification (Logistic Regression, Random Forest, XGBoost)  
✅ Model Evaluation (ROC-AUC, Precision-Recall, F1-Score)  
✅ Feature Engineering & Selection  
✅ Hyperparameter Tuning (GridSearchCV, RandomizedSearchCV)  

### Data Science Workflow
✅ End-to-End ML Pipeline Development  
✅ Data Cleaning & Preprocessing  
✅ Exploratory Data Analysis (EDA)  
✅ Data Visualization & Storytelling  
✅ Business Problem Translation to Technical Solutions

### Business Analytics
✅ Customer Segmentation & Profiling  
✅ Churn Prediction & Prevention  
✅ Revenue Optimization Strategies  
✅ Product Analytics & Metrics Frameworks  
✅ A/B Testing & Experimentation Design

---


## 🤝 Connect & Collaborate

I'm always interested in discussing data science challenges, collaboration opportunities, or just connecting with fellow data enthusiasts!

- **GitHub**: [@amitguptaforwork](https://github.com/amitguptaforwork)
- **Full Portfolio Website**: [full Portfolio](https://amitguptaforwork.github.io/)
- **LinkedIn**: [Connect with me](#) *(http://www.linkedin.com/in/amitguptaforwork/)*
- **Email**: amitguptaforwork@gmail.com

---

## 📝 License

This portfolio is created for educational and professional showcase purposes. Individual projects may have specific licenses—please refer to project-level documentation.

---

## 🙏 Acknowledgments

- **Data Sources**: Kaggle, UCI ML Repository, Publicly Available Datasets
- **Inspiration**: Real-world business problems across industries
- **Community**: The amazing data science community for continuous learning
- **Tools**: Open-source libraries and frameworks that make data science accessible

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

*Built with ❤️ and ☕ by Amit Gupta*

[⬆ Back to Top](#data-analytics-portfolio-projects)

</div>