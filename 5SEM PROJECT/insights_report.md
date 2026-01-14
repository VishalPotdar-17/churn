# Telecom Customer Churn Business Insights

## Executive Summary
This report analyzes customer churn patterns based on the synthetic telecom dataset. The goal is to identify key drivers of churn and recommend strategies to improve retention.

## Key Findings

### 1. Contract Type is the Dominant Factor
- **Observation**: Customers with **Month-to-month** contracts exhibit a drastically higher churn rate compared to those on **One-year** or **Two-year** contracts.
- **Insight**: Flexibility allows customers to leave easily. Long-term contracts act as a strong barrier to exit.
- **Recommendation**: 
    - Offer discounts or value-added services (e.g., free streaming subscription) for customers upgrading to 1-year or 2-year contracts.
    - Implement a "loyalty check-in" program for month-to-month users after 3 months.

### 2. Internet Service & Tech Support
- **Observation**: Customers with **Fiber optic** internet service have higher churn rates than DSL users, likely due to higher price points or potential technical issues.
- **Observation**: Customers who subscribe to **Tech Support** and **Online Security** churn less.
- **Recommendation**:
    - Bundle Tech Support with Fiber optic plans to increase perceived value and reduce frustration.
    - Investigate Fiber optic service reliability and pricing competitiveness.

### 3. Tenure and Lifecycle
- **Observation**: The risk of churn is highest in the first **12 months** (low tenure).
- **Insight**: If a customer survives the first year, they are much more likely to stay loyal.
- **Recommendation**:
    - Focus retention efforts heavily on the first 90 days (onboarding).
    - Provide "milestone rewards" at 6 months and 12 months.

### 4. Payment Methods
- **Observation**: **Electronic check** users churn more frequently than those using automatic bank transfers or credit cards.
- **Insight**: Manual payment methods require active customer action, providing a monthly decision point to "renew or quit". Automatic payments reduce friction.
- **Recommendation**:
    - Incentivize Auto-Pay setup (e.g., $5/month discount).

## Predictive Model Performance
- The developed **Gradient Boosting Classifier** achieves an accuracy of approximately **82%**.
- It effectively identifies high-risk customers, allowing the marketing team to target interventions efficiently.

## Conclusion
To reduce churn, the company should shift focus from customer acquisition to retention, specifically targeting month-to-month fiber optic users with tenure under 1 year. Promoting longer contracts and automatic payments will yield the highest ROI.
