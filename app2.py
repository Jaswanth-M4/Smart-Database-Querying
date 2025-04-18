from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and generate SQL query
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

# Function to execute SQL query
def read_sql_query(sql, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    col_names = [description[0] for description in cur.description]
    conn.close()
    return col_names, rows

# Prompt for Gemini
prompt = [
    """
    You are an expert in converting English questions to SQLlite queries!
    "The database is in SQLite, not MySQL. Use only SQLite-compatible queries."
    The SQL database is named classicmodels and has the following important tables and columns:

    1. customers(customerNumber, customerName, contactLastName, contactFirstName, phone, addressLine1, addressLine2, city, state, postalCode, country, salesRepEmployeeNumber, creditLimit)
    2. employees(employeeNumber, lastName, firstName, extension, email, officeCode, reportsTo, jobTitle)
    3. offices(officeCode, city, phone, addressLine1, addressLine2, state, country, postalCode, territory)
    4. orders(orderNumber, orderDate, requiredDate, shippedDate, status, comments, customerNumber)
    5. orderdetails(orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
    6. payments(customerNumber, checkNumber, paymentDate, amount)
    7. products(productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
    8. productlines(productLine, textDescription)

    Examples:
    Q: How many customers are in the database?
    A: SELECT COUNT(*) FROM customers;

    Q: List the names of all employees working in officeCode '1'.
    A: SELECT firstName, lastName FROM employees WHERE officeCode = '1';

    Q: Show all orders placed in 2004.
    A: SELECT * FROM orders WHERE orderDate LIKE '2004%';

    IMPORTANT:
    - Do not include ``` or the word "sql"
    - Just return the SQL query
    """
]

# Streamlit App UI
st.set_page_config(page_title="Natural Language to SQL")
st.title("Smart Data Querying using Generative AI")
st.subheader("Ask a question about the ClassicModels database")

# Define a trigger function to run when Enter is pressed
def run_query():
    st.session_state['trigger'] = True

# Input field with trigger on Enter
st.text_input("Enter your question:", key="input", on_change=run_query)

# If Enter pressed or Submit button clicked
if st.session_state.get("trigger") or st.button("Submit"):
    st.session_state["trigger"] = False  # Reset trigger
    question = st.session_state.get("input", "")
    
    if question.strip() != "":
        try:
            sql_query = get_gemini_response(question, prompt)
            st.write("Generated SQL Query:")
            st.code(sql_query, language="sql")

            columns, result = read_sql_query(sql_query, "classicmodels.db")
            st.write("Query Results:")
            if result:
                st.dataframe([dict(zip(columns, row)) for row in result])
            else:
                st.info("Query executed successfully but returned no results.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
