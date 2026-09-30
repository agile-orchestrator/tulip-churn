# Dead code that slopguard's vulture check should ignore. Delete a line once it is no longer true.

# pydantic fields of Customer and Score: FastAPI reads and writes them, our code never does.
CreditScore  # unused variable (src/tulip_churn/api.py:20)
Geography  # unused variable (src/tulip_churn/api.py:21)
Gender  # unused variable (src/tulip_churn/api.py:22)
Age  # unused variable (src/tulip_churn/api.py:23)
Tenure  # unused variable (src/tulip_churn/api.py:24)
Balance  # unused variable (src/tulip_churn/api.py:25)
NumOfProducts  # unused variable (src/tulip_churn/api.py:26)
HasCrCard  # unused variable (src/tulip_churn/api.py:27)
IsActiveMember  # unused variable (src/tulip_churn/api.py:28)
EstimatedSalary  # unused variable (src/tulip_churn/api.py:29)
churn_probability  # unused variable (src/tulip_churn/api.py:33)
at_risk  # unused variable (src/tulip_churn/api.py:34)

# Only called from notebooks/01_exploration.ipynb, which vulture does not scan (until #10).
evaluate  # unused function (src/tulip_churn/evaluate.py:6)

# Unused: the target column is hard-coded as "Exited" instead. Remove once code uses TARGET.
TARGET  # unused variable (src/tulip_churn/data.py:12)
