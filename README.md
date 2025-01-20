# GenAI on DBs

## Overview
`GenAIonDBs` explores the integration of **Generative AI** with **Databases** to enhance data-driven applications. This repository provides tools, frameworks, and examples to showcase how Generative AI models can be applied to database operations, data generation, and intelligent querying.

## Key Features
- **Generative Data Insights**:
  - Use AI to analyze and generate summaries of database content.
- **Intelligent Querying**:
  - Convert natural language queries into SQL statements using AI.
- **Data Augmentation**:
  - Generate synthetic data for testing and training.
- **Use Case Demonstrations**:
  - Real-world examples of how GenAI can enhance database interactions.

## Technologies Used
- **Programming Languages**: Python
- **AI Frameworks**: OpenAI, Hugging Face Transformers
- **Database Systems**: MySQL, PostgreSQL, SQLite (extendable to others)
- **Libraries**:
  - `sqlalchemy` for database abstraction.
  - `pandas` for data manipulation.
  - `langchain` for natural language processing.

## Installation
Follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/srikprabhu/GenAIonDBs.git
   cd GenAIonDBs
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Add your API keys (e.g., OpenAI API key) to an `.env` file:
     ```
     OPENAI_API_KEY=<your_api_key>
     ```

5. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage
### Key Functionalities
1. **Natural Language to SQL**:
   - Input a natural language query, and the system generates a corresponding SQL statement.

2. **Data Augmentation**:
   - Generate synthetic data for specific database tables.

3. **Summarizing Data**:
   - Provide insights or summaries of database contents using Generative AI.

### Examples
#### Natural Language Query to SQL
Input:
```
"Show me the top 10 customers by revenue."
```
Output SQL:
```sql
SELECT customer_name, SUM(revenue) AS total_revenue
FROM customers
GROUP BY customer_name
ORDER BY total_revenue DESC
LIMIT 10;
```

#### Generating Synthetic Data
Input:
```
Generate 1000 rows of customer data with attributes: name, age, city, and purchase amount.
```
Output:
- Inserts 1000 rows of realistic-looking customer data into the specified table.

## Contributing
We welcome contributions to this project! Here’s how you can help:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Create a Pull Request.

## Roadmap
- [ ] Extend support to more database systems (e.g., MongoDB, Snowflake).
- [ ] Add a web-based user interface.
- [ ] Integrate advanced AI models for multilingual query support.
- [ ] Optimize for performance with large-scale databases.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or suggestions, please contact:
- **Author**: Srikanth Prabhu
- **Email**: [Your Email Address Here]
- **GitHub**: [https://github.com/srikprabhu](https://github.com/srikprabhu)

---
Thank you for exploring **GenAIonDBs**! We hope this project helps you unlock the power of Generative AI in database operations.
