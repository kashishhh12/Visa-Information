from flask import Flask, jsonify, request
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

# Define the route to fetch data by ID
@app.route('/visainfo/<nationality>/<source_country>/<destination_country>', methods=['GET'])
def get_visainfo(nationality, source_country, destination_country):
    try:
        # Create a cursor
        cursor = conn.cursor()

        # Execute the stored procedure passing parameters
        cursor.execute("EXEC dbo.get_visainfo @nationality=?, @source_country=?, @destination_country=?",
                       (nationality, source_country, destination_country))

        # Fetch all rows returned by the stored procedure
        rows = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # If no rows found, return 404 Not Found
        if not rows:
            return jsonify({'error': 'Visa information not found for the provided parameters'}), 404

        # Convert the rows to a list of dictionaries
        visainfo_list = []
        for row in rows:
            visainfo = {
                'nationality': row[0],
                'source_country': row[1],
                'destination_country': row[2],
                'visa_requirement': row[3],
                'visa_type': row[4],
                'validity': row[5],
                'max_stay': row[6],
                'service_fee(in AED)': row[7],
                'Document_requirement': row[8]
                # Add other columns as needed
            }
            visainfo_list.append(visainfo)

        # Return the data as JSON
        return jsonify(visainfo_list), 200

    except pyodbc.Error as e:
        return jsonify({'error': f'SQL error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
