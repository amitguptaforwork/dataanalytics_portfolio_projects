# Customer Churn Prediction - End-to-End Data Analytics Project
# Topic: Predictive Analytics Models for Customer Behavior Forecasting

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

class CustomerChurnPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.models = {}
        self.best_model = None
        self.feature_importance = None
        
    def generate_synthetic_data(self, n_samples=10000):
        """
        Generate synthetic customer data for churn prediction
        """
        print("🔄 Generating synthetic customer dataset...")
        
        # Customer demographics
        customer_ids = [f"CUST_{i:06d}" for i in range(1, n_samples + 1)]
        ages = np.random.normal(45, 15, n_samples).astype(int)
        ages = np.clip(ages, 18, 80)
        
        genders = np.random.choice(['Male', 'Female'], n_samples, p=[0.52, 0.48])
        
        # Account information
        account_length = np.random.exponential(scale=24, size=n_samples).astype(int)
        account_length = np.clip(account_length, 1, 120)  # 1-120 months
        
        # Service usage patterns
        monthly_charges = np.random.normal(65, 25, n_samples)
        monthly_charges = np.clip(monthly_charges, 20, 150)
        
        total_charges = monthly_charges * account_length + np.random.normal(0, 100, n_samples)
        total_charges = np.maximum(total_charges, monthly_charges)
        
        # Service features
        internet_service = np.random.choice(['DSL', 'Fiber', 'No'], n_samples, p=[0.35, 0.45, 0.20])
        online_security = np.random.choice(['Yes', 'No'], n_samples, p=[0.4, 0.6])
        tech_support = np.random.choice(['Yes', 'No'], n_samples, p=[0.35, 0.65])
        streaming_tv = np.random.choice(['Yes', 'No'], n_samples, p=[0.45, 0.55])
        streaming_movies = np.random.choice(['Yes', 'No'], n_samples, p=[0.42, 0.58])
        
        # Contract and payment information
        contract_type = np.random.choice(['Month-to-month', 'One year', 'Two year'], 
                                       n_samples, p=[0.55, 0.25, 0.20])
        payment_method = np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'],
                                        n_samples, p=[0.35, 0.15, 0.25, 0.25])
        paperless_billing = np.random.choice(['Yes', 'No'], n_samples, p=[0.6, 0.4])
        
        # Behavioral metrics
        customer_service_calls = np.random.poisson(2, n_samples)
        late_payments = np.random.poisson(1.5, n_samples)
        
        # Usage metrics
        avg_monthly_gb = np.random.exponential(15, n_samples)
        avg_monthly_minutes = np.random.normal(450, 200, n_samples)
        avg_monthly_minutes = np.maximum(avg_monthly_minutes, 0)
        
        # Satisfaction scores (1-10)
        satisfaction_score = np.random.normal(7, 2, n_samples)
        satisfaction_score = np.clip(satisfaction_score, 1, 10)
        
        # Generate churn based on realistic patterns
        churn_probability = self._calculate_churn_probability(
            ages, account_length, monthly_charges, contract_type, 
            customer_service_calls, late_payments, satisfaction_score,
            internet_service, payment_method
        )
        
        churned = np.random.binomial(1, churn_probability, n_samples)
        
        # Create DataFrame
        data = pd.DataFrame({
            'customer_id': customer_ids,
            'age': ages,
            'gender': genders,
            'account_length_months': account_length,
            'monthly_charges': monthly_charges,
            'total_charges': total_charges,
            'internet_service': internet_service,
            'online_security': online_security,
            'tech_support': tech_support,
            'streaming_tv': streaming_tv,
            'streaming_movies': streaming_movies,
            'contract_type': contract_type,
            'payment_method': payment_method,
            'paperless_billing': paperless_billing,
            'customer_service_calls': customer_service_calls,
            'late_payments': late_payments,
            'avg_monthly_gb_used': avg_monthly_gb,
            'avg_monthly_minutes': avg_monthly_minutes,
            'satisfaction_score': satisfaction_score,
            'churned': churned
        })
        
        print(f"✅ Generated dataset with {len(data)} customers")
        print(f"📊 Churn rate: {churned.mean():.2%}")
        
        return data
    
    def _calculate_churn_probability(self, ages, account_length, monthly_charges, 
                                   contract_type, service_calls, late_payments, 
                                   satisfaction, internet_service, payment_method):
        """
        Calculate realistic churn probabilities based on customer characteristics
        """
        base_prob = 0.15
        
        # Age factor (younger customers more likely to churn)
        age_factor = np.where(ages < 30, 0.05, 
                             np.where(ages > 60, -0.03, 0))
        
        # Account length factor (newer customers more likely to churn)
        length_factor = np.where(account_length < 6, 0.1,
                               np.where(account_length > 24, -0.05, 0))
        
        # Contract factor
        contract_factor = np.where(contract_type == 'Month-to-month', 0.08,
                                 np.where(contract_type == 'Two year', -0.06, -0.02))
        
        # Service and satisfaction factors
        service_factor = (service_calls - 2) * 0.02
        payment_factor = (late_payments - 1) * 0.03
        satisfaction_factor = (7 - satisfaction) * 0.01
        
        # Internet service factor
        internet_factor = np.where(internet_service == 'Fiber', -0.02,
                                 np.where(internet_service == 'No', 0.03, 0))
        
        # Payment method factor
        payment_factor_method = np.where(payment_method == 'Electronic check', 0.03, -0.01)
        
        total_prob = (base_prob + age_factor + length_factor + contract_factor + 
                     service_factor + payment_factor + satisfaction_factor + 
                     internet_factor + payment_factor_method)
        
        return np.clip(total_prob, 0.05, 0.8)
    
    def perform_eda(self, data):
        """
        Perform comprehensive exploratory data analysis
        """
        print("\n📈 PERFORMING EXPLORATORY DATA ANALYSIS")
        print("=" * 50)
        
        # Basic information
        print(f"Dataset shape: {data.shape}")
        print(f"Churn rate: {data['churned'].mean():.2%}")
        print(f"Missing values: {data.isnull().sum().sum()}")
        
        # Set up the plotting style
        plt.style.use('default')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Churn distribution
        plt.subplot(3, 4, 1)
        churn_counts = data['churned'].value_counts()
        plt.pie(churn_counts.values, labels=['Retained', 'Churned'], autopct='%1.1f%%', 
                startangle=90, colors=['lightblue', 'salmon'])
        plt.title('Customer Churn Distribution')
        
        # 2. Age distribution by churn
        plt.subplot(3, 4, 2)
        for churn_status in [0, 1]:
            subset = data[data['churned'] == churn_status]
            plt.hist(subset['age'], alpha=0.7, bins=20, 
                    label=f"{'Churned' if churn_status else 'Retained'}")
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.title('Age Distribution by Churn Status')
        plt.legend()
        
        # 3. Monthly charges vs churn
        plt.subplot(3, 4, 3)
        data.boxplot(column='monthly_charges', by='churned', ax=plt.gca())
        plt.title('Monthly Charges by Churn Status')
        plt.suptitle('')
        
        # 4. Contract type vs churn
        plt.subplot(3, 4, 4)
        contract_churn = pd.crosstab(data['contract_type'], data['churned'], normalize='index')
        contract_churn.plot(kind='bar', ax=plt.gca(), color=['lightblue', 'salmon'])
        plt.title('Churn Rate by Contract Type')
        plt.xticks(rotation=45)
        plt.legend(['Retained', 'Churned'])
        
        # 5. Customer service calls vs churn
        plt.subplot(3, 4, 5)
        service_churn = data.groupby('customer_service_calls')['churned'].mean()
        service_churn.plot(kind='bar', ax=plt.gca(), color='orange')
        plt.title('Churn Rate by Service Calls')
        plt.xlabel('Number of Service Calls')
        plt.ylabel('Churn Rate')
        
        # 6. Account length vs churn
        plt.subplot(3, 4, 6)
        for churn_status in [0, 1]:
            subset = data[data['churned'] == churn_status]
            plt.hist(subset['account_length_months'], alpha=0.7, bins=20,
                    label=f"{'Churned' if churn_status else 'Retained'}")
        plt.xlabel('Account Length (Months)')
        plt.ylabel('Frequency')
        plt.title('Account Length by Churn Status')
        plt.legend()
        
        # 7. Satisfaction score vs churn
        plt.subplot(3, 4, 7)
        data.boxplot(column='satisfaction_score', by='churned', ax=plt.gca())
        plt.title('Satisfaction Score by Churn Status')
        plt.suptitle('')
        
        # 8. Internet service vs churn
        plt.subplot(3, 4, 8)
        internet_churn = pd.crosstab(data['internet_service'], data['churned'], normalize='index')
        internet_churn.plot(kind='bar', ax=plt.gca(), color=['lightblue', 'salmon'])
        plt.title('Churn Rate by Internet Service')
        plt.xticks(rotation=45)
        plt.legend(['Retained', 'Churned'])
        
        # 9. Payment method vs churn
        plt.subplot(3, 4, 9)
        payment_churn = pd.crosstab(data['payment_method'], data['churned'], normalize='index')
        payment_churn.plot(kind='bar', ax=plt.gca(), color=['lightblue', 'salmon'])
        plt.title('Churn Rate by Payment Method')
        plt.xticks(rotation=45)
        plt.legend(['Retained', 'Churned'])
        
        # 10. Correlation heatmap
        plt.subplot(3, 4, 10)
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        correlation_matrix = data[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, ax=plt.gca(), cbar_kws={'shrink': 0.8})
        plt.title('Feature Correlation Matrix')
        
        # 11. Late payments vs churn
        plt.subplot(3, 4, 11)
        late_churn = data.groupby('late_payments')['churned'].mean()
        late_churn.plot(kind='bar', ax=plt.gca(), color='red', alpha=0.7)
        plt.title('Churn Rate by Late Payments')
        plt.xlabel('Number of Late Payments')
        plt.ylabel('Churn Rate')
        
        # 12. Feature importance preview (using simple correlation)
        plt.subplot(3, 4, 12)
        feature_corr = data[numeric_cols].corrwith(data['churned']).abs().sort_values(ascending=True)
        feature_corr.plot(kind='barh', ax=plt.gca(), color='green', alpha=0.7)
        plt.title('Feature Correlation with Churn')
        plt.xlabel('Absolute Correlation')
        
        plt.tight_layout()
        plt.show()
        
        # Summary statistics
        print("\n📊 SUMMARY STATISTICS BY CHURN STATUS")
        print("=" * 50)
        summary_stats = data.groupby('churned')[numeric_cols].agg(['mean', 'std'])
        print(summary_stats.round(2))
        
        return data
    
    def preprocess_data(self, data):
        """
        Preprocess the data for machine learning
        """
        print("\n🔧 PREPROCESSING DATA")
        print("=" * 30)
        
        # Create a copy
        processed_data = data.copy()
        
        # Handle missing values (if any)
        imputer = SimpleImputer(strategy='mean')
        numeric_cols = processed_data.select_dtypes(include=[np.number]).columns
        processed_data[numeric_cols] = imputer.fit_transform(processed_data[numeric_cols])
        
        # Feature engineering
        print("🔨 Creating new features...")
        
        # Calculate average charge per month
        processed_data['avg_charge_per_month'] = processed_data['total_charges'] / processed_data['account_length_months']
        
        # Create customer value segments
        processed_data['customer_value'] = pd.cut(processed_data['total_charges'], 
                                                bins=3, labels=['Low', 'Medium', 'High'])
        
        # Create satisfaction categories
        processed_data['satisfaction_category'] = pd.cut(processed_data['satisfaction_score'], 
                                                       bins=[0, 5, 7, 10], 
                                                       labels=['Low', 'Medium', 'High'])
        
        # Service usage intensity
        processed_data['service_usage_intensity'] = (
            processed_data['avg_monthly_gb_used'] * processed_data['avg_monthly_minutes'] / 1000
        ).fillna(0)
        
        # Risk factors
        processed_data['high_risk_payment'] = (processed_data['payment_method'] == 'Electronic check').astype(int)
        processed_data['month_to_month'] = (processed_data['contract_type'] == 'Month-to-month').astype(int)
        processed_data['high_service_calls'] = (processed_data['customer_service_calls'] > 3).astype(int)
        processed_data['frequent_late_payments'] = (processed_data['late_payments'] > 2).astype(int)
        
        # Encode categorical variables
        print("🏷️ Encoding categorical variables...")
        categorical_cols = ['gender', 'internet_service', 'online_security', 'tech_support',
                          'streaming_tv', 'streaming_movies', 'contract_type', 'payment_method',
                          'paperless_billing', 'customer_value', 'satisfaction_category']
        
        label_encoders = {}
        for col in categorical_cols:
            if col in processed_data.columns:
                le = LabelEncoder()
                processed_data[col + '_encoded'] = le.fit_transform(processed_data[col].astype(str))
                label_encoders[col] = le
        
        # Select features for modeling
        feature_cols = [
            'age', 'account_length_months', 'monthly_charges', 'total_charges',
            'customer_service_calls', 'late_payments', 'avg_monthly_gb_used',
            'avg_monthly_minutes', 'satisfaction_score', 'avg_charge_per_month',
            'service_usage_intensity', 'high_risk_payment', 'month_to_month',
            'high_service_calls', 'frequent_late_payments'
        ]
        
        # Add encoded categorical features
        encoded_cols = [col for col in processed_data.columns if col.endswith('_encoded')]
        feature_cols.extend(encoded_cols)
        
        X = processed_data[feature_cols]
        y = processed_data['churned']
        
        print(f"✅ Features prepared: {len(feature_cols)} features")
        print(f"📊 Dataset size: {X.shape}")
        
        return X, y, processed_data, label_encoders
    
    def train_models(self, X, y):
        """
        Train multiple machine learning models
        """
        print("\n🤖 TRAINING MACHINE LEARNING MODELS")
        print("=" * 40)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                          random_state=42, stratify=y)
        
        # Scale the features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Define models
        models = {
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'SVM': SVC(random_state=42, probability=True)
        }
        
        # Train and evaluate models
        results = {}
        
        for name, model in models.items():
            print(f"\n🔄 Training {name}...")
            
            if name in ['Logistic Regression', 'SVM']:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                y_prob = model.predict_proba(X_test_scaled)[:, 1]
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                y_prob = model.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            roc_auc = roc_auc_score(y_test, y_prob)
            
            # Cross-validation
            if name in ['Logistic Regression', 'SVM']:
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
            else:
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
            
            results[name] = {
                'model': model,
                'predictions': y_pred,
                'probabilities': y_prob,
                'roc_auc': roc_auc,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'classification_report': classification_report(y_test, y_pred)
            }
            
            print(f"✅ {name} - ROC AUC: {roc_auc:.4f}")
            print(f"📊 CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
        
        self.models = results
        self.X_test = X_test
        self.y_test = y_test
        self.X_test_scaled = X_test_scaled
        
        # Select best model
        best_model_name = max(results, key=lambda x: results[x]['roc_auc'])
        self.best_model = results[best_model_name]['model']
        self.best_model_name = best_model_name
        
        print(f"\n🏆 Best Model: {best_model_name} (ROC AUC: {results[best_model_name]['roc_auc']:.4f})")
        
        return results
    
    def evaluate_models(self):
        """
        Comprehensive model evaluation and visualization
        """
        print("\n📊 MODEL EVALUATION AND COMPARISON")
        print("=" * 40)
        
        # Create evaluation plots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # 1. ROC Curves
        ax1 = axes[0, 0]
        for name, result in self.models.items():
            fpr, tpr, _ = roc_curve(self.y_test, result['probabilities'])
            ax1.plot(fpr, tpr, label=f"{name} (AUC: {result['roc_auc']:.3f})")
        ax1.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate')
        ax1.set_title('ROC Curves Comparison')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Model Performance Comparison
        ax2 = axes[0, 1]
        model_names = list(self.models.keys())
        roc_scores = [self.models[name]['roc_auc'] for name in model_names]
        cv_scores = [self.models[name]['cv_mean'] for name in model_names]
        
        x = np.arange(len(model_names))
        width = 0.35
        ax2.bar(x - width/2, roc_scores, width, label='Test ROC AUC', alpha=0.8)
        ax2.bar(x + width/2, cv_scores, width, label='CV ROC AUC', alpha=0.8)
        ax2.set_xlabel('Models')
        ax2.set_ylabel('ROC AUC Score')
        ax2.set_title('Model Performance Comparison')
        ax2.set_xticks(x)
        ax2.set_xticklabels(model_names, rotation=45)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Confusion Matrix for Best Model
        ax3 = axes[0, 2]
        best_predictions = self.models[self.best_model_name]['predictions']
        cm = confusion_matrix(self.y_test, best_predictions)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax3)
        ax3.set_title(f'Confusion Matrix - {self.best_model_name}')
        ax3.set_xlabel('Predicted')
        ax3.set_ylabel('Actual')
        
        # 4. Feature Importance (for tree-based models)
        if self.best_model_name in ['Random Forest', 'Gradient Boosting']:
            ax4 = axes[1, 0]
            importances = self.best_model.feature_importances_
            feature_names = self.X_test.columns
            indices = np.argsort(importances)[::-1][:15]  # Top 15 features
            
            ax4.barh(range(len(indices)), importances[indices])
            ax4.set_yticks(range(len(indices)))
            ax4.set_yticklabels([feature_names[i] for i in indices])
            ax4.set_xlabel('Feature Importance')
            ax4.set_title(f'Top 15 Feature Importances - {self.best_model_name}')
            ax4.invert_yaxis()
            
            self.feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
        
        # 5. Prediction Probability Distribution
        ax5 = axes[1, 1]
        best_probabilities = self.models[self.best_model_name]['probabilities']
        
        # Separate probabilities by actual class
        churn_probs = best_probabilities[self.y_test == 1]
        no_churn_probs = best_probabilities[self.y_test == 0]
        
        ax5.hist(no_churn_probs, bins=30, alpha=0.7, label='No Churn', density=True)
        ax5.hist(churn_probs, bins=30, alpha=0.7, label='Churn', density=True)
        ax5.set_xlabel('Predicted Churn Probability')
        ax5.set_ylabel('Density')
        ax5.set_title('Prediction Probability Distribution')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Model Calibration Plot
        ax6 = axes[1, 2]
        from sklearn.calibration import calibration_curve
        
        for name, result in self.models.items():
            fraction_of_positives, mean_predicted_value = calibration_curve(
                self.y_test, result['probabilities'], n_bins=10
            )
            ax6.plot(mean_predicted_value, fraction_of_positives, marker='o', 
                    label=name, linewidth=2)
        
        ax6.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Perfect Calibration')
        ax6.set_xlabel('Mean Predicted Probability')
        ax6.set_ylabel('Fraction of Positives')
        ax6.set_title('Calibration Plot')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Print detailed results
        print(f"\n📋 DETAILED RESULTS FOR {self.best_model_name}")
        print("=" * 50)
        print(self.models[self.best_model_name]['classification_report'])
        
        if self.feature_importance is not None:
            print(f"\n🔍 TOP 10 MOST IMPORTANT FEATURES")
            print("=" * 40)
            print(self.feature_importance.head(10).to_string(index=False))
    
    def make_predictions(self, customer_data=None):
        """
        Make predictions for new customers
        """
        print("\n🔮 MAKING PREDICTIONS FOR NEW CUSTOMERS")
        print("=" * 45)
        
        if customer_data is None:
            # Create sample customer profiles for demonstration
            sample_customers = pd.DataFrame({
                'age': [25, 45, 65],
                'account_length_months': [3, 24, 48],
                'monthly_charges': [85, 65, 45],
                'total_charges': [255, 1560, 2160],
                'customer_service_calls': [5, 1, 0],
                'late_payments': [3, 0, 0],
                'avg_monthly_gb_used': [25, 15, 5],
                'avg_monthly_minutes': [300, 500, 200],
                'satisfaction_score': [4, 8, 9],
                'avg_charge_per_month': [85, 65, 45],
                'service_usage_intensity': [7.5, 7.5, 1.0],
                'high_risk_payment': [1, 0, 0],
                'month_to_month': [1, 0, 0],
                'high_service_calls': [1, 0, 0],
                'frequent_late_payments': [1, 0, 0],
                'gender_encoded': [0, 1, 0],
                'internet_service_encoded': [1, 1, 0],
                'online_security_encoded': [0, 1, 1],
                'tech_support_encoded': [0, 1, 1],
                'streaming_tv_encoded': [1, 1, 0],
                'streaming_movies_encoded': [1, 1, 0],
                'contract_type_encoded': [0, 1, 2],
                'payment_method_encoded': [0, 2, 3],
                'paperless_billing_encoded': [1, 1, 0],
                'customer_value_encoded': [0, 1, 2],
                'satisfaction_category_encoded': [0, 2, 2]
            })
            
            customer_profiles = ['High Risk', 'Medium Risk', 'Low Risk']
        else:
            sample_customers = customer_data
            customer_profiles = [f'Customer {i+1}' for i in range(len(customer_data))]
        
        # Make predictions
        if self.best_model_name in ['Logistic Regression', 'SVM']:
            sample_scaled = self.scaler.transform(sample_customers)
            predictions = self.best_model.predict(sample_scaled)
            probabilities = self.best_model.predict_proba(sample_scaled)[:, 1]
        else:
            predictions = self.best_model.predict(sample_customers)
            probabilities = self.best_model.predict_proba(sample_customers)[:, 1]
        
        # Create results DataFrame
        results_df = pd.DataFrame({
            'Customer_Profile': customer_profiles,
            'Churn_Probability': probabilities,
            'Predicted_Churn': ['Yes' if p == 1 else 'No' for p in predictions],
            'Risk_Level': ['High' if p > 0.7 else 'Medium' if p > 0.3 else 'Low' for p in probabilities]
        })
        
        print(results_df.to_string(index=False))
        
        return results_df
    
    def generate_business_insights(self):
        """
        Generate actionable business insights from the model
        """
        print("\n💡 BUSINESS INSIGHTS AND RECOMMENDATIONS")
        print("=" * 50)
        
        if self.feature_importance is not None:
            top_features = self.feature_importance.head(5)
            
            print("🔍 KEY CHURN DRIVERS:")
            for idx, row in top_features.iterrows():
                print(f"   • {row['feature']}: {row['importance']:.4f}")
            
            print("\n📋 ACTIONABLE RECOMMENDATIONS:")
            
            # Generate specific recommendations based on top features
            recommendations = []
            
            for _, row in top_features.iterrows():
                feature = row['feature']
                
                if 'satisfaction_score' in feature:
                    recommendations.append("🎯 Implement customer satisfaction monitoring and proactive outreach programs")
                elif 'customer_service_calls' in feature:
                    recommendations.append("📞 Invest in first-call resolution training and self-service options")
                elif 'late_payments' in feature:
                    recommendations.append("💳 Develop payment reminder systems and flexible payment plans")
                elif 'month_to_month' in feature:
                    recommendations.append("📋 Offer incentives for longer-term contracts (discounts, perks)")
                elif 'monthly_charges' in feature:
                    recommendations.append("💰 Review pricing strategy and offer value-based packages")
                elif 'account_length' in feature:
                    recommendations.append("🕒 Create onboarding programs and early engagement initiatives")
                elif 'age' in feature:
                    recommendations.append("👥 Develop age-specific retention strategies and communication channels")
            
            for i, rec in enumerate(recommendations[:5], 1):
                print(f"   {i}. {rec}")
        
        print("\n📊 CHURN PREVENTION STRATEGY:")
        print("   🚨 High Risk (>70% churn probability):")
        print("      - Immediate personal outreach by retention team")
        print("      - Offer significant discounts or service upgrades")
        print("      - Schedule satisfaction surveys and feedback sessions")
        
        print("   ⚠️  Medium Risk (30-70% churn probability):")
        print("      - Automated email campaigns with personalized offers")
        print("      - Proactive customer service check-ins")
        print("      - Loyalty program enrollment")
        
        print("   ✅ Low Risk (<30% churn probability):")
        print("      - Standard retention communications")
        print("      - Upselling opportunities")
        print("      - Referral program invitations")
    
    def save_model_artifacts(self, filepath='churn_model_artifacts'):
        """
        Save model and preprocessing artifacts for deployment
        """
        import pickle
        import os
        
        print(f"\n💾 SAVING MODEL ARTIFACTS")
        print("=" * 30)
        
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        
        # Save the best model
        with open(f'{filepath}/best_model.pkl', 'wb') as f:
            pickle.dump(self.best_model, f)
        
        # Save the scaler
        with open(f'{filepath}/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        
        # Save feature importance
        if self.feature_importance is not None:
            self.feature_importance.to_csv(f'{filepath}/feature_importance.csv', index=False)
        
        # Save model performance metrics
        performance_data = {
            'best_model_name': self.best_model_name,
            'roc_auc_score': self.models[self.best_model_name]['roc_auc'],
            'cv_mean_score': self.models[self.best_model_name]['cv_mean'],
            'cv_std_score': self.models[self.best_model_name]['cv_std']
        }
        
        with open(f'{filepath}/model_performance.pkl', 'wb') as f:
            pickle.dump(performance_data, f)
        
        print(f"✅ Model artifacts saved to '{filepath}/' directory")
        print("   📁 Files created:")
        print("      - best_model.pkl (trained model)")
        print("      - scaler.pkl (feature scaler)")
        print("      - feature_importance.csv (feature rankings)")
        print("      - model_performance.pkl (performance metrics)")

def create_deployment_api():
    """
    Create a simple Flask API for model deployment
    """
    api_code = '''
from flask import Flask, request, jsonify
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model artifacts
with open('churn_model_artifacts/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('churn_model_artifacts/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict_churn():
    try:
        # Get data from request
        data = request.json
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        
        # Make prediction
        if hasattr(model, 'predict_proba'):
            # Scale if needed (for logistic regression or SVM)
            if 'Logistic' in str(type(model)) or 'SVM' in str(type(model)):
                df_scaled = scaler.transform(df)
                probability = model.predict_proba(df_scaled)[0][1]
                prediction = model.predict(df_scaled)[0]
            else:
                probability = model.predict_proba(df)[0][1]
                prediction = model.predict(df)[0]
        
        # Determine risk level
        if probability > 0.7:
            risk_level = 'High'
        elif probability > 0.3:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return jsonify({
            'churn_probability': float(probability),
            'predicted_churn': bool(prediction),
            'risk_level': risk_level,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open('churn_prediction_api.py', 'w') as f:
        f.write(api_code)
    
    print("🚀 Deployment API created: 'churn_prediction_api.py'")
    print("   To run: python churn_prediction_api.py")
    print("   API endpoint: POST http://localhost:5000/predict")

# MAIN EXECUTION
def main():
    """
    Main execution function for the complete analytics project
    """
    print("🚀 CUSTOMER CHURN PREDICTION - ANALYTICS PROJECT")
    print("=" * 60)
    print("📝 Project Overview:")
    print("   • Generate synthetic customer data")
    print("   • Perform comprehensive exploratory data analysis")
    print("   • Engineer features and preprocess data")
    print("   • Train and compare multiple ML models")
    print("   • Generate business insights and recommendations")
    print("   • Create deployment-ready artifacts")
    print("=" * 60)
    
    # Initialize the predictor
    predictor = CustomerChurnPredictor()
    
    # Step 1: Generate synthetic data
    data = predictor.generate_synthetic_data(n_samples=10000)
    
    # Save the generated data
    data.to_csv('customer_churn_dataset.csv', index=False)
    print("💾 Dataset saved as 'customer_churn_dataset.csv'")
    
    # Step 2: Exploratory Data Analysis
    data = predictor.perform_eda(data)
    
    # Step 3: Data preprocessing
    X, y, processed_data, label_encoders = predictor.preprocess_data(data)
    
    # Step 4: Train models
    results = predictor.train_models(X, y)
    
    # Step 5: Evaluate models
    predictor.evaluate_models()
    
    # Step 6: Make sample predictions
    sample_predictions = predictor.make_predictions()
    
    # Step 7: Generate business insights
    predictor.generate_business_insights()
    
    # Step 8: Save model artifacts
    predictor.save_model_artifacts()
    
    # Step 9: Create deployment API
    create_deployment_api()
    
    print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")
    print("=" * 40)
    print("📊 Generated Outputs:")
    print("   1. customer_churn_dataset.csv - Synthetic dataset")
    print("   2. churn_model_artifacts/ - Model files for deployment")
    print("   3. churn_prediction_api.py - Flask API for predictions")
    print("   4. Comprehensive analysis plots and insights")
    
    print("\n💡 Next Steps:")
    print("   • Deploy the model using the provided API")
    print("   • Integrate with existing customer systems")
    print("   • Set up automated retraining pipeline")
    print("   • Implement real-time churn alerts")
    print("   • A/B test retention strategies")
    
    return predictor, data, results

# Run the complete project
if __name__ == "__main__":
    predictor, dataset, model_results = main()