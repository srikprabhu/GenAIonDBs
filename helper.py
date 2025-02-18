import re
import json

def extract_json_content(input_string):
    pattern = r'\{.*\}'
    match = re.search(pattern, input_string, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None
    

if __name__ == "__main__":
    response = '''json
    {
    "sql_query": "WITH EmployeeStatusCounts AS (\n  SELECT \n    Employment_Type,\n    Loan_Status,\n    COUNT(Loan_ID) AS TotalCount\n  FROM Employee\n  WHERE Employment_Type = 'Salaried'\n  GROUP BY Employment_Type, Loan_Status\n)\nSELECT\n  ES.Employment_Type AS EmployeeType,\n  SUM(CASE WHEN ES.Loan_Status = 0 THEN ES.TotalCount ELSE 0 END) AS UnpaidCount,\n  SUM(CASE WHEN ES.Loan_Status = 1 THEN ES.TotalCount ELSE 0 END) AS PaidCount\nFROM EmployeeStatusCounts AS ES\nGROUP BY ES.Employment_Type;"
    }
    '''

    response = extract_json_content(response)
    print("1",type(response),response)
    response = json.loads(response, strict=False)
    print("2",type(response),response)
