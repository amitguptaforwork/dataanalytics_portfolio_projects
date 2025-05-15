# AeroFit Treadmill Product Recommendation Case Study

## Project Overview
This case study explores customer profiles and preferences for AeroFit treadmill products to develop a focused marketing strategy. The analysis uses descriptive statistics and probability concepts to identify the characteristics of customers most likely to purchase each of AeroFit's three treadmill models (KP281, KP481, and KP781).

## Business Context
AeroFit is a leading brand in the fitness equipment industry that sells treadmills through specialty fitness equipment stores. The company offers three treadmill products differentiated by features and price points:

- **KP281**: Entry-level model ($1,500)
- **KP481**: Mid-level model ($1,750)
- **KP781**: Advanced model ($2,500)

## Dataset Description
The analysis is based on a dataset containing customer information including:
- Product purchased
- Age
- Gender
- Education level
- Relationship status
- Annual household income
- Average number of times the customer plans to use the treadmill each week
- Self-rated fitness level
- Days of usage of previous treadmill ownership
- Income
- Fitness level
- Miles expected to run

## Statistical Concepts Explored

### 1. Descriptive Statistics
- **Measures of Central Tendency**: Mean, median, and mode calculations across different demographic variables
- **Measures of Dispersion**: Standard deviation, variance, range, and IQR to understand the spread of numerical variables
- **Frequency Distributions**: Analysis of categorical variables and their distributions
- **Cross-tabulation**: Exploring relationships between categorical variables

### 2. Probability Concepts
- **Conditional Probability**: Analyzing purchase patterns given specific customer attributes
- **Probability Distributions**: Examining the distribution of customer characteristics
- **Joint Probability**: Assessing the likelihood of combinations of customer attributes

### 3. Data Visualization Techniques
- **Histograms and Density Plots**: Visualizing distributions of numerical variables
- **Bar Charts and Pie Charts**: Representing categorical data distributions
- **Box Plots**: Identifying outliers and comparing distributions across product categories
- **Scatter Plots**: Examining relationships between continuous variables
- **Heat Maps**: Visualizing correlation matrices between variables

## Key Visualizations

### Income Distribution by Product
![Income Distribution](https://raw.githubusercontent.com/amitguptaforwork/dataanalytics_portfolio_projects/main/CaseStudyAerofit-Exploring%20Descriptive%20Statistics%20and%20Probability/images/income_distribution.png)

*This visualization shows the income distribution across different treadmill products, highlighting that higher-income customers tend to purchase the premium KP781 model.*

### Age Distribution by Product
![Age Distribution](https://raw.githubusercontent.com/amitguptaforwork/dataanalytics_portfolio_projects/main/CaseStudyAerofit-Exploring%20Descriptive%20Statistics%20and%20Probability/images/age_distribution.png)

*This analysis demonstrates the age distribution for each treadmill model, showing that younger customers typically prefer the KP281 model while older customers lean toward the KP781 model.*

### Correlation Heatmap
![Correlation Heatmap](https://raw.githubusercontent.com/amitguptaforwork/dataanalytics_portfolio_projects/main/CaseStudyAerofit-Exploring%20Descriptive%20Statistics%20and%20Probability/images/correlation_heatmap.png)

*The correlation heatmap reveals relationships between variables, with strong positive correlations between income, fitness level, and preference for premium models.*

### Product Distribution by Education Level
![Product by Education Level](https://raw.githubusercontent.com/amitguptaforwork/dataanalytics_portfolio_projects/main/CaseStudyAerofit-Exploring%20Descriptive%20Statistics%20and%20Probability/images/education_product.png.png)

*This visualization demonstrates how gender and marital status affect product selection, providing insights for targeted marketing.*

## Key Findings

1. **Income Correlation**: Strong positive correlation between income and purchase of premium models (KP781)
2. **Age Factors**: 
   - KP281: Popular among younger customers (20-30)
   - KP481: Preferred by middle-aged customers (30-40)
   - KP781: Favored by older customers (40+)
3. **Usage Patterns**: Higher expected usage correlates with preference for premium models
4. **Education Impact**: Higher education levels show greater likelihood of purchasing premium models
5. **Gender Differences**: Male customers show higher preference for the premium KP781 model

## Business Recommendations

1. **Targeted Marketing**:
   - KP281: Position for younger, budget-conscious customers with basic fitness needs
   - KP481: Market to middle-income families seeking reliable fitness equipment
   - KP781: Target higher-income professionals with advanced fitness requirements

2. **Product Bundling**:
   - Offer complementary accessories based on customer profiles
   - Develop loyalty programs aligned with anticipated usage patterns

3. **Feature Development**:
   - Enhance features that resonate with specific demographic segments
   - Consider price point adjustments based on perceived value

4. **Distribution Strategy**:
   - Focus premium models in high-income geographic areas
   - Position entry-level models in areas with younger demographics

## Technical Implementation

This analysis was conducted using Python with the following libraries:
- Pandas for data manipulation
- NumPy for numerical computations
- Matplotlib and Seaborn for data visualization
- SciPy for statistical calculations

The complete analysis process included:
- Data cleaning and preprocessing
- Exploratory data analysis
- Statistical testing
- Visualization development
- Insight generation

## Conclusion

The AeroFit case study demonstrates the power of descriptive statistics and probability concepts in understanding customer segmentation and product preferences. By analyzing demographic and behavioral patterns, AeroFit can develop targeted marketing strategies to optimize their product positioning and maximize sales across different customer segments.

The statistical approach provides a data-driven foundation for business decision-making, highlighting the practical application of data analytics in real-world marketing scenarios.
