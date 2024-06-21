from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# Connect to SQL Server
try:
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=KASHISH\\SQLEXPRESS;'
                          'DATABASE=myproject;'
                          'Trusted_Connection=yes;')
except pyodbc.Error as e:
    print("Error connecting to SQL Server:", e)
    exit()

# Define the route to fetch all visa information
@app.route('/visainformation', methods=['GET'])
def get_all_visainformation():
    try:
        # Create a cursor
        cursor = conn.cursor()
        # Execute the stored procedure to get all visa information
        cursor.execute("EXEC get_visainfo_by_params")
        # Fetch all rows returned by the stored procedure
        rows = cursor.fetchall()
        # Close the cursor
        cursor.close()
        # If no rows found, return 404 Not Found
        if not rows:
            return jsonify({'error': 'No visa information found'}), 404
        # Convert the rows to a list of dictionaries
        visainformation_list = []
        for row in rows:
            visainfo = {
                'countryID': row[0],
                'destination_country': row[1]
                # Add other columns as needed
            }
            visainformation_list.append(visainfo)
        # Return the data as JSON
        return jsonify(visainformation_list), 200
    except pyodbc.Error as e:
        return jsonify({'error': f'SQL error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
